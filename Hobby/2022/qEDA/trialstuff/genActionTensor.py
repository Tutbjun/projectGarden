

















#start with unit tensor
#multiply all matricies by val
#store to file
from os import path
import numpy as np

fileName = 'Supply'
bufferCount = 100
pinCount = 1

def main():
    #arrays to fill: diff and non diff, 0. 1. and 2. power, and all pins
    defaultArray = np.zeros(bufferCount)
    defaultArray[0] = 1
    arr = np.zeros((pinCount,pinCount,6,bufferCount), dtype=np.float16)
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            for k in range(len(arr[0][0])):
                arr[i][j][k] = defaultArray
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            for k in range(len(arr[0][0])):
                mult = input(f'Multiply {i}x{j}x{k} by: ')
                arr[i][j][k] *= float(mult)
    np.save(path.join(path.dirname(__file__),f'{fileName}'),arr)

if __name__ == '__main__':
    main()