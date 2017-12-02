# cythonize code by hroncok
# available at https://github.com/hroncok/wator/blob/master/wator/_cwator.pyx

#cython language_level=3
#cython cdivision=3
#cython boundscheck=False
#cython initializedcheck=False
#cython wrapatuond=False
#cython nonecheck=False
#cython overflowcheck=False

cimport  numpy
from libc.stdlib cimport rand
import numpy


ctypedef numpy.int8_t I8
ctypedef numpy.int64_t I64


cdef int randint(int low, int high):
    return low + (rand() % (high - low))


def random_creatures(shape, int nfish, int nsharks,
                      int age_fish, int age_shark):
    cdef numpy.ndarray[I8, ndim=2] c = numpy.zeros(shape, dtype=numpy.int8)
    cdef int height = shape[0]
    cdef int width = shape[1]
    cdef int size = height * width
    cdef int empties = size - nfish - nsharks
    cdef int i, j, rand

    if empties < 0:
        raise ValueError('Too many creatures for small shape')

    for i in range(height):
        for j in range(width):
            rand = randint(0, empties + nfish + nsharks)
            if rand < empties:
                empties -= 1
            elif rand < empties + nfish:
                c[i, j] = randint(1, age_fish + 1)
                nfish -= 1
            else:
                c[i, j] = randint(age_shark, 0)
                nsharks -= 1
    return c


cdef bint is_fish(numpy.ndarray[I8, ndim=2] creatures, int i, int j):
    return creatures[i, j] > 0


cdef bint is_shark(numpy.ndarray[I8, ndim=2] creatures, int i, int j):
    return creatures[i, j] < 0


cdef bint is_empty(numpy.ndarray[I8, ndim=2] creatures, int i, int j):
    return creatures[i, j] == 0


cdef bint is_dead(numpy.ndarray[I64, ndim=2] energies, int i, int j):
    return energies[i, j] <= 0


cdef bint is_moved(numpy.ndarray[I8, ndim=2] moved, int i, int j):
    return moved[i, j]


cdef void move_one_fish(numpy.ndarray[I8, ndim=2] creatures,
        numpy.ndarray[I64, ndim=2] energies, numpy.ndarray[I8, ndim=2] moved,
        numpy.ndarray[I64, ndim=2] targets, int age_fish, int height,
        int width, int i, int j):
    cdef int count = 0
    cdef int tmp, t0, t1

    tmp = (i - 1 + height) % height
    if is_empty(creatures, tmp, j):
        targets[count, 0] = tmp
        targets[count, 1] = j
        count +=1

    tmp = (i + 1) % height
    if is_empty(creatures, tmp, j):
        targets[count, 0] = tmp
        targets[count, 1] = j
        count +=1

    tmp = (j - 1 + width) % width
    if is_empty(creatures, i, tmp):
        targets[count, 0] = i
        targets[count, 1] = tmp
        count +=1

    tmp = (j + 1) % width
    if is_empty(creatures, i, tmp):
        targets[count, 0] = i
        targets[count, 1] = tmp
        count +=1

    if count > 0:
        tmp = randint(0, count)
        t0 = targets[tmp, 0]
        t1 = targets[tmp, 1]

        if creatures[i, j] > age_fish:
            creatures[t0, t1] = 1
            creatures[i, j] = 1
            moved[i, j] = True
        else:
            creatures[t0, t1] = creatures[i, j] + 1
            creatures[i, j] = 0
        moved[t0, t1] = True
    else:
        moved[i, j] = True
        if creatures[i, j] <= age_fish:
            creatures[i, j] += 1


cdef void move_one_shark(numpy.ndarray[I8, ndim=2] creatures,
        numpy.ndarray[I64, ndim=2] energies, numpy.ndarray[I8, ndim=2] moved,
        numpy.ndarray[I64, ndim=2] targets, int age_shark, int energy_eat,
        int height, int width, int i, int j):
    cdef int count = 0
    cdef int tmp, t0, t1

    tmp = (i - 1 + height) % height
    if is_fish(creatures, tmp, j):
        targets[count, 0] = tmp
        targets[count, 1] = j
        count +=1

    tmp = (i + 1) % height
    if is_fish(creatures, tmp, j):
        targets[count, 0] = tmp
        targets[count, 1] = j
        count +=1

    tmp = (j - 1 + width) % width
    if is_fish(creatures, i, tmp):
        targets[count, 0] = i
        targets[count, 1] = tmp
        count +=1

    tmp = (j + 1) % width
    if is_fish(creatures, i, tmp):
        targets[count, 0] = i
        targets[count, 1] = tmp
        count +=1

    if count == 0:
        tmp = (i - 1 + height) % height
        if is_empty(creatures, tmp, j):
            targets[count, 0] = tmp
            targets[count, 1] = j
            count +=1

        tmp = (i + 1) % height
        if is_empty(creatures, tmp, j):
            targets[count, 0] = tmp
            targets[count, 1] = j
            count +=1

        tmp = (j - 1 + width) % width
        if is_empty(creatures, i, tmp):
            targets[count, 0] = i
            targets[count, 1] = tmp
            count +=1

        tmp = (j + 1) % width
        if is_empty(creatures, i, tmp):
            targets[count, 0] = i
            targets[count, 1] = tmp
            count +=1

    energies[i, j] -= 1

    if count > 0:
        tmp = randint(0, count)
        t0 = targets[tmp, 0]
        t1 = targets[tmp, 1]

        was_fish = is_fish(creatures, t0, t1)

        if creatures[i, j] < age_shark:
            creatures[t0, t1] = -1
            creatures[i, j] = -1
            moved[i, j] = True
        else:
            creatures[t0, t1] = creatures[i, j] - 1
            creatures[i, j] = 0
        moved[t0, t1] = True

        energies[t0, t1] = energies[i, j]
        if was_fish:
            energies[t0, t1] += energy_eat
    else:
        moved[i, j] = True
        if creatures[i, j] >= age_shark:
            creatures[i, j] -= 1


cdef void move_fish(numpy.ndarray[I8, ndim=2] creatures,
        numpy.ndarray[I64, ndim=2] energies, numpy.ndarray[I8, ndim=2] moved,
        numpy.ndarray[I64, ndim=2] targets, int age_fish, int height,
        int width):
    cdef int i, j
    for i in range(height):
        for j in range(width):
            if is_fish(creatures, i, j) and not is_moved(moved, i, j):
                move_one_fish(creatures, energies, moved, targets, age_fish,
                              height, width, i, j)


cdef void move_sharks(numpy.ndarray[I8, ndim=2] creatures,
        numpy.ndarray[I64, ndim=2] energies, numpy.ndarray[I8, ndim=2] moved,
        numpy.ndarray[I64, ndim=2] targets, int age_shark, int energy_eat,
        int height, int width):
    cdef int i, j
    for i in range(height):
        for j in range(width):
            if is_shark(creatures, i, j) and not is_moved(moved, i, j):
                move_one_shark(creatures, energies, moved, targets, age_shark,
                        energy_eat, height, width, i, j)


cdef void remove_dead_sharks(numpy.ndarray[I8, ndim=2] creatures,
        numpy.ndarray[I64, ndim=2] energies, int height, int width):
    cdef int i, j
    for i in range(height):
        for j in range(width):
            if is_shark(creatures, i, j) and is_dead(energies, i, j):
                creatures[i, j] = 0


def tick(numpy.ndarray[I8, ndim=2] creatures,
        numpy.ndarray[I64, ndim=2] energies, int age_fish, int age_shark,
        int energy_eat):
    cdef numpy.ndarray[I8, ndim=2] moved
    cdef numpy.ndarray[I64, ndim=2] targets = \
        numpy.ndarray((4, 2), dtype=numpy.int64)

    cdef int height = creatures.shape[0]
    cdef int width = creatures.shape[1]

    moved = numpy.zeros((height, width), dtype=numpy.int8)
    move_fish(creatures, energies, moved, targets, age_fish, height, width)

    moved[::] = 0
    move_sharks(creatures, energies, moved, targets, age_shark, energy_eat,
                height, width)

    remove_dead_sharks(creatures, energies, height, width)
    return creatures, energies
