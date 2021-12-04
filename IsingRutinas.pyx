# cython: language_level=3

cimport cython

import numpy as np
cimport numpy as np

from libc.math cimport exp
from libc.stdlib cimport rand
cdef extern from 'limits.h':
    int RAND_MAX

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.profile(False)
@cython.cdivision(False)
cdef EvaluacionSpinesArreglo(np.float64_t[:,:] spines,np.float64_t T):
    cdef np.float64_t total_energia, dE
    cdef int N = spines.shape[0]
    cdef int i,j

    for i in range(N):
        for j in range(N):
            total_energia = spines[(i+1)%N,j]+spines[(i-1)%N,j]+spines[i,(j+1)%N]+spines[i,(j-1)%N]
            dE = 2.0 * spines[i, j] * total_energia
            if exp(-dE / T) > rand()/(RAND_MAX) or dE<0:
                spines[i,j] *= -1 



def EvolucionIsingCy(np.float64_t[:,:] spines,np.float64_t T):
    EvaluacionSpinesArreglo(spines, T)