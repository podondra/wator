import numpy


class WaTor:
    age_fish = 5
    age_shark = 10
    energy_initial = 5

    def __init__(self, creatures=None,
                 shape=None, nfish=None, nsharks=None,
                 age_fish=None, age_shark=None,
                 energy_initial=None, energies=None):
        """Setup WaTor simulation."""
        self.age_fish = age_fish if age_fish else 5
        self.age_shark = age_shark if age_shark else 10
        self.energy_initial = energy_initial if energy_initial else 5

        if creatures is not None:
            if nfish or nsharks or shape:
                raise(ValueError)
            self.creatures = creatures
        else:
            if not shape or not nfish or not nsharks:
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
            if energies.shape != self.creatures.shape or energy_initial:
                raise(ValueError)
            self.energies = energies
        else:
            self.energies = numpy.zeros_like(self.creatures, dtype=numpy.int)
            self.energies[self.creatures < 0] = self.energy_initial

    def tick(self):
        """Simulate one chronone."""
        return self

    def count_fish(self):
        """Return number of fish."""
        # fish are represented as positive numbers
        return numpy.sum(self.creatures > 0)

    def count_sharks(self):
        """Return number of sharks."""
        # fish are represented as negative numbers
        return numpy.sum(self.creatures < 0)
