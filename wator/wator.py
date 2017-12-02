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
                                                     self.age_fish,
                                                     self.age_shark)

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

    def tick(self):
        """Simulate one chronon."""
        self.creatures, self.energies = cwator.tick(self.creatures,
                                                    self.energies,
                                                    self.age_fish,
                                                    self.age_shark,
                                                    self.energy_eat)
        return self
