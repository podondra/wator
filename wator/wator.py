import numpy
from . import cwator


class WaTor:
    def __init__(self, creatures=None,
                 shape=None, nfish=None, nsharks=None,
                 age_fish=None, age_shark=None,
                 energy_initial=None, energies=None, energy_eat=None):
        """Setup WaTor simulation."""
        # member variables setup
        self.age_fish = age_fish if age_fish else 5
        self.age_shark = -age_shark if age_shark else -10
        self.energy_initial = energy_initial if energy_initial else 5
        self.energy_eat = energy_eat if energy_eat else 3

        # WaTor planet setup
        error_msg = 'Either provide creatures or shape, nfish and nsharks'
        if creatures is not None:   # creatures provided
            if nfish is not None or nsharks is not None or shape is not None:
                raise ValueError(error_msg)
            self.creatures = creatures.astype(numpy.int8, copy=False)
        else:  # create creatures
            if shape is None or nfish is None or nsharks is None:
                raise ValueError(error_msg)
            self.creatures = cwator.random_creatures(shape, nfish, nsharks,
                    self.age_fish, self.age_shark)

        if energies is not None:
            if energies.shape != self.creatures.shape:
                raise ValueError('Shapes of creatures and energies must be '
                                 'the same.')
            if energy_initial is not None:
                raise ValueError('Do not provide energy_initial together with '
                                 'energies.')
            self.energies = energies.astype(numpy.int64, copy=False)
        else:
            self.energies = numpy.full(self.creatures.shape,
                    self.energy_initial, dtype=numpy.int64)

        self.height, self.width = self.creatures.shape

    def count_fish(self):
        """Return number of fish."""
        # fish are represented as positive numbers
        return numpy.sum(self.creatures > 0)

    def count_sharks(self):
        """Return number of sharks."""
        # fish are represented as negative numbers
        return numpy.sum(self.creatures < 0)

    def _generate_move(self, x, y):
        directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        for i, j in numpy.random.permutation(directions):
            a, b = (x + i) % self.height, (y + j) % self.width
            if (a, b) != (x, y):  # cannot move to same field
                yield a, b

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
                new_creatures[x, y] = min(self.creatures[x, y] + 1,
                                          self.age_fish)

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
        new_energies[a, b] = self.energies[x, y] + energy_gain

    def _move_sharks(self, new_creatures, new_energies):
        for x, y in numpy.argwhere(self.creatures < 0):  # for each shark
            moved = False
            # find fish
            for a, b in self._generate_move(x, y):
                if new_creatures[a, b] > 0:  # if there is fish eat it
                    self._move_shark(new_creatures, new_energies, (x, y),
                                     (a, b), self.energy_eat)
                    moved = True
                    break

            if moved:
                continue

            # move
            for a, b in self._generate_move(x, y):
                if new_creatures[a, b] == 0:
                    self._move_shark(new_creatures, new_energies,
                                     (x, y), (a, b))
                    moved = True
                    break

            if not moved:
                new_creatures[x, y] = max(self.creatures[x, y] - 1,
                                          self.age_shark)
                new_energies[x, y] = self.energies[x, y]

        new_energies -= 1
        new_creatures[(new_energies == 0) & (new_creatures < 0)] = 0

        return new_creatures, new_energies

    def tick(self):
        """Simulate one chronon."""
        new_creatures = numpy.copy(self.creatures)
        new_energies = numpy.copy(self.energies)
        new_fish = self._move_fish(new_creatures)
        self.creatures, self.energies = self._move_sharks(new_fish,
                                                          new_energies)
        return self
