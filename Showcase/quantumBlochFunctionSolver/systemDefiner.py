import numpy as np
from utils import *
import os
import statistics
from matplotlib import pyplot as plt

numberOfCells = 1
cellRad = 0.5
stepSize = 0.001#skift pot filen hvis den skiftes
coloumbCap = -15
case = "kronig"
verbose = False

qe = 1.60217662
siliconQ = 14*qe
elekperm = 8.8541878176
cKonst = 1/(4*math.pi*elekperm)
hbar = 1
hbarSquare = pow(hbar,2)
m = 1
sigma = math.sqrt(2*m)/hbar


direct = os.getcwd()
limitDist = cellRad*numberOfCells
stepCount = int(2*limitDist/stepSize)
if stepCount / 2 == stepCount // 2:
    stepCount += 1

def loadColoumbFunc(direct):
    return np.loadtxt(direct + "/coloumbFunc.csv",delimiter=";") 

def roundColoumbAmm(base):
    if base // 2 == base / 2:
        base = round(base)
        if base // 2 == base / 2:
            base += 1
    return base

def defineColoumbFunc():
    coloumbAmm = roundColoumbAmm(100)
    coloumbPoints = np.array([])
    coloumbDist = 2 * cellRad
    for x in frange(-coloumbAmm/2*coloumbDist+coloumbDist/2,coloumbAmm/2*coloumbDist+coloumbDist/2,coloumbDist):
        coloumbPoints = np.append(coloumbPoints,x)
    coloumbPots = np.full(stepCount//numberOfCells,0,dtype='float64')
    for i,e in enumerate(coloumbPoints):
        print("coloumbPot number " + str(i))
        for j,x in enumerate(frange(-cellRad, cellRad+stepSize, stepSize)):
            if (r := abs(e+x)) != 0:
                coloumbPots[j] += cKonst * siliconQ * -qe/ r
            else:
                coloumbPots[j] = min(coloumbPots)
    coloumbPots = capFunc(coloumbPots,(coloumbCap,max(coloumbPots)))
    saveCSV(coloumbPots,'coloumbFunc',direct)
    return coloumbPots

def getColoumbPots():
    if "coloumbFunc.csv" in os.listdir(direct):
        coloumbPots = loadColoumbFunc(direct)
    else:
        coloumbPots = defineColoumbFunc()
    return coloumbPots

def coloumb2Kronig(coloumb,funcCords,numberOfCells,maxI):
    diff = np.full(coloumb.shape[0]-1,0,dtype='float64')
    for i,__ in enumerate(diff):
        diff[i] = (coloumb[i+1]-coloumb[i])/(funcCords[i+1]-funcCords[i])
    vhChangePoints = np.array([], dtype='int16')
    for i,e in enumerate(diff):
        diff[i] = abs(e)
    slopLim = (max(coloumb)-min(coloumb))/(max(funcCords)-min(funcCords))
    for i in range(diff.shape[0]-1):
        if (diff[i+1] <= slopLim and diff[i] >= slopLim) or (diff[i+1] >= slopLim and diff[i] <= slopLim):
            vhChangePoints = np.append(vhChangePoints, i+1)
    if len(vhChangePoints) == 0:
        raise Exception("coloumbCap may be too high?") 
    vertLines = [0,0]
    vertLines[0] = round(statistics.mean(range(vhChangePoints[0],vhChangePoints[1]+1)))
    vertLines[1] = round(statistics.mean(range(vhChangePoints[len(vhChangePoints)-2],vhChangePoints[len(vhChangePoints)-1]+4)))#scuffed

    horLines = [0,0]
    horLines[0] = statistics.mean(coloumb[0:vhChangePoints[0]])
    horLines[1] = statistics.mean(coloumb[vhChangePoints[len(vhChangePoints)-1]:maxI])
    horLine = statistics.mean(horLines)

    minColoumbPot = min(coloumb)
    lenColoumbPot = len(coloumb)
    funcPots = np.zeros(stepCount,dtype='float64')
    for j in range(0,numberOfCells):
        for i,__ in enumerate(funcPots):
            funcPots[i+j*lenColoumbPot] = horLine
        for i in range(vertLines[0],vertLines[1]):
            funcPots[i+j*lenColoumbPot] = minColoumbPot
    return funcPots

def getPot(coloumbPots,funcCords,numberOfCells,maxI):
    if case == "coloumb":
        funcPots = np.tile(coloumbPots,numberOfCells)
    elif case == "kronig":
        funcPots = coloumb2Kronig(coloumbPots,funcCords,numberOfCells,maxI)
    return funcPots

def defineSystem():
    coloumbPots = getColoumbPots()
    funcCords = np.array(frange(-limitDist, limitDist+stepSize, stepSize))
    maxI = funcCords.shape[0]-1
    funcPots = getPot(coloumbPots,funcCords,numberOfCells,maxI)

    #todo fix det her (måske?):
    coloumbPots -= min(funcPots)
    funcPots -= min(funcPots)

    if verbose:
        plt.plot(funcCords,funcPots)
        plt.plot(funcCords,np.tile(coloumbPots,numberOfCells))
        plt.show()
        """if verboseLightMode == False:
            
        else:
            plt.show(block=False)
            try:
                plt.pause(3)
            except:
                pass
            plt.close()"""

    if len(funcPots)!=len(funcCords):
        raise Exception("+1 fejl et sted")
    return funcCords, funcPots, maxI