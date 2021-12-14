# cython: language_level=3

cimport cython

import numpy as np
cimport numpy as np
np.import_array()

ctypedef np.float64_t dtype_t

from libc.math cimport exp
from libc.stdlib cimport rand
cdef extern from 'limits.h':
    int RAND_MAX

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.profile(False)
@cython.cdivision(True)
cdef EvaluacionSpinesArreglo(np.ndarray[dtype_t, ndim=2] spines, np.ndarray[dtype_t, ndim=2] spinesCopia, dtype_t T):
    cdef dtype_t dE, SpinVecinos
    cdef int Nx = <int>spines.shape[0]
    cdef int Ny = <int>spines.shape[1]
    cdef int i,j, iRandom, jRandom
    cdef int i1, i2, j1, j2

    #Iniciamos un doble ciclo for en el cual seleccionamos Nx*Ny celdas aleatorias del arreglo
    #para calcular su nuevo estado de espin
    for i in range(Nx):
        iRandom = rand()%Nx
        i1 = iRandom+1
        i2 = iRandom-1

        if i1 == Nx:
            i1 = 0
        if i2 == -1:
            i2 = Nx-1

        for j in range(Ny):
            jRandom = rand()%Ny
            j1 = jRandom+1
            j2 = jRandom-1

            if j1 == Ny:
                j1 = 0
            if j2 == -1:
                j2 = Ny-1

            #Evaluamo la suma de espines alrededor de la celda elegida y la diferencia de energia de la misma
            SpinVecinos = spinesCopia[i1,jRandom]+spinesCopia[i2,jRandom]+spinesCopia[iRandom,j1]+spinesCopia[iRandom,j2]
            dE = 2.0 * spinesCopia[iRandom, jRandom] * SpinVecinos
            
            #El cambio de estado sucede si la diferencia de energia es negativa
            #o si un numero aleatorio entre 0 y 1 es mayor que el factor de Boltzmann
            if exp(-<dtype_t>dE /<dtype_t> T) > <dtype_t>rand()/<dtype_t>RAND_MAX or dE<0:
                spines[iRandom,jRandom] *= -1


def EvolucionIsingCy(np.ndarray[dtype_t, ndim=2] spines, np.ndarray[dtype_t, ndim=2] spinesCopia, dtype_t T):
    EvaluacionSpinesArreglo(spines, spinesCopia, T)
