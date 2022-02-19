import enum
from genericpath import exists
from re import T
from PIL import Image,ImageTk
import math
from os import path
import UI
import numpy as np
from copy import copy

#TODO: add more actionTensors

#config
class config():
    dt = 10**-6
    bufferLen = 10**-4

class pseudoTensor():
    axis = ''
    arr = np.array([])
    def __init__(self, axi, arrayLike = None, shape = None):
        if str(type(arrayLike)) == "<class '__main__.pseudoTensor'>":
            self.arr = arrayLike.arr
            self.axis = arrayLike.axis
            return
        inIsArr = False
        try:
            if len(np.asarray(arrayLike)) > 0:
                inIsArr = True
        except:
            pass
        if inIsArr and not shape:
            arr = []
            for e in arrayLike:
                try:
                    float(e)
                    arr.append(e)
                except:
                    arr.append(pseudoTensor(axi[1:],e))
            arr = np.asarray(arr)
            self.arr = arr
            self.axis = axi[0]
        elif inIsArr and shape:
            raise ValueError
        elif shape:
            arrElem = pseudoTensor(axi[1:],shape=list(shape)[1:])
            try:
                float(arrElem.arr)
                if arrElem.arr == 0:
                    arrElem = 0
            except:
                pass
                
            tempArr = []
            for _ in range(shape[0]):
                tempArr.append(copy(arrElem))
                """elemIsInt = False
                try:
                    int(arrElem)
                    elemIsInt = True    
                except:
                    pass
                if elemIsInt:
                    tempArr.append()
                else:
                """    
            self.arr = np.asarray(tempArr)
            self.axis = axi[0].lower()
        else:
            if arrayLike == None:
                self.arr = 0
            else:    
                self.arr = arrayLike.copy()
    def shape(self):
        shp = tuple([len(self.arr)])
        try: 
            self.arr[0].arr
        except:
            return shp
        try: 
            float(self.arr[0])
        except:
            return (*shp,*self.arr[0].shape())
        return shp

def tensorMult(T1,T2):
    arr = T1.arr * T2
    return pseudoTensor([T1.axis],arr)

def tensorSum(tensorList):
    inIsFloat = False
    try:
        float(tensorList[0])
        inIsFloat = True
    except:
        pass
    if inIsFloat:
        return np.sum(tensorList)
    else:
        if len(tensorList) == 1:
            return tensorList[0]
        shp = tensorList[0].shape()
        sumArr = np.zeros((len(tensorList),*shp))
        for i in range(0,len(tensorList)):
            sumArr[i] = tensorList[i].arr
        return sumArr.sum(axis=0)

def tensorOpperation(T1, T2):
    multList = []
    try:
        float(T1)
        try:
            float(T2)
            return T2*T1
        except:
            return tensorMult(T2,T1)
    except:
        try:
            float(T2)
            return tensorMult(T1,T2)
        except:
            pass
    if len(T1.arr) != len(T2.arr) or T1.axis == T2.axis:
        raise ValueError
    for i in range(len(T1.arr)):
        multList.append(tensorOpperation(T1.arr[i],T2.arr[i]))
    if T1.axis == 'x':
        return tensorSum(multList)
    elif T1.axis == 'y':
        return pseudoTensor(['y'],multList)
    else:
        raise ValueError


class circuitSim():
    components = []
    nets = {}
    _newNetsSchedule = {'latestComp' : False}
    def __init__(self):
        self.bufferCount = int(config.bufferLen/config.dt)

    def addComponent(self, type, pos = (0,0)):
        self.components.append(type(pos = pos))
        self._updateAll()#will in this case create new nets for all pins

    def renderCircuit(self):
        UI.renderCircuit(self)

    def _addNet(self,compNr,pinNr):
        newNet = net(self.nets,self.bufferCount)
        self.nets[newNet.id] = newNet
        #self.nets.append()
        #id = self.nets[-1].id
        self.components[compNr].connections[pinNr] = newNet.id

    def mergeNets(self,toMerge,componentsReferences=None):
        newId = min(toMerge)
        newNet = self.nets[newId]
        
        if componentsReferences:
            for cr in componentsReferences:
                self.components[cr[0]].connections[cr[1]] = newNet.id
        else:
            raise NotImplementedError
        for i in range(len(self.nets[toMerge[0]].stateBuffer)):
            avg = netState(0,0)
            for n in toMerge:
                avg.voltage += self.nets[n].stateBuffer[i].voltage
                avg.dVoltage += self.nets[n].stateBuffer[i].dVoltage
            avg.dVoltage /= len(toMerge)
            avg.voltage /= len(toMerge)
            newNet.stateBuffer[i] = avg
        self.nets[newNet.id] = newNet
        for n in toMerge:
            if n != newNet.id:
                self.nets.pop(n)
    def addConnection(self,componentConnections):
        netsToMerge = []
        for cc in componentConnections:
            netId = self.components[cc[0]].connections[cc[1]]
            netsToMerge.append(netId)
        self.mergeNets(netsToMerge, componentConnections)
    def simulate(self,simTime):
        dt = config.dt
        t = 0
        while t < simTime:
            #t = step*dt
            nT = self.prepNetTensor()#netTensor
            ncTs = pseudoTensor(['y'],[0]*len(nT.arr))#netCurrentTensors
            for c in self.components:
                nTC = pseudoTensor(['y'],nT.arr[c.connections])#netTensorComponent
                change = tensorOpperation(c.actionTensor,nTC)
                for i,old in enumerate(ncTs.arr[c.connections]):
                    ncTs.arr[c.connections][i] = tensorSum([old,change.arr[i]])
            for i in range(len(ncTs.arr)):
                #TODO calc a dt in relationship to net capacitances
                #TODO add dt*I charges to nets
                #TODO from all capacitances in net, calc a voltage increase
                #TODO add the voltage derivative to the net tensor
                raise NotImplementedError
                ncTs.arr[i].arr[1] = (ncTs.arr[i].arr[0] - nT.arr[i].arr[0].arr[1].arr[0]) / dt
            for ncT in ncTs:
                raise NotImplementedError
                self.updateNetsByVector(ncT)
    def getNetTensor(self):
        arr = np.zeros((len(self.nets.keys()),self.bufferCount,2))
        for i,k in enumerate(self.nets.keys()):
            n = self.nets[k]
            for j in range(self.bufferCount):
                arr[i][j] = n.stateBuffer[j].asarray()
        shape = arr.shape
        arr = np.reshape(arr,(shape[0],shape[2],shape[1]))
        return arr
    def prepNetTensor(self):
        nets = self.getNetTensor()
        newTensor = pseudoTensor(['y','x','y','y'],shape=(len(self.nets),1,6,self.bufferCount))
        for i,n in enumerate(nets):
            for j in range(3):
                newTensor.arr[i].arr[0].arr[j].arr = np.power(n[0],j)
                newTensor.arr[i].arr[0].arr[j+3].arr = np.power(n[0],j)
        return newTensor
    def updateNetsByVector():
        return
    def _scheduleNewNets(self,mode=None):
        if mode:
            self._newNetsSchedule[mode] = True
    def _updateAll(self):
        if self._newNetsSchedule['latestComp']:
            pinsOcupied = [True if e else False for e in self.components[-1].connections]
            for i in range(self.components[-1].pinCount):
                if not pinsOcupied[i]:
                    self._addNet(len(self.components)-1,i)
            self._newNetsSchedule['latestComp'] = False
        

class component(circuitSim):
    rotation = 0
    pinCount = 0
    scale = (1,1)
    _ogPinPositions = []
    pinPositions = []
    actionTensor = np.array([])
    _compImg = Image.open(path.join(path.dirname(__file__),"defaultIcon.jpg"))
    icon = 0
    pos = (0,0)
    connections = []
    def __init__(self, pos, pinCount, imgN, scale, pinPositions = []):
        self.pos = pos
        self.pinCount = pinCount
        self.scale = scale
        try:
            self._compImg = Image.open(path.join(path.dirname(__file__),imgN))
        except:
            pass
        self._ogPinPositions = pinPositions
        self._updateIcon()
        self._updatePinPos()
        self._initPinNets()
    def _initPinNets(self):
        self.connections = [None for _ in range(self.pinCount)]
        super()._scheduleNewNets(mode = 'latestComp')
    def _updateIcon(self, scaleMultiplier=1):
        scale = self.scale[0]*scaleMultiplier,self.scale[1]*scaleMultiplier
        icon = self._compImg
        icon = icon.rotate(self.rotation*180/math.pi)
        icon = icon.resize(scale, Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(icon)
    def _updatePinPos(self):
        c = math.cos(self.rotation)
        s = math.sin(self.rotation)
        rotM = np.array([[c,s],[-s,c]])
        self.pinPositions = self._ogPinPositions
        for i,pp in enumerate(self.pinPositions):
            pp = tuple(np.matmul(rotM,np.asarray(pp)))
            self.pinPositions[i] = pp
    def rotateBy(self,rot):
        rot *= math.pi/180
        self.rotation -= rot
        self._updatePinPos()
        self._updateIcon()

class netState():
    voltage = 0
    dVoltage = 0
    def __init__(self, V=0, dV=0):
        self.voltage = V
        self.dVoltage = dV
    def asarray(self):
        return np.array([self.voltage,self.dVoltage],dtype=np.float64)

class net(circuitSim):
    _capacitance = 10**-12
    stateBuffer = []
    id = 0
    def __init__(self,existingNets,bufferCount):
        takenIds = []
        for n in existingNets.keys():
            takenIds.append(existingNets[n].id)
        takenIds.sort()
        for id in range(len(takenIds)):
            if takenIds[id] != id:
                self.id = id
                return
        self.id = len(takenIds)
        self.stateBuffer = np.full((bufferCount),netState())

    def cleanBuffer(self):
        for i in range(len(self.stateBuffer),self.bufferCount,-1):
            self.stateBuffer[i].pop(i)

class opamp(component,circuitSim):
    def __init__(self, scale=(10,10), pos=(50,50)):
        super().__init__(
            pos, 
            5,
            "opAmpIcon.png", 
            scale, 
            pinPositions = [(0.45,0),(-0.01,0.315),(0,-0.33),(-0.5,0.25),(-0.5,-0.25)]
            )

class resistor(component,circuitSim):
    def __init__(self, scale=(3,3), pos=(0,0)):
        super().__init__(
            pos, 
            2,
            "resistor.png", 
            scale,
            pinPositions = [(-0.5,0),(0.5,0)]
            )

class supply(component,circuitSim):
    _voltage = 0
    _maxCurrent = 0
    def __init__(self, scale=(2,2), pos=(0,0)):
        super().__init__(
            pos, 
            1,
            "supply.png", 
            scale,
            pinPositions = [(0.5,0)]
            )
    def setSpecs(self,voltage,current):
        self._voltage = voltage
        self._current = current
        self.actionTensor = np.load(path.join(path.dirname(__file__),'Supply.npy'))#TODO: should return a current which is zeroth order minus first order
        self.actionTensor *= voltage
        self.actionTensor = pseudoTensor(['x','y','x','x'],self.actionTensor)

class caps(component):
    capacitance = 1
    def __init__(self, scale=(3,3), pos=(0,0)):
        super().__init__(
            pos, 
            2,
            "cCap.png", 
            scale,
            pinPositions = [(-0.5,0),(0.5,0)]
            )

class eCap(caps):
    def __init__(self, pos=(0,0)):
        super().__init__(pos = pos)

class cCap(caps):
    def __init__(self, pos=(0,0)):
        super().__init__(pos = pos)

def main():
    c = circuitSim()
    c.addComponent(supply, pos = (15,5))
    c.components[0].rotateBy(90)
    c.components[0].setVoltage(9)
    c.addComponent(resistor, pos = (15,10))
    c.components[1].rotateBy(90)
    c.components[1].resistance = 1000
    c.addComponent(cCap, pos = (15,20))
    c.components[2].rotateBy(90)
    c.components[2].capacitance = 10**(-5)
    c.addComponent(supply, pos = (15,25))
    c.components[3].rotateBy(-90)
    c.components[3].voltage = 0
    c.addConnection([[0,0],[1,0]])
    c.addConnection([[1,1],[2,0]])
    c.addConnection([[2,1],[3,0]])

    """c.addComponent(opamp, pos = (15,10))
    c.addComponent(resistor,pos = (45,10))
    c.addComponent(supply, pos = (14,5))
    c.addConnection([[0,0],[0,1]])
    c.addConnection([[0,0],[1,0]])
    c.addConnection([[2,0],[0,2]])"""
    c.renderCircuit()
    c.simulate(0.01)
    


#klasse component
    #antal pins - done
    #timedependant on function buffer
    #tidsfunktionkatalog - done
    #billede - done
    #netforbindelser - done
    #onstate function for alle ben
    #buffer fill - buffer perform - buffer cleanup, for loop

if __name__ == '__main__':
    main()
        