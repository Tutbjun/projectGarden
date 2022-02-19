import time
import numpy as np
import keyboard
from matplotlib import pyplot as plt

###########################################bare live-plotting funktioner#####################################################

def defPlot(maxPlotVal,funcCords):
    plt.ion()
    fig = plt.figure(figsize=(21, 12))
    axDiff = fig.add_subplot(111)
    axFunc = fig.add_subplot(111)
    axPots = fig.add_subplot(111)
    tempPlot = np.full(funcCords.shape[0],maxPlotVal)
    tempPlot[0] *= -1
    lineDiff, = axDiff.plot(funcCords[0:len(funcCords)],tempPlot, 'r-')
    lineFunc, = axFunc.plot(funcCords[0:len(funcCords)],tempPlot, 'b-')
    linePots, = axPots.plot(funcCords[0:len(funcCords)],tempPlot, 'g-')
    return fig,lineDiff,lineFunc,linePots

def plot(fig,d,f,lineDiff,lineFunc,linePots,maxPlotVal,plotUndefined, funcPots):
    lineDiff.set_ydata(d)
    lineFunc.set_ydata(f)
    global verbose

    linePots.set_ydata(funcPots[0:len(funcPots)])
    try:
        fig.canvas.draw()
    except:
        if keyboard.is_pressed(['ctrl','shift']):
            verbose = False
            time.sleep(1)

    f = np.absolute(f)
    d = np.absolute(d)
    if max(f) > maxPlotVal or max(d) > maxPlotVal:
        maxPlotVal*=3
        plotUndefined = True
        plt.close(fig='all')
    plt.pause(0.001)
    return maxPlotVal, plotUndefined