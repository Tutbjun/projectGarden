import math
import numpy as np
#from numpy.core.numeric import False_
#from numpy.lib.shape_base import take_along_axis
from numba import jit

#constants#
sqrt2resiprok = 1/math.sqrt(2)
hadamarMat = np.array([[1,1],[1,-1]], dtype=np.float)

simulate = False

class fakeQBit():
    selfVector = np.zeros(2, dtype=np.cdouble)
    
    def normalize(self):
        squareSum = 0
        for e in self.selfVector:
            squareSum += pow(e,2)
        amplitude = math.sqrt(squareSum)
        self.selfVector /= amplitude

    def __init__(self):
        self.selfVector[0] = 1



class stateSpace():
    bits = []
    states = np.empty(0)

    def __init__(self,inBits):
        self.bits = list(inBits)
        self.updateStateVector()
    
    def updateStateVector(self):
        self.states = stateTensorProduct(self.bits)
        self.bits = None


def stateTensorProduct(states):
    states = states[::-1]
    vec = states[0].selfVector
    for i in range(1,len(states)):
        newVec = np.zeros(len(vec)*len(states[i].selfVector),dtype=np.cdouble)
        for j,e in enumerate(vec):
            for k,f in enumerate(states[i].selfVector):
                newVec[j*2+k] = e*f
        vec, newVec = newVec, None
    return vec

@jit
def toBinary(n):
    div = n/2
    if div != 0:
        ret = f'{n % 2}'
        return toBinary(int(div)) + ret
    return f'{n % 2}'

def getBinaryStringList(integer,binaryLength=8):
    stringList = toBinary(integer).split()#toBinary(integer)
    while len(stringList) < binaryLength:
        stringList.append('0')
    return stringList

def bit_hadamar(bit):
    bit.selfVector = np.matmul(hadamarMat,bit.selfVector)*sqrt2resiprok
    return bit
def zFlip():
    raise NotImplementedError


def controlledXFlip(states, target ,*controls):
    bitCount = round(math.log(len(states))/math.log(2))
    controls = list(np.asarray(controls).flatten())
    if simulate:
        toOpStates = []
        for i in range(len(states)):
            bits = getBinaryStringList(i,max(controls)+1)
            controlsTrue = True
            for j,t in enumerate(bits):
                for b in controls:
                    if b == j:
                        if t != '1':
                            controlsTrue = False
                            break
                if controlsTrue == False:
                    break
            if controlsTrue == True:
                toOpStates.append(i)
        while len(toOpStates) > 0:
            partFound = False
            for i,e in enumerate(toOpStates):
                state1 = getBinaryStringList(e,bitCount)
                state1.pop(target)
                for j,f in enumerate(toOpStates[i+1:]):
                    state2 = getBinaryStringList(f,bitCount)
                    state2.pop(target)
                    if state1 == state2:
                        states[e],states[f] = states[f],states[e]
                        toOpStates.pop(j+1+i)
                        toOpStates.pop(i)
                        partFound = True
                        break
                if partFound:
                    break
        return states
    else:
        raise NotImplementedError
def bit_xFlip(bit):
    bit.selfVector[0], bit.selfVector[1] = bit.selfVector[1], bit.selfVector[0]
    return bit
def yFlip():
    raise NotImplementedError
    

def checkOpInputs(states,*usedInputRanges):
    bitSum = 0
    #usedInputRanges = [e for sublist in usedInputRanges for e in sublist]
    for r in usedInputRanges:
        bitSum += len(r)
    bits = round(math.log(len(states))/math.log(2))
    if bitSum > bits:
        raise ValueError('requested to use more bits than available for opperation')
    for i,r1 in enumerate(usedInputRanges):
        for j,r2 in enumerate(usedInputRanges):
            if j != i:
                if r1[0] <= r2[1] and r2[0] <= r1[1]:
                    raise ValueError('requested to use more bits that overlap each other')

def multiply(states,aBits,bBits,carryBits,outBits):
    states = states.states
    checkOpInputs(states, aBits, bBits, carryBits, outBits)
    for i,a in enumerate(aBits):
        for j,b in enumerate(bBits):#multiplies to carry bits
            states =  controlledXFlip(states, carryBits[j]+i, a, b)
        states = sumToInput1(states,outBits,carryBits)#sums carry bits to output
        for j,b in enumerate(bBits):#does multiply again to revert carry bits
            states =  controlledXFlip(states, carryBits[j]+i, a, b)
    return states

def sumToInput1(states,elem1Bits,elem2Bits):
    """if len(elem1Bits) - 1 != len(elem2Bits):
        raise ValueError('not enough bits to carry out adittion')"""
    for i,e in enumerate(elem2Bits):
        for j,k in enumerate(elem1Bits[:len(elem1Bits)-i]):
            cbits = elem1Bits[i:-1-j]#range(elem1Range[0]+i,elem1Range[1]-1-j))
            cbits.append(e)
            states = controlledXFlip(states, elem1Bits[-1-j], cbits)
    return states