    """def gausian(self, x,a=1,b=1,c=0):
        funcEnded = False
        gausian = math.exp(-b*(x-c)**2)
        if gausian < 0.01:
            funcEnded = True
        return a*gausian, funcEnded
    
    def pulse(self, x,a=1,b=1,c=0, d=0.25):
        x -= c
        if x < 0:
            return 0, False
        elif x > b:
            return 0, True
        elif x < d:
            return x * (a/d), False
        elif x > b - d:
            h = -a/d
            s = -h*b
            return h*x+s, False
        else:
            return a, False
    
    functionLib = {'1' : gausian}
    
    def functionCaller(self, x, funcID, a, b, c):
        funcID = str(funcID)
        return self.functionLib[funcID](x,a,b,c)"""