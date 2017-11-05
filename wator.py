import numpy


class WaTor:

    def __init__(self, creatures=None,
                 shape=None, nfish=None, nsharks=None,
                 age_fish=None, age_shark=None,
                 energy_initial=None, energies=None, energy_eat=None):
        """Setup WaTor simulation."""
        self.age_fish = age_fish if age_fish else 5
        self.age_shark = age_shark if age_shark else 10
        self.energy_initial = energy_initial if energy_initial else 5
        self.energy_eat = energy_eat if energy_eat else 3

        if creatures is not None:
            if nfish is not None or nsharks is not None or shape is not None:
                raise(ValueError)
            self.creatures = creatures
        else:
            if shape is None or nfish is None or nsharks is None:
                raise(ValueError)
            self.creatures = numpy.zeros(shape, dtype=numpy.int)

            wator_size = shape[0] * shape[1]
            wator_index = numpy.arange(wator_size)
            random_index = numpy.random.choice(wator_index,
                                               size=nfish + nsharks,
                                               replace=False)

            fish_ages = numpy.random.randint(1, self.age_fish + 1, size=nfish)
            fish_index = random_index[:nfish]
            self.creatures.flat[fish_index] = fish_ages

            shark_ages = numpy.random.randint(-self.age_shark, 0, size=nsharks)
            shark_index = random_index[nfish:]
            self.creatures.flat[shark_index] = shark_ages

        if energies is not None:
            if energies.shape != self.creatures.shape or \
               energy_initial is not None:
                raise(ValueError)
            self.energies = energies
        else:
            self.energies = numpy.zeros_like(self.creatures, dtype=numpy.int)
            self.energies[self.creatures < 0] = self.energy_initial

        self.width, self.height = self.creatures.shape

    def count_fish(self):
        """Return number of fish."""
        # fish are represented as positive numbers
        return numpy.sum(self.creatures > 0)

    def count_sharks(self):
        """Return number of sharks."""
        # fish are represented as negative numbers
        return numpy.sum(self.creatures < 0)

    def tick(self):
        """Simulate one chronon."""
        new_fish = numpy.copy(self.creatures)
        new_fish[self.creatures > 0] = 0

        directions = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
        for x, y in numpy.argwhere(self.creatures > 0):  # for each fish
            moved = False
            for i, j in numpy.random.permutation(directions):  # random move
                a, b = (x + i) % self.width, (y + j) % self.height
                if new_fish[a, b] == 0:  # move if the field is empty
                    new_fish[a, b] = self.creatures[x, y] + 1
                    moved = True
            if not moved:
                new_fish[x, y] = self.creatures[x, y] + 1


        new_shark = numpy.copy(new_fish)
        new_shark[self.creatures < 0] = 0
        new_energies = numpy.copy(self.energies)

        for x, y in numpy.argwhere(new_fish < 0):  # for each shark
            moved = False
            for i, j in numpy.random.permutation(directions):
                a, b = (x + i) % self.width, (y + j) % self.height
                if new_shark[a, b] > 0:  # if there is fish eat it
                    new_shark[a, b] = new_fish[x, y] - 1
                    new_energies[a, b] = self.energies[x, y] + self.energy_eat
                    moved = True

            if moved:
                continue

            for i, j in numpy.random.permutation(directions):
                a, b = (x + i) % self.width, (y + j) % self.height
                if new_shark[a, b] == 0:  # if there is fish eat it
                    new_shark[a, b] = new_fish[x, y] - 1
                    new_energies[a, b] = self.energies[x, y]

        new_shark[new_energies == 1] = 0
        new_energies[new_energies > 0] -= 1

        self.creatures = new_shark
        self.energies = new_energies
        return self

