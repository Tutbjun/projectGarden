from systemDefiner import *
from qFunction import *
import keyboard
import mpmath
from livePlotter import *
import sympy

kToTry = 0.171255
EToTry = 0.855*11.19810654216253*2
AToTry = 10
BToTry = 10

funcCords, funcPots, maxI = defineSystem()

###########################################løser et step i funktionen#####################################################

def solPart(dirr,pos,i,E,k,A,B,prevF,prevD):
    B = calcB(prevF,E,funcPots[i],k,prevD,pos)
    A = calcA(prevF,E,funcPots[i],k,prevD,pos)
    f = calcFuncVal(pos+stepSize*dirr,E,funcPots[i],k,A,B)
    d = calcDiffVal(pos+stepSize*dirr,E,funcPots[i],k,A,B)
    return f,d,B,A

###########################################finder funktion givet k- og E-værdier hvor grænsekontinuerlighed er ligegyldigt#####################################################

def trysol(k,E,A0,B0):
    global verbose
    
    f = np.full(len(range(0,maxI+1)),0,dtype='complex128')
    d = np.copy(f)
    paramAs = np.copy(f)
    paramBs = np.copy(paramAs)


    startPoint = (maxI)//2
    paramAs[startPoint] = A0
    paramBs[startPoint] = B0

    f[startPoint] = calcFuncVal(0,E,funcPots[startPoint],k,A0,B0)
    d[startPoint] = calcDiffVal(0,E,funcPots[startPoint],k,A0,B0)
    
    plotUndefined = True
    maxPlotVal = 1
    
    for i in range(1,startPoint+1):
        pos = stepSize*i
        normI = startPoint+i
        f[normI],d[normI],paramBs[normI],paramAs[normI] = solPart(1,pos,normI,E,k,paramAs[normI-1],paramBs[normI-1],f[normI-1],d[normI-1])
        invI = startPoint-i
        f[invI],d[invI],paramBs[invI],paramAs[invI] = solPart(-1,-pos,invI,E,k,paramAs[(invI)+1],paramBs[(invI)+1],f[invI+1],d[invI+1])

        if verbose == True:
            if plotUndefined:
                if (maxVal := max(np.absolute(f))) > maxPlotVal: 
                    maxPlotVal = maxVal
                fig,lineDiff,lineFunc,linePots = defPlot(maxPlotVal,funcCords)
                plotUndefined = False
            imagF = np.full(f.shape,0,dtype='float64')
            for i,__ in enumerate(f):
                imagF[i] = f[i].imag
            maxPlotVal, plotUndefined = plot(fig,imagF,f.astype('float64'),lineDiff,lineFunc,linePots,maxPlotVal,plotUndefined,funcPots)
        elif keyboard.is_pressed(['ctrl','shift']) and len(plt.get_fignums()) == 0:
            verbose = True
            plotUndefined = True
            time.sleep(1)

    """if verboseLightMode == True and verbose == True:
        try:
            plt.pause(5)
        except:
            pass
        plt.close()"""
    while len(plt.get_fignums())>0:
        try:
            plt.pause(1)
        except:
            pass
    return f,d

###########################################ignorer den her, den bliver kun brugt hvis du siger den skal#####################################################

def evalABdependance(k,E):
    cofStep = 0.05
    maxTestVal = 10
    arraySize = round(maxTestVal/cofStep+1)
    scores = np.full((arraySize,arraySize),0,dtype='float64')
    cofRange = frange(0,maxTestVal+cofStep,cofStep)
    for i,A in enumerate(cofRange):
        print(f"trying with A = {A}")
        for j,B in enumerate(cofRange):
            __,scores[i,j] = trysol(k,E,A,B)

    file = open(direct + "/ABdepend.csv","w+")
    file.close()
    np.savetxt(direct + "/ABdepend.csv",scores,delimiter=",", fmt='%f')

    x = cofRange
    y = cofRange
    hf = plt.figure()
    ha = hf.add_subplot(111,projection='3d')
    X, Y = np.meshgrid(x,y)
    ha.plot_surface(X,Y,scores)
    plt.show()

###########################################givet E og k finder den funktionerne med B0=1,A0=0 og B0=0,A0=1#####################################################

def tryk(k,E):
    fA,dA = trysol(k,E,1,0)
    fB,dB = trysol(k,E,0,1)
    return fA,dA,fB,dB

###########################################givet E finder den en løsning for k hvor grænserne går op til 0 (nogle gange uløselig)#####################################################

def tryE(E):
    if E == 0:
        E += 0.00000001
    kRad = math.pi/cellRad*2
    kStep = 2*kRad / 200#
    kRange = frange(-kRad,kRad+kStep,kStep)
    wA = np.full(len(kRange),0,dtype='complex128')
    wB = np.full(len(kRange),0,dtype='complex128')
    wdA = np.full(len(kRange),0,dtype='complex128')
    wdB = np.full(len(kRange),0,dtype='complex128')
    for i,k in enumerate(kRange):
        print(f"calculating at k={k}")
        fA,dA,fB,dB = tryk(k,E)
        wA[i] = fA[0]-fA[len(fA)-1]
        wB[i] = fB[0]-fB[len(fB)-1]
        wdA[i] = dA[0]-dA[len(dA)-1]
        wdB[i] = dB[0]-dB[len(dB)-1]
    fitwA = np.polyfit(kRange, wA, 10)
    fitwB = np.polyfit(kRange, wB, 10)
    fitwdA = np.polyfit(kRange, wdA, 10)
    fitwdB = np.polyfit(kRange, wdB, 10)
    kRange = frange(-kRad,kRad+kStep,kStep/100)
    #plt.plot(kRange, np.poly1d(fitwA)(kRange))
    #plt.plot(kRange, np.poly1d(fitwB)(kRange))
    #plt.plot(kRange, np.poly1d(fitwdA)(kRange))
    #plt.plot(kRange, np.poly1d(fitwdB)(kRange))
    #plt.show()
    k = sympy.Symbol('k')
    pol1 = sympy.expand(0)
    for i,c in enumerate(fitwA):
        pol1 += sympy.expand(c*k**i)
    pol2 = sympy.expand(0)
    for i,c in enumerate(fitwB):
        pol2 += sympy.expand(c*k**i)
    pol3 = sympy.expand(0)
    for i,c in enumerate(fitwdA):
        pol3 += sympy.expand(c*k**i)
    pol4 = sympy.expand(0)
    for i,c in enumerate(fitwdB):
        pol4 += sympy.expand(c*k**i)
    M = sympy.Matrix([[pol1,pol2],[pol3,pol4]])
    det = M.det()
    maxPower = 0
    for e in det.args:
        for f in e.args:
            if 'k' in str(f):
                comps = str(f).split('*')
                lastComp = comps[len(comps)-1]
                if is_number(lastComp) == False:
                    if 1 > maxPower:
                        maxPower = 1
                elif (val:=int(lastComp)) > maxPower:
                    maxPower = val
    cofs = np.full(maxPower+1,0,dtype='complex128')
    I = mpmath.mp.mpc(0, 1)
    for e in det.args:
        val = mpmath.mpmathify(0)
        power = 0
        if len(e.args) == 0:
            val += mpmath.mpmathify(e)
            power = 0
        elif len(e.args) == 2:
            if str(type(e.args[1])) != "<class 'sympy.core.numbers.ImaginaryUnit'>":
                val += mpmath.mpmathify(e.args[0])
                comps = str(e.args[1]).split('*')
                if comps[-1] != 'k':
                    power = int(comps[-1])
                else:
                    power = 1
            else:
                val += mpmath.mpmathify(e.args[0])*I
                power = 0
        else:
            val += mpmath.mpmathify(e.args[0])*I
            comps = str(e.args[2]).split('*')
            if comps[-1] != 'k':
                power = int(comps[-1])
            else:
                power = 1
        cofs[-power-1] += complex(val)
    kSolves = []
    try:
        kSolves = mpmath.polyroots(cofs,maxsteps=500)
    except:
        print(f"no sollutions found at E={E}")
    tbd = np.array([],dtype='int32')
    for i,__ in enumerate(kSolves):
        kSolves[i] = complex(kSolves[i])
        if abs(kSolves[i].imag) > abs(kSolves[i].real/100) or abs(kSolves[i]) > max(kRange) or kSolves[i] != kSolves[i]:
            tbd = np.append(tbd,i)
    for i in range(len(tbd)-1,-1,-1):
        kSolves = np.delete(kSolves,tbd[i])
    ksnScors = np.full((len(kSolves),2),0,dtype='complex128')
    if len(kSolves) > 0:
        ksnScors[0:ksnScors.shape[0],0] = kSolves
        for i,__ in enumerate(ksnScors):
            print(f"checking solution at k={kSolves[i]}")
            fA,dA,fB,dB = tryk(kSolves[i].real,E)
            wA = fA[0]-fA[len(fA)-1]
            wB = fB[0]-fB[len(fB)-1]
            wdA = dA[0]-dA[len(dA)-1]
            wdB = dB[0]-dB[len(dB)-1]
            checkScalar = -wA/wB
            checkVal = wdA + checkScalar*wdB
            ksnScors[i,1] = abs(checkVal)/math.sqrt(max(np.absolute(fA))+max(np.absolute(fB)))
    return ksnScors

###########################################gemmer til E/k-diagram#####################################################
def saveEkCords(cords,scores):
    file = open(direct + "/results.csv","w+")
    file.close()
    np.savetxt(direct + "/results.csv",cords,delimiter=",", fmt='%f')
    file = open(direct + "/resultScores.csv","w+")
    file.close()
    np.savetxt(direct + "/resultScores.csv",scores, fmt='%f')

###########################################overordnet funktion der går gennem hele E-rangen for at finde k-løsninger#####################################################

def tryAll():
    ERangeRad = 0.5
    maxE = ERangeRad*max(funcPots)
    minE = 0
    Estep = (maxE-minE)/100
    EsToTry = frange(minE,maxE,Estep)
    if 0 in EsToTry:
        print("warning, divission with zero will most likely happen. changing E variable...")
    Ekcords = np.full((1,2),0,dtype='float64')
    Ekscores = np.full(1,0,dtype='float64')
    for E in EsToTry:
        print(f"attempting solution with E={E/max(funcPots)}")
        validksnScors = np.real(tryE(E))
        for e in validksnScors:
            Ekcords = np.append(Ekcords,[[e[0],E/max(funcPots)]], axis=0)
            Ekscores = np.append(Ekscores,e[1])
        saveEkCords(Ekcords,Ekscores)
    Ekcords = np.delete(Ekcords,0,axis=0)
    Ekscores = np.delete(Ekscores,0)
    saveEkCords(Ekcords,Ekscores)