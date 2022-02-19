import time

import qlib as q
q.simulate = True


bits = []
for i in range(10):
    bits.append(q.fakeQBit())
inputABits = list(range(0,2))
inputBBits = list(range(inputABits[-1]+1,inputABits[-1]+3))
carryBits = list(range(inputBBits[-1]+1,inputBBits[-1]+4))
outBits = list(range(carryBits[-1]+1,carryBits[-1]+4))
for i,_ in enumerate(inputABits+inputBBits):
    #bits[i] = q.bit_xFlip(bits[i])
    bits[i] = q.bit_hadamar(bits[i])
stateVector = q.stateSpace(bits)
t1 = time.time()
stateVector = q.multiply(stateVector,inputABits,inputBBits,carryBits,outBits)
print(time.time()-t1)


#prep qubits for operation
#perform circuit in loop
    #oracle (flip arround s' space)
        #multiply
        #comparator
        #z-flip
        #de-comparator
        #de-multiply
    #hadamars (make bases in s space)
    #phase flip (flip arround s)
    #hadamars (reverts bases to s' space)





pass