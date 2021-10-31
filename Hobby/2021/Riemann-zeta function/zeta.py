from numba import jit,cuda

@jit
def zetaPart(s,n):
    r = n**s.real
    c = n**complex(0,s.imag)
    res = r*c
    result = 1/res
    return result.real,result.imag
@jit
def zeta_numeric(s,n):
    sum_r = 0
    sum_c = 0
    for i in range(1,n+1):
        r,c = zetaPart(s,i)
        sum_r += r
        sum_c += c
    return complex(sum_r,sum_c)