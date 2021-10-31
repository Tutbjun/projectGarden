import zeta
import numpy as np
from numba import jit,cuda
import time
import math
import matplotlib.pyplot as plt

threadsperblock = (16, 16)

@jit
def get_complex_grid(rmin,rmax,imin,imax,divission):
    grid = []
    for i in range(round(imin/divission),round(imax/divission)):
        for r in range(round(rmin/divission),round(rmax/divission)):
            grid.append(complex(r,i))
    return np.asarray(grid)

@jit
def calc_zeta_grid(grid,n):
    result = np.zeros(len(grid),dtype=np.dtype(np.complex128))
    for i,g in enumerate(grid):
        result[i] = zeta.zeta_numeric(g, n)
    return result


def calc_zeta_points(rmin,rmax,imin,imax,divission,n):
    grid = get_complex_grid(rmin,rmax,imin,imax,divission)
    result = calc_zeta_grid(grid,n)
    return result

def plot_complex(data):
    x = [e.real for e in data]
    y = [e.imag for e in data]
    plt.scatter(x, y)
    plt.ylabel('Imaginary')
    plt.xlabel('Real')
    plt.show()

def main():
    plot_complex(calc_zeta_points(1.0001,1.1,-0.01,0.01,0.005,10))
    

if __name__ == '__main__':
    main()
    