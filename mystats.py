def summation(ls,f=(lambda x:x)):
    def summ(lx,f):
        if len(lx) == 0:
            return 0
        else : 
            x = lx.pop()
            return f(x) + summ(lx,f)
    return summ(ls.copy(),f)

def mean(ls):
    n = len(ls)
    return summation(ls)/n

#residual sum of squares
#x the variable
#f the predictor function of x
#y the observed value at x
def SSres(lx,ly,f):
    ls = list(zip(lx,ly))
    g = (lambda t:(t[1]-f(t[0]))**2)
    return summation(ls,g)

def cov(lx, ly):
    if len(lx) != len(ly):
        print("Cov(X,Y) cannot be computed due to differing lengths")
        return None
    else:
        n = len(lx)
        ybar = mean(ly)
        xbar = mean(lx)
        ls = list(zip(lx,ly))
        return summation(ls, lambda t:(t[0]-xbar)*(t[1]-ybar)) / (n-1)

def var(lx):
    return cov(lx, lx.copy())

def std_deviation(lx):
    return math.sqrt(var(lx))

def correlation(lx,ly):
    sd_devX = std_deviation(lx)
    sd_devY = std_deviation(ly)
    if sd_devX > 0 and sd_devY >0:
        return cov(lx,ly)/(sd_devX*sd_devY)

def beta(lx,ly):
    return cov(lx,ly)/var(lx)

def alpha(lx,ly):
    return mean(ly) - (beta(lx,ly)*mean(lx))

def SStot(ly):
    ybar = mean(ly)
    return summation(ly, lambda y: (y - ybar)**2)

def rsquared(lx,ly,f):
    return 1 - (SSres(lx,ly,f)/SStot(ly))
