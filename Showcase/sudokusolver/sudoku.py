from copy import deepcopy

width = 0
height = 0
boxwidth = 0
boxheight = 0

def getRow(h):
    row = []
    for i in range(width):
        val = input(f"værdi af h{h};w{i}: ")
        if val != '':
            row.append([int(val)])
        else:
            row.append([])
    return row

def getSoduku():
    global width
    global height
    global boxwidth
    global boxheight
    width = int(input("input width: "))
    height = int(input("input height: "))
    boxwidth = int(input("input boxwidth: "))
    boxheight = int(input("input boxheight: "))
    soduku = []
    for i in range(height):
        soduku.append(getRow(i))
    return soduku

def findPossible(soduku):
    solved = True
    progressMade = False
    unsolvable = False
    for i,r in enumerate(soduku):
        if unsolvable:
            break
        for j,c in enumerate(r):
            if len(c) != 1:
                startLength = len(c)
                c = list(range(1,boxheight*boxwidth+1))
                for iMark in range(height):
                    if iMark != i and len(soduku[iMark][j]) == 1:
                        c = [e for e in c if soduku[iMark][j][0] != e]
                for jMark in range(width):
                    if jMark != j and len(soduku[i][jMark]) == 1:
                        c = [e for e in c if soduku[i][jMark][0] != e]
                boxCord = (i-i%boxheight)//boxheight, (j-j%boxwidth)//boxwidth
                for iMark in range(boxCord[0]*boxheight,(boxCord[0]+1)*boxheight):
                    for jMark in range(boxCord[1]*boxwidth,(boxCord[1]+1)*boxwidth):
                        if (jMark != j or iMark != i) and len(soduku[iMark][jMark]) == 1:
                            c = [e for e in c if soduku[iMark][jMark][0] != e]
                soduku[i][j] = c
                if len(c) == 0:
                    unsolvable = True
                    break
                if len(c) != 1:
                    solved = False
                endLength = len(c)
                change = abs(endLength-startLength)
                if change > 0:
                    progressMade = True
    return soduku, solved, progressMade, unsolvable

def solveRoutine(soduku, guessLevel = 1, guessNumber = 1):
    solved = False#for-loop med alle de ikke-umulige løsninger til det dybere niveau
    blindRoad = False
    sodukuOG = deepcopy(soduku)
    def performGuess():
        soduku = deepcopy(sodukuOG)
        guesPerformed = False
        for j in range(width):
            if guesPerformed == True:
                break
            for i in range(height):
                if len(soduku[i][j]) == guessLevel:
                    soduku[i][j] = deepcopy([soduku[i][j][guessNumber-1]])
                    guesPerformed = True
                    break
        return soduku
    if guessLevel > 1:
        soduku = deepcopy(performGuess())
    else:
        soduku, _, _, _ = findPossible(soduku)
        sodukuOG = deepcopy(soduku)
    posibleSols = []
    while solved == False:
        soduku, solved, progressMade, unsolvable = findPossible(soduku)
        if unsolvable:
            if guessNumber >= guessLevel:
                for s in posibleSols:
                    soduku, solved, blindRoad = solveRoutine(s, guessLevel+1, guessNumber = 1)
                    if solved == True:
                        break
                if blindRoad:
                    break
            elif guessNumber < guessLevel:
                guessNumber += 1
                soduku = performGuess()
        if progressMade == False and unsolvable == False:
            posibleSols.append(deepcopy(soduku))
            if guessLevel < 10:
                if guessNumber >= guessLevel:
                    for s in posibleSols:
                        soduku, solved, blindRoad = solveRoutine(s, guessLevel+1, guessNumber = 1)
                        if solved == True:
                            break
                    if blindRoad:
                        break
                elif guessNumber < guessLevel:
                    guessNumber += 1
                    soduku = performGuess()
            else:
                blindRoad = True
                break
    return soduku, solved, blindRoad

def main():
    soduku = getSoduku()
    soduku, _, _ = solveRoutine(soduku)
    print(soduku)

main()