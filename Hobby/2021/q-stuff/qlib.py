import math
import numpy as np


class fakeQBit():
    selfVector = np.zeros(2, dtype=np.cdouble)
    
    def normalize(self):
        squareSum = 0
        for e in self.selfVector:
            squareSum += pow(e,2)
        amplitude = math.sqrt(squareSum)
        self.selfVector /= amplitude

    def __init__(self):
        self.selfVector[1] = 1



class stateSpace():
    bits = []
    states = np.empty(0)

    def __init__(self,inBits):
        self.bits = list(inBits)
        self.updateStateVector()
    
    def updateStateVector(self):
        self.states = stateTensorProduct(self.bits)


def stateTensorProduct(states):
    vec = states[0].selfVector
    for i in range(1,len(states)):
        newVec = np.zeros(len(vec)*len(states[i].selfVector),dtype=np.cdouble)
        for j,e in enumerate(vec):
            for k,f in enumerate(states[i].selfVector):
                newVec[j*2+k] = e*f
        vec = newVec
    return vec

def gates():
    def hadamar():
        raise NotImplementedError
    def zFlip():
        raise NotImplementedError
    def controlledXFlip(bit,*controls):
        raise NotImplementedError
    def xFlip():
        raise NotImplementedError
    def yFlip():
        raise NotImplementedError
    
def operations():
    

    def checkOpInputs(state,*usedInputRanges):
        bitSum = 0
        for r in usedInputRanges:
            bitSum += r[1]-r[0]
        if bitSum > len(state):
            raise ValueError('requested to use more bits than available for opperation')
        for r1 in usedInputRanges:
            for r2 in usedInputRanges:
                if r1[0] <= r2[1] and r2[0] <= r1[1]:
                    raise ValueError('requested to use more bits that overlap each other')

    def multiply(state,aRange,bRange,carryRange,outRange):
        checkOpInputs(state, aRange, bRange, carryRange, outRange)
        for i,abit in enumerate(state[aRange]):
            for j,bbit in enumerate(state[bRange]):
                state[carryRange[j]+i] = gates.controlledXFlip(state[carryRange[j]+i], abit,bbit)
            state[outRange] = sumToInput1(state,outRange,carryRange)
            for j,bbit in enumerate(state[bRange]):
                state[carryRange[j]+i] = gates.cnot(state[carryRange[j]+i], abit,bbit)

    def sumToInput1(state,elem1Range,elem2Range):
        checkOpInputs(state,elem1Range,elem2Range)
        if elem1Range[1] - elem1Range[0] - 1 != elem2Range[1] - elem2Range[0]:
            raise ValueError('not enough bits to carry out adittion')
        ##prøv igen i morgen, tror på dig :)
        for i,j in enumerate(range(elem2Range[1]+1,elem2Range[0]+1,-1)):
            for k in range(j):
                controlIndecies = list(range(elem1Range[0],elem1Range[1]-i))
                controlIndecies.append(list(range(elem2Range))[i])
                controlNTargetIndecies = controlIndecies
                controlNTargetIndecies.insert())
                state[]
                state[]
        gates.controlledXFlip()
        
        
        
        