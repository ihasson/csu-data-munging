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

#def mathMajorSankey():

