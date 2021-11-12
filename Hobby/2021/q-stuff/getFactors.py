import qlib as q

bits = []

for i in range(5):
    bits.append(q.fakeQBit())
stateVector = q.stateSpace(bits)#




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