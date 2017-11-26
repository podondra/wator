import numpy
cimport numpy
cimport cython


cdef class WaTor:
    cdef int age_fish, age_shark
    cdef numpy.int16_t energy_initial, energy_eat
    cdef int width, height
    cdef public numpy.ndarray creatures
    cdef public numpy.ndarray energies

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef numpy.ndarray[numpy.int8_t, ndim=2] _random_creatures(self, int height, int width, int nfish, int nsharks):
        cdef numpy.ndarray[numpy.int8_t, ndim=2] creatures = numpy.zeros((height, width), dtype=numpy.int8)
        cdef numpy.ndarray[numpy.int32_t] random_index = numpy.random.choice(numpy.arange(height * width, dtype=numpy.int32), size=nfish + nsharks, replace=False)

        creatures.flat[random_index[:nfish]] = numpy.random.randint(1, self.age_fish + 1, size=nfish, dtype=numpy.int8)
        creatures.flat[random_index[nfish:]] = numpy.random.randint(self.age_shark, 0, size=nsharks, dtype=numpy.int8)

        return creatures

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def __cinit__(self, numpy.ndarray creatures=None, shape=None, int nfish=-1, int nsharks=-1,
            int age_fish=-1, int age_shark=-1, int energy_initial=-1, numpy.ndarray energies=None, int energy_eat=-1):
        """Setup WaTor simulation."""
        # member variables setup
        self.age_fish = age_fish if age_fish != -1 else 5
        self.age_shark = -age_shark if age_shark != -1 else -10
        self.energy_initial = energy_initial if energy_initial != -1 else 5
        self.energy_eat = energy_eat if energy_eat != -1 else 3

        # WaTor planet setup
        error_msg = 'Either provide creatures or shape, nfish and nsharks'
        if creatures is not None:   # creatures provided
            if nfish != -1 or nsharks != -1 or shape is not None:
                raise ValueError(error_msg)
            self.creatures = creatures.astype(numpy.int8, copy=False)
        else:  # create creatures
            if shape is None or nfish == -1 or nsharks == -1:
                raise ValueError(error_msg)
            self.creatures = self._random_creatures(shape[0], shape[1], nfish, nsharks)

        self.height = self.creatures.shape[0]
        self.width = self.creatures.shape[1]

        if energies is not None:
            if energies.shape[0] != self.creatures.shape[0] or energies.shape[1] != self.creatures.shape[1]:
                raise ValueError('Shapes of creatures and energies must be the same.')
            if energy_initial != -1:
                raise ValueError('Do not provide energy_initial together with energies.')
            self.energies = energies.astype(numpy.int16, copy=False)
        else:
            self.energies = numpy.zeros((self.height, self.width), dtype=numpy.int16)
            self.energies[self.creatures < 0] = self.energy_initial

    cpdef int count_fish(self):
        """Return number of fish."""
        # fish are represented as positive numbers
        return (self.creatures > 0).sum()

    cpdef int count_sharks(self):
        """Return number of sharks."""
        # fish are represented as negative numbers
        return (self.creatures < 0).sum()

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef numpy.ndarray[numpy.int16_t, ndim=2] _generate_move(self, numpy.int16_t x, numpy.int16_t y):
        cdef int idx
        cdef numpy.ndarray[numpy.int16_t, ndim=2] directions = numpy.array([[-1, 0], [0, -1], [1, 0], [0, 1]], numpy.int16)
        cdef numpy.ndarray[numpy.int16_t, ndim=2] moves = numpy.random.permutation(directions)
        for idx in range(4):
            moves[idx, 0] += x
            moves[idx, 1] += y
            moves[idx, 0] = moves[idx, 0] % self.height
            moves[idx, 1] = moves[idx, 1] % self.width
        return moves

    def _move_fish(self, new_creatures):
        for x, y in numpy.argwhere(self.creatures > 0):  # for each fish
            moved = False
            for a, b in self._generate_move(x, y):
                if new_creatures[a, b] == 0:
                    if new_creatures[x, y] + 1 > self.age_fish:
                        # reproduce
                        new_creatures[x, y] = 1
                        new_creatures[a, b] = 1
                    else:  # move
                        new_creatures[a, b] = self.creatures[x, y] + 1
                        new_creatures[x, y] = 0
                    moved = True
                    break

            if not moved:
                new_creatures[x, y] = min(self.creatures[x, y] + 1, self.age_fish)

        return new_creatures

    def _move_shark(self, new_creatures, new_energies, fr, to, energy_gain=0):
        x, y = fr
        a, b = to
        if new_creatures[x, y] - 1 < self.age_shark:
            new_creatures[x, y] = -1
            new_energies[x, y] = self.energies[x, y]
            new_creatures[a, b] = -1
        else:
            new_creatures[a, b] = self.creatures[x, y] - 1
            new_creatures[x, y] = 0
            new_energies[x, y] = 0
        new_energies[a, b] = self.energies[x, y] + energy_gain

    def _move_sharks(self, new_creatures, new_energies):
        for x, y in numpy.argwhere(self.creatures < 0):  # for each shark
            moved = False
            # find fish
            for a, b in self._generate_move(x, y):
                if new_creatures[a, b] > 0:  # if there is fish eat it
                    self._move_shark(new_creatures, new_energies, (x, y), (a, b), self.energy_eat)
                    moved = True
                    break

            if moved:
                continue

            # move
            for a, b in self._generate_move(x, y):
                if new_creatures[a, b] == 0:
                    self._move_shark(new_creatures, new_energies, (x, y), (a, b))
                    moved = True
                    break

            if not moved:
                new_creatures[x, y] = max(self.creatures[x, y] - 1, self.age_shark)
                new_energies[x, y] = self.energies[x, y]

        new_creatures[new_energies == 1] = 0
        new_energies[new_energies > 0] -= 1

        return new_creatures, new_energies

    def tick(self):
        """Simulate one chronon."""
        cdef numpy.ndarray[numpy.int8_t, ndim=2] new_creatures = numpy.copy(self.creatures)
        cdef numpy.ndarray[numpy.int16_t, ndim=2] new_energies = numpy.copy(self.energies)
        cdef numpy.ndarray[numpy.int8_t, ndim=2] new_fish = self._move_fish(new_creatures)
        self.creatures, self.energies = self._move_sharks(new_fish, new_energies)
        return self
