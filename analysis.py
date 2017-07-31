from set_operations import *
import pickle

DATASET = rd.load_data()

def read_filter_match_FTF_ONLY():
    d = filter_has_hs_and_college(readall())
    hs = and_filter(d,[lambda x: x.cohort_type == 'FTF'])
    return set_hs_course_labels(hs)

def gpa_freshmen_by_year_retention(data):
    d = partitionByRetention(data) 
    d2 = mapOverDct(d,lambda x: startYear(x))
    d3 = mapOverDct(d2,lambda x: mapOverDct(x,lambda y: stlstToDct(y)))
    d4 = mapOverDct(d3,groupGPA)
    return pd.DataFrame(d4)

# the explanation for why my data had more people was that it did not filter out
# transfer students?
def graduation_by_incoming_year(dataSet) -> "could be freshmen or transfer":
    ret = partitionByRetention(dataSet)
    ret_sty=mapOverDct(ret,lambda x: startYear(x))
    d = mapOverDct(ret_sty, lambda x:mapOverDct(x,lambda y: len(y)))
    df = pd.DataFrame(d) 
    
   # df = pd.DataFrame(col,columns=['current','dropout','grad'],index=yr)
    #df = df.drop(['2016','2015','2014'])
    df['total'] = df.sum(axis=1)
    df['ret_rate'] = 100*(df['current']+df['grad'])/df['total']
    df['grad_rate'] = 100*df['grad']/df['total']
    df['drop_rate'] = 100*df['drop']/df['total']
    df['current_rate'] = 100*df['current']/df['total']
    return df

# figure out why cohort term differs from start term

def weird_start(dataSet):
    d = and_filter(dataSet,[lambda x: int(x.cohort_term) - int(x.first_term)>10])
    return d

def course_cohort_outcome(dataSet):
    d = mapOverDct(dct_by_gradelvl_math(dataSet),
            lambda x:partitionByCohortYear(x,lambda y: y.cohort_type=='FTF'))
    d2 = {}
    for k,e in d.items():
        d2[k] = mapOverDct(e,partitionByRetention)
    return d2

## what was this for again?
def studentToDct(stdnt):
    return {'start_term': stdnt.cohort_term, 'last_term': stdnt.last_term, 
            'grad':stdnt.hasGraduated()}

# Don't use until fixed.
# doesn't tell me anything
def correlate12gMwGrad(dataSet):
    hs = and_filter(dataSet,[lambda x: x.cohort_type == 'FTF'])
    #crs = mapOverDct(partitionBylastHSMath(hs),
    #        lambda x:mapOverDct(x,lambda: ) # not sure what happened here
    outcomes = mapOverDct(hs,studentToDct)  # but need to fix before using.
    df1 = pd.DataFrame(crs)
    df1 = df1.transpose()
    df2 = pd.DataFrame(outcomes)
    df2 = df2.transpose()
    df1 = df1.applymap(lambda x: 1 if x == 1 else 0)
    df=df1.join(df2['grad'].map(lambda x: 1 if x else 0))
    return df

def partition_cohort_outcome_g12math(dataSet):
    cohorts = partitionByCohortYear(dataSet)
    coho_reten = mapOverDct(cohorts,partitionByRetention)
    return mapOverNestedDct(coho_reten,partitionBylastHSMath,2)

def partition_g12math_timeToGrad(dataSet):
    d = and_filter(dataSet,[lambda x: x.grad_term != '9999'])
    d1 = partitionBylastHSMath(d)
    d2 = mapOverNestedDct(d1,lambda x: x.number_of_terms(),2)
    return d2

def fullResultsTablesBy_g12Math(dataSet):
    p = partitionBylastHSMath(dataSet)
    d = mapOverNestedDct(p,lambda x: x.results(),2)
    dfDCT = {}
    for key,data in d.items(): 
        dfDCT[key] = pd.DataFrame(data).transpose().fillna(0.0)
    return dfDCT

## 4-year,6-year,all-time, graduation rates
def graduationRates(dataSet):
    
    fourYear = startYear(
            and_filter(dataSet,[lambda x: x.fourYearGrad()]))
    fourYear = mapOverDct(fourYear,len)
    sixYear = startYear(
            and_filter(dataSet,[lambda x: x.sixYearGrad()]))
    sixYear = mapOverDct(sixYear,len)
        
    ret = partitionByRetention(dataSet)
    ret_sty=mapOverDct(ret,lambda x: startYear(x))
    d = mapOverDct(ret_sty, lambda x:mapOverDct(x,lambda y: len(y)))
    df = pd.DataFrame(d) 
    df['total'] = df.sum(axis=1)
    fourandsix = pd.DataFrame({'four_year':fourYear,'six_year':sixYear})
    df = df.join(fourandsix)
    df['ret_rate'] = 100*(df['current']+df['grad'])/df['total']
    df['drop_rate'] = 100*df['drop']/df['total']
    df['current_rate'] = 100*df['current']/df['total']
    df['grad_rate'] = 100*df['grad']/df['total']
    df['six_year_grad_rate'] = 100*df['six_year']/df['total']
    df['four_year_grad_rate'] = 100*df['four_year']/df['total']
    df = df.drop(['2003','2013']) #,'2014','2015','2016'])
    return df

#def timetogradanal(data):
#    results = {}
#    for mc,time in data.itmes():
#        if mc in results:
#            for sids,time in 

# both of these need improvement
# the standard deviation formula
# sigma^2 = E[(X - mu)^2]
def meanDct(dataSet):
    accum = 0
    size = len(dataSet)
    for key,e in dataSet.items():
        accum += e
    return (accum/size)

# 
def varDct(dataSet):
    accum = 0
    mu = meanDct(dataSet)
    size = len(dataSet)
    for k,e in dataSet.items():
        accum+= (e - mu)**2
    return (accum/size)

# correlation coeff.
#def rho()

## 4-year,6-year,all-time, graduation rates
def graduationRates2(dataSet):
    data = and_filter(dataSet,[lambda x: x.hasGraduated()])
    fourYear = partitionByGraduationYear(
            and_filter(data,[lambda x: x.fourYearGrad()]))
    fourYear = mapOverDct(fourYear,len)
    sixYear = partitionByGraduationYear(
            and_filter(data,[lambda x: x.sixYearGrad()]))
    sixYear = mapOverDct(sixYear,len)
    graduated = mapOverDct(partitionByGraduationYear(data),len)
    df = pd.DataFrame({'4ygrad':fourYear,'6ygrad':sixYear,'grad':graduated})

    return df
