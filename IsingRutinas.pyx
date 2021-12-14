# cython: language_level=3

cimport cython

import numpy as np
cimport numpy as np
ctypedef np.float64_t dtype_t


from libc.math cimport exp
from libc.stdlib cimport rand
cdef extern from 'limits.h':
    int RAND_MAX

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.profile(False)
@cython.cdivision(False)
cdef EvaluacionSpinesArreglo(np.ndarray[dtype_t, ndim=2] spines,dtype_t T):
    cdef np.float64_t total_energia, dE
    cdef int N = spines.shape[0]
    cdef int i,j, iRandom, jRandom
    cdef int i1, i2, j1, j2

    for i in range(N):
        iRandom = rand()%N
        i1 = iRandom+1
        i2 = iRandom-1

        if i1 == N:
            i1 = 0
        if i2 == -1:
            i2 = N-1

        for j in range(N):
            jRandom = rand()%N
            j1 = jRandom+1
            j2 = jRandom-1

            if j1 == N:
                j1 = 0
            if j2 == -1:
                j2 = N-1

            total_energia = spines[i1,jRandom]+spines[i2,jRandom]+spines[iRandom,j1]+spines[iRandom,j2]
            dE = 2.0 * spines[iRandom, jRandom] * total_energia
            if exp(-dE / T) > rand()/(RAND_MAX) or dE<0:
                spines[iRandom,jRandom] *= -1 


def EvolucionIsingCy(np.ndarray[dtype_t, ndim=2] spines,dtype_t T):
    EvaluacionSpinesArreglo(spines, T)