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
