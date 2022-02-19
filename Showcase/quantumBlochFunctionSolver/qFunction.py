from utils import *
from systemDefiner import sigma
from numba import jit

###########################################funktionværdiudregner (her er den generelle løsning for diff ligningen)#####################################################

def calcFuncVal(x,E,V,k,A,B):
    global sigma
    val = 0
    kx = k*x
    c3 = cos(kx)
    c4 = sin(kx)
    if E >= V:
        c = math.sqrt(E-V)*sigma
        cx = c*x
        c1 = math.cosh(cx)
        c2 = math.sinh(cx)
        if A != 0:
            #val += np.complex128(complex(A*c1*c3,-A*c1*c4))
            val += A*complex(c1*c3, -c1*c4)
        if B != 0:
            #val += np.complex128(complex(B*c2*c4,B*c2*c3))
            val += B*complex(c2*c4,c2*c3)
    elif E < V:
        c = math.sqrt(V-E)*sigma
        cx = c*x
        c1 = cos(cx)
        c2 = sin(cx)
        if A != 0:
            #val += np.complex128(complex(A*c1*c3,-A*c1*c4))
            val += A*complex(c1*c3,-c1*c4)
        if B != 0:
            #val += np.complex128(complex(B*c2*c3,-B*c2*c4))
            val += B*complex(c2*c3,-c2*c4)
    return val

###########################################diffværdiudregner (her er den også generelle løsning for diff ligningen, men dens diff i stedet)#####################################################

def calcDiffVal(x,E,V,k,A,B):
    global sigma
    val = 0
    kx = k*x
    c3 = cos(kx)
    c4 = sin(kx)
    if E >= V:
        c = math.sqrt(E-V)*sigma
        cx = c*x
        c1 = math.cosh(cx)
        c2 = math.sinh(cx)
        if A != 0:
            #val += np.complex128(complex(A*c*c2*c3-A*c1*k*c4,-A*c*c2*c4-A*c1*k*c3))
            val += A*complex(c*c2*c3 - c1*k*c4, - c*c2*c4 - c1*k*c3)
        if B != 0:
            #val += np.complex128(complex(B*c*c1*c4+B*c2*k*c3,B*c*c1*c3-B*c2*k*c4))
            val += B*complex(c*c1*c4 + c2*k*c3,c*c1*c3 - c2*k*c4)
    elif E < V:
        c = math.sqrt(V-E)*sigma
        cx = c*x
        c1 = cos(cx)
        c2 = sin(cx)
        if A != 0:
            #val += np.complex128(complex(-A*c*c2*c3-A*c1*k*c4,A*c*c2*c4-A*c1*k*c3))
            val += A*complex(-c*c2*c3 - c1*k*c4,c*c2*c4 - c1*k*c3)
        if B != 0:
            #val += np.complex128(complex(B*c*c1*c3-B*c2*k*c4,-B*c*c1*c4-B*c2*k*c3))
            val += B*complex(c*c1*c3 - c2*k*c4, - c*c1*c4 - c2*k*c3)
    return val

###########################################A B skaleringsudregning for at opretteholde kontinuerlighed og differentierbarhed på tværs af forskellige potentialetrin#####################################################

def calcB(f,E,V,k,d,x):
    global sigma
    kx = k*x
    c5 = cos(kx)
    c6 = sin(kx)
    if E >= V:
        c1 = math.sqrt(E-V)
        c7 = c1*sigma
        c2 = c7*x
        c3 = math.sinh(c2)
        c4 = math.cosh(c2)
        val = complex((-c3*c6*c7*f + c5*c4*f*k + c6*c4*d),(c3*c5*c7*f + c6*c4*f*k - c5*c4*d))
        val /= c7
    elif E < V:
        c1 = math.sqrt(V-E)
        c7 = c1*sigma
        c2 = c7*x
        c3 = sin(c2)
        c4 = cos(c2)
        val = complex((c3*c5*c7*f - c4*c6*f*k + c4*c5*d), (c6*c3*c7*f + c4*c5*f*k + c4*c6*d))
        val /= c7
    return val

def calcA(f,E,V,k,d,x):
    global sigma
    kx = k*x
    c5 = cos(kx)
    c6 = sin(kx)
    if E >= V:
        c1 = math.sqrt(E-V)
        c7 = c1*sigma
        c2 = x*c7
        c3 = math.sinh(c2)
        c4 = math.cosh(c2)
        val = complex((c4*c5*c7*f + c6*c3*f*k - c5*c3*d),(c4*c6*c7*f - c5*c3*f*k - c6*c3*d))
        val /= c7
    elif E < V:
        c1 = math.sqrt(V-E)
        c7 = c1*sigma
        c2 = x*c7
        c3 = sin(c2)
        c4 = cos(c2)
        val = complex((c6*c3*f*k + c4*c5*c7*f - c3*c5*d),(c6*c4*c7*f - c3*c5*f*k - c6*c3*d))
        val /= c7
    return val