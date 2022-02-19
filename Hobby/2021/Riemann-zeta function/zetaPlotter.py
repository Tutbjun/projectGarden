import cmath
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.type_check import imag, real

def zetaPart(n,s):
    return cmath.exp(-cmath.log(n)*s)

def getZetaLines(N,s):
    vectors = []
    for n in range(1,N+1):
        vectors.append(zetaPart(n,s))
    return vectors

def plotZetaLines(vectors):
    plotList = [[[0,real(vectors[0])],[0,imag(vectors[0])]]]
    for i in range(1,len(vectors)):
        x1 = plotList[i-1][0][1]
        y1 = plotList[i-1][1][1]
        x = [x1, real(vectors[i]) + x1]
        y = [y1, imag(vectors[i]) + y1]
        plotList.append([x,y])

    for i in range(len(plotList)):
        plt.plot(*plotList[i])
    
    plt.grid()
    plt.show()

def main():
    while True:
        zetaCord = complex(input("input complex number zeta cord:  "))
        zetaLines = getZetaLines(5,zetaCord)
        plotZetaLines(zetaLines)

if __name__ == '__main__':
    main()