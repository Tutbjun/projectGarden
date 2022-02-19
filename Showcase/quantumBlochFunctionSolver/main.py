from functionHandler import *

programMode = "tryAll"

if __name__ == "__main__":
    if programMode == "evalABdependance":
        evalABdependance(kToTry,EToTry)
    if programMode == "tryEk":
        trysol(kToTry,EToTry,AToTry,BToTry)
    if programMode == "tryE":
        tryE(EToTry)
    if programMode == "tryAll":
        tryAll()