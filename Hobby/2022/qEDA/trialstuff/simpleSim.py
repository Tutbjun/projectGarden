import enum
from genericpath import exists
from re import T
from PIL import Image,ImageTk
import math
from os import path
import UI
import numpy as np
from copy import copy

#TODO: fix that nets have infinete recursions of itself
#TODO: add log with warning of when the simulation needs smaller dt and make it so that sim redoes with smaller dt
#TODO: fix the net reshaping order


#config
class config():
    dt = 10**-9
    bufferCount = 100
    dV = 10**-2

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
    def multiplyBy(self,val):
        for i,_ in enumerate(self.arr):
            try:
                self.arr[i] *= val
            except:
                self.arr[i].multiplyBy(val)

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
    if T1.axis == T2.axis:# or len(T1.arr) != len(T2.arr):
        raise ValueError
    for i in range(len(T1.arr)):
        if len(T2.arr) == 1:
            multList.append(tensorOpperation(T1.arr[i],T2.arr[0]))
        else:
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
        self.bufferCount = config.bufferCount

    def addComponent(self, type, pos = (0,0), model = None):
        if model:
            self.components.append(type(pos = pos, model = model))
        else:
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
    def renameNet(self,start,target):
        if start != target:
            self.nets[target] = self.nets[start]
            for i in range(len(self.components)):
                for j in range(len(self.components[i].connections)):
                    if self.components[i].connections[j] == start:
                        self.components[i].connections[j] = target
            del self.nets[start]
            self.nets[target].id = target
    def addConnection(self,componentConnections):
        netsToMerge = []
        for cc in componentConnections:
            netId = self.components[cc[0]].connections[cc[1]]
            netsToMerge.append(netId)
        self.mergeNets(netsToMerge, componentConnections)
        keys = list(self.nets.keys())
        for i,k in enumerate(keys):
            self.renameNet(k,i)
    def simulate(self,simTime):
        t = 0
        while t < simTime:
            nT = self.prepNetTensor()#netTensor
            ncTs = pseudoTensor(['y'],np.asarray([0]*len(nT.arr[0].arr),dtype=np.float32))#netCurrentTensors
            for c in self.components:
                nTC = pseudoTensor(['x','y'],[nT.arr[0].arr[c.connections]])#netTensorComponent
                change = tensorOpperation(c.actionTensor,nTC)
                for i,old in enumerate(ncTs.arr[c.connections]):
                    j = c.connections[i]
                    ncTs.arr[j] = tensorSum([old,change.arr[i]])
            Cs = np.asarray([self.nets[k]._capacitance for k in self.nets.keys()])
            for c in self.components:
                for i,j in enumerate(c.connections):
                    Cs[j] += c.pinCapacitances[i]
            dVdts = ncTs.arr/Cs
            dVs = config.dt*dVdts
            if max(abs(dVs)) > config.dV:
                #!log issue
                #! or redo sim with smaller dt
                print("max dV exceeded...")
            for i,dV in enumerate(dVs):
                self.nets[i].updateBufferWithV(dV)
            t += config.dt
    def getNetTensor(self):
        arr = np.zeros((len(self.nets.keys()),self.bufferCount,2))
        for i,k in enumerate(self.nets.keys()):
            n = self.nets[k]
            for j in range(self.bufferCount):
                arr[i][j] = n.stateBuffer[j].asarray()
        shape = arr.shape
        arr = np.reshape(arr,(1,shape[0],shape[2],shape[1]))#!Fix reshaping here
        return arr
    def prepNetTensor(self):
        nets = self.getNetTensor()
        newTensor = pseudoTensor(['x','y','y','y'],shape=(1,len(self.nets),6,self.bufferCount))
        for i,n in enumerate(nets[0]):
            for j in range(3):
                newTensor.arr[0].arr[i].arr[j].arr = np.power(n[0],j)
                newTensor.arr[0].arr[i].arr[j+3].arr = np.power(n[0],j)
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
    #pinCapacitances = []
    rotation = 0
    pinCount = 0
    scale = (1,1)
    _ogPinPositions = []
    pinPositions = []
    actionTensor = np.array([])
    _compImg = Image.open(path.join(path.dirname(__file__),"componentIcons","defaultIcon.jpg"))
    icon = 0
    pos = (0,0)
    connections = []
    def __init__(self, pos, pinCount, imgN, scale, modelName, pinCapacitances, pinPositions = []):
        self.pos = pos
        self.pinCount = pinCount
        self.scale = scale
        try:
            self._compImg = Image.open(path.join(path.dirname(__file__),"componentIcons",imgN))
        except FileNotFoundError:
            print("Component icon not found...")
        self._ogPinPositions = pinPositions
        if len(pinCapacitances) == self.pinCount:
            self.pinCapacitances = pinCapacitances
        self._updateIcon()
        self._updatePinPos()
        self._initPinNets()
        self._loadModelTensor(modelName)
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
    def _loadModelTensor(self,name):
        self.actionTensor = np.load(path.join(path.dirname(__file__),'componentModels',f'{name}.npy'))#TODO: should return a current which is zeroth order minus first order
        self.actionTensor = pseudoTensor(['y','x','x','x'],self.actionTensor)

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

    def updateBufferWithV(self,dV,dt=config.dt):
        V = self.stateBuffer[0].voltage + dV
        dVdt = dV/dt
        nS = netState(V,dVdt)
        self.stateBuffer = np.insert(self.stateBuffer,0,nS)[:-1]

    def cleanBuffer(self):
        for i in range(len(self.stateBuffer),self.bufferCount,-1):
            self.stateBuffer[i].pop(i)

class opamp(component,circuitSim):
    def __init__(self, scale=(10,10), pos=(50,50), model = None):
        super().__init__(
            pos, 
            5,
            "opAmpIcon.png", 
            scale,
            model,
            pinCapacitances=[],
            pinPositions = [(0.45,0),(-0.01,0.315),(0,-0.33),(-0.5,0.25),(-0.5,-0.25)]
            )

class resistor(component,circuitSim):
    def __init__(self, scale=(3,3), pos=(0,0), model = 'res1k'):
        super().__init__(
            pos, 
            2,
            "resistor.png", 
            scale,
            model,
            pinCapacitances=[0,0],
            pinPositions = [(-0.5,0),(0.5,0)]
            )

class supply(component,circuitSim):
    _maxCurrent = 0
    def __init__(self, scale=(2,2), pos=(0,0), model = "supply0v"):#make a more advanced with constant current input by a square wave
        super().__init__(
            pos, 
            1,
            "supply.png", 
            scale,
            model,
            pinCapacitances=[10*(10**(-6))],
            pinPositions = [(0.5,0)]
            )

class caps(component):
    capacitance = 1
    def __init__(self, scale=(3,3), pos=(0,0), model = 'cap'):
        super().__init__(
            pos, 
            2,
            "cCap.png", 
            scale,
            model,
            pinCapacitances=[100*(10**(-6)),100*(10**(-6))],
            pinPositions = [(-0.5,0),(0.5,0)]
            )

class eCap(caps):
    def __init__(self, pos=(0,0), model = None):
        super().__init__(pos = pos, model = model)

class cCap(caps):
    def __init__(self, pos=(0,0), model = None):
        super().__init__(pos = pos, model = model)

def main():
    c = circuitSim()
    c.addComponent(supply, pos = (15,5), model='supply9V')
    c.components[-1].rotateBy(90)
    c.addComponent(resistor, pos = (15,10), model='res1k')
    c.components[-1].rotateBy(90)
    c.components[-1].resistance = 1000
    #c.addComponent(cCap, pos = (15,20), model='cap')
    #c.components[2].rotateBy(90)
    #c.components[2].capacitance = 10**(-5)
    c.addComponent(supply, pos = (15,25), model='supply0V')
    c.components[-1].rotateBy(-90)
    c.addConnection([[0,0],[1,0]])
    c.addConnection([[1,1],[2,0]])
    #c.addConnection([[2,1],[3,0]])
    c.renderCircuit()
    c.simulate(0.01)

if __name__ == '__main__':
    main()        