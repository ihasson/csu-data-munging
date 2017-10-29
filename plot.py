from analysis import *
from matplotlib import pylab as pl
from matplotlib import pyplot as plt

def plotGradRates():
    df = graduationRates(DATASET)
    pl.plot(df['four_year_grad_rate'],label='four_year_grad_rate')
    pl.plot(df['six_year_grad_rate'],label='six_year_grad_rate')
    pl.plot(df['grad_rate'],label='all_time_grad_rate')
    pl.legend()
    pl.title('Graduation Rates by First Time Freshman Cohorts')
    pl.show()

### need to redo this one
def plotHSMathGradRates():
    ''' break up the data set 
    '''
    grads_and_nonGrads = partition_cohort_outcome_g12math(DATASET)
    fourYearGrads = and_filter(DATASET,[lambda x:x.fourYearGrad()])
    sixYearGrads = and_filter(DATASET,[lambda x:x.sixYearGrad()])
    fyg = mapOverDct(partitionByCohortYear(fourYearGrads),dct_by_gradelvl_math)
    syg = mapOverDct(partitionByCohortYear(sixYearGrads),dct_by_gradelvl_math)
    fyg = mapOverNestedDct(fyg,len,2)
    syg = mapOverNestedDct(syg,len,2)
    overall = mapOverNestedDct(grads_and_nonGrads,len,3)
    for y in overall:
        if y in fyg:
            overall[y]['4y_grad'] = fyg[y]
        if y in syg:
            overall[y]['6y_grad']=syg[y]
    #return overall
    dfDCT={}
    for k,e in overall.items():
        if '4y_grad' in e:
            df= pd.DataFrame(e).fillna(0)
            df['total']=df['current']+df['drop']+df['grad']
            df['4y grad rate'] = 100*df['4y_grad']/df['total']
            df['6y grad rate'] = 100*df['6y_grad']/df['total']
            df['grad rate'] = 100*df['grad']/df['total']
            df['4y grad rate'].plot(label=k,kind='line')
            dfDCT[k]=df.transpose()
    pl.legend()
    pl.ylim(0,100)
    pl.show()
    return dfDCT

def problemWithData():
    data = rd.read_Progress()
    d = partitionByGraduationYear(data)
    d = mapOverDct(d,len)
    ds = pd.Series(d)
    ds = ds.drop('9999')
    ds = ds.drop('2004')
    plt.plot(ds)
    plt.title('Number of Graduating Students By Year')
    plt.legend('lower left')
    plt.xticks(range(2005,2017))
    plt.show()

def timeToGraduateOfGraduates(data=DATASET):
    graduates = and_filter(data,[lambda x: x.hasGraduated()])
    d1 = partitionByHSMathCategory(data) 
    d2 = mapOverDct(d1,graduationRates2)
   # pl.xticks(range(0,11)) # for some reason this is necessary
                           # probably because matplotlib is dumb 
    for k,v in d2.items():
        v['6ygradrate'] = 100*v['6ygrad']/v['grad']
        v['4ygradrate'] = 100*v['4ygrad']/v['grad']
        v['4ygradrate'].plot(label=k,kind='line')

    pl.legend()
    pl.title("percent of grads who finished in 4 years")
    pl.ylim(0,100)
    pl.show()
    return d2

def timeToGraduateOfCohorts(data=DATASET):
    #graduates = and_filter(data,[lambda x: x.hasGraduated()])
    d1 = partitionByHSMathCategory(data) 
    d2 = mapOverDct(d1,graduationRates1)
   # pl.xticks(range(0,11)) # for some reason this is necessary
                           # probably because matplotlib is dumb 
    for k,v in d2.items():
        v['6ygradrate'] = 100*v['6ygrad']/v['cohort size']
        v['4ygradrate'] = 100*v['4ygrad']/v['cohort size']
        v['4ygradrate'].plot(label=k,kind='line')

    pl.legend()
    pl.title("percent of cohort who finished in 4 years")
    pl.ylim(0,100)
    pl.show()
    return d2

##These two functions might do the same thing.
##
def plotSATDct(dct,title='sat',show=True):
    for cat,d in dct.items():
        l = []
        for score,pop in d.items():
            l.append([int(score),pop])
        l.sort()
        xy = matrixTranspose(l)
        plt.plot(xy[0],xy[1],label=cat)
    plt.legend()
    plt.title=(title)
    if show: plt.show()
def plotSAT(data ,title='None',step=False):
    #satDct = mapOverNestedDct(satanal2(data),len,2)
    #plot = plt.Subplot()
    for cat,d in data.items():
        l = []
        for score,popul in d.items():
            l.append([int(score),popul])
        l.sort()
        x = []
        y = []
        for e in l:
            x.append(e[0])
            y.append(e[1])
        if step:
            plt.step(x,y,label=cat)
        else: plt.plot(x,y,label=cat)
    plt.legend()
    plt.title(title)
    #plt.show()
    return plt

def plotSATG12(dataset=DATASET):
    data = and_filter(dataset,[lambda x: x.hasSAT()])
    satDct = mapOverNestedDct(G12Math_BestSATMath(data),len,2)
    plt = plotSAT(satDct,title='Best SAT Math vs Grade 12 Math',step=True)
    plt.xlabel("SAT Score")
    plt.ylabel("Number of Students")

# need to rethink this one.
def plotSATG11(data=DATASET):
    data = and_filter(data,[lambda x: x.hasSAT()])
    satDct1 = mapOverNestedDct(G11Math_BestSATMath(data),len,2)
    #plot = plt.Subplot()
    #satGradDct = and_filter(data,[lambda x: x.hasGraduated()])
    for cat,d in satDct1.items():
        l = []
        for score,popul in d.items():
            l.append([int(score),popul])
        l.sort()
        x = []
        y = []
        for e in l:
            x.append(e[0])
            y.append(e[1])
        plt.step(x,y,label=cat)
    
    plt.legend()
    plt.title('grade11 Math')
    plt.xlabel("SAT Score")
    plt.ylabel("Number of Students")
    plt.show()

def plotACT(data=DATASET,grdlvl='12',title="",step=False):
    def getACTs(dct): 
        dat = filterDct(lambda x: x != None and len(x) > 0,
            mapOverDct(dct,lambda s: s.getScores2(['ACT','ANY','Math'])))
        return mapOverDct(dat,lambda ls: max(map(lambda v: int(v), ls)))
     
    the_courses = mapOverDct(data, lambda x: [x,x.hsMathCategory(grdlvl)])
    actDct = getACTs(data)
    dct1 = {}
    #want
    #{course:{actScore: number of students who got the score}}
    for k,v in the_courses.items():
        if k in actDct:
            dct1[k] = {"Course": v[1], "actScore": actDct[k]}

    dct2={}
    for k,v in dct1.items():
        if not(v["Course"] in dct2): 
            dct2[v["Course"]] = { x : 0 for x in range(36)}            
        dct2[v["Course"]][v["actScore"]] += 1

    plotSAT(dct2,title=title,step=step)
    plt.xlabel("Math ACT Score")
    plt.ylabel("Number of Students")
    plt.show()
    return dct1,dct2


    #better categorization rules 
    # if only one use old rules 
    # if 1 is good but and the rest unknown/bad use the good one
    # if if multiple good ones not sure what to do

    #ACTs_dct_by_categ = mapOverDct(dataDct,getACTs)
    #return ACTs_dct_by_categ
    #plotSATDct(ACTs_dct_by_categ,title='act')

def betterACTPlot(data,grdlvl):
    dat1 = and_filter(data,[lambda x: x.hasACT()])
    dat2 = first_math2(dat1) 
    dat3 = {}
    for k,b in dat2["ACTvsSAT"].items():
        if b: dat3[k] = data[k]
    #dat4 = first_math2(dat3)
     
    return dat3
    
def plotACT2(data=DATASET,grdlvl='12',title="",step=False):
    def getACTs(dct): 
        dat = filterDct(lambda x: x != None and len(x) > 0,
            mapOverDct(dct,lambda s: s.getScores2(['ACT','ANY','Math'])))
        return mapOverDct(dat,lambda ls: max(map(lambda v: int(v), ls)))
     
    the_courses = mapOverDct(data, lambda x: [x,x.hsMathCategory(grdlvl)])
    actDct = getACTs(data)
    dct1 = {}
    #want
    #{course:{actScore: number of students who got the score}}
    for k,v in the_courses.items():
        if k in actDct:
            dct1[k] = {"Course": v[1], "actScore": actDct[k]}

    dct2={}
    for k,v in dct1.items():
        if not(v["Course"] in dct2): 
            dct2[v["Course"]] = { x : 0 for x in range(36)}            
        dct2[v["Course"]][v["actScore"]] += 1
    df = pd.DataFrame(dct2)
    x = list(range(36))
    y = df.as_matrix()
    ### what was this one for again?


## this is to generate the final plots.
## 
def reportPlots(data=DATASET):
    data05_15 = and_filter(
                DATASET, 
                [   lambda x: int(x.cohort_term)>2055, 
                    lambda x: int(x.cohort_term)<2157])
    a,b = plotACT(data05_15, grdlvl='12',title="Math ACT vs grade 12 Math")
    plotACT(data05_15, grdlvl='11',title="Math ACT vs grade 11 Math")
    plotSATG12(data05_15)
    plt.show()
    plotSATG11(data05_15)
    plt.show()
    ## need to revise the below.
    #df.boxplot(column='SAT_math',by='GRD11Math')
