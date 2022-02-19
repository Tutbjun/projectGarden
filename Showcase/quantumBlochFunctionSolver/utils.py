import numpy as np
import math
from numba import jit

taylorPrecDef = 6

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def capFunc(func,capRange):
    for i,__ in enumerate(func):
        if func[i] < capRange[0]:
            func[i] = capRange[0]
        if func[i] > capRange[1]:
            func[i] = capRange[1]
    return func

def float_range(x, y, jump):
    if '.' in str(jump):
        d = len(str(jump).split('.')[1])
    else:
        d = -1
    d = abs(d)+1
    if x < y:
        while x < y:
            yield x
            x += jump
            x = round(x,d)
    elif x > y:
        while x > y:
            yield x
            x -= jump
            x = round(x,d)

def frange(start, stop, step):
    return(list(float_range(start,stop,step)))

def saveCSV(array,name,baseDirect):
    file = open(f'{baseDirect}/{name}.csv',"w+")
    file.close()
    np.savetxt(f'{baseDirect}/{name}.csv',array,delimiter=";")

@jit
def cosTaylor(x,n):
    if n == 0:
        return 1
    elif n == 1:
        return -x**2/2
    elif n == 2:
        return x**4/24
    elif n == 3:
        return -x**6/720
    elif n == 4:
        return math.pow(x,8)/40320
    elif n == 5:
        return -math.pow(x,10)/3628800
    elif n == 6:
        return math.pow(x,12)/479001600

halfPi=math.pi/2

@jit
def cos(x, n = taylorPrecDef):
    x = abs(x)
    cycles = x/(halfPi)
    x = halfPi*(cycles - int(cycles))
    cycle = int(cycles)+1
    if cycle/2 == cycle//2:
        x-=halfPi
    val = 0
    count = 0
    while (n:=n-1) >= 0:
        val += cosTaylor(x,count)
        count += 1
    wholeCycles = (cycle+2)//2
    if wholeCycles/2 == wholeCycles//2:
        val = -val
    return val

@jit
def sin(x, n = taylorPrecDef):
    return cos(x-halfPi,n)