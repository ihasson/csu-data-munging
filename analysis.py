from set_operations import *
#import pickle
import pandas as pd
import load

DATASET = load.loadFTF()

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
def graduationRates1(dataSet):
    """By Cohort year
    """
    data = and_filter(dataSet,[lambda x: x.hasGraduated()])
    fourYear = startYear(
            and_filter(data,[lambda x: x.fourYearGrad()]))
    fourYear = mapOverDct(fourYear,len)
    sixYear = startYear(
            and_filter(data,[lambda x: x.sixYearGrad()]))
    sixYear = mapOverDct(sixYear,len)
    graduated = mapOverDct(startYear(data),len)
    everyone = mapOverDct(startYear(dataSet),len)
    df = pd.DataFrame({'4ygrad':fourYear,'6ygrad':sixYear,'grad':graduated,
        'cohort size':everyone})

    return df

## 4-year,6-year,all-time, graduation rates
def graduationRates2(dataSet):
    """ by gad year """
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

##
def droppedOut(dct):
    outcomes={}
    for cat in dct:
        dropout=cat+'_dropout'
        current=cat+'_current'
        grad=cat+'_grad'
        rate=cat+'_dropout_rate'
        outcomes[dropout] = 0
        outcomes[current] = 0
        outcomes[grad] = 0
        for st in dct[cat]:
            grad_term = int(st.grad_term)
            last_term = int(st.last_term)
            current_term = 2167
            #grad := gradterm != 9999
            #inprogress := gradterm == 9999 and current - last term < 10
            #drop out otherwise
            if grad_term != 9999:
                outcomes[grad] += 1
            elif (current_term - last_term) < 10:
                outcomes[current] += 1
            else:
                outcomes[dropout] += 1
        outcomes[rate] = (outcomes[dropout] / 
                (outcomes[dropout]+outcomes[current]+outcomes[grad]))
        outcomes[cat+'_total'] = len(dct[cat])
    return outcomes


## Takes a dictionary of lists as input. Returns what the key implies in
#   terms of passing or failing or failing the first math course.
#   
def compute_first_course_grades(dct):
    pfg={}
    for cat in dct:
        p=cat+'_pass'
        f=cat+'_fail'
        pfg[p] = 0
        pfg[f] = 0
        for st in dct[cat]:
            st.collegeSeq.sort()
            if st.collegeSeq[0][3] in gradesMap: 
                if gradesMap[st.collegeSeq[0][3]] >= 2.0:
                    pfg[p] += 1
                else: 
                    pfg[f] += 1
            else:
                print("WARNING  " +st.collegeSeq[0][3]+ "  not a grade")
                print(st.sid)
            ratio=cat+'_fail_rate'
            pfg[ratio] = (pfg[f]/(pfg[f]+pfg[p]))
    return pfg

## not sure what to name this it returns results about how courses were labeled
def f(dct):
    matched = {}
    matchedLabel = {}
    notMatched = {}
    for st in dct:
        for hsc in dct[st].hsCourses:
            if hsc.course_label == 'unknown':
                if hsc.descr in notMatched:
                    notMatched[hsc.descr] += 1
                else: 
                    notMatched[hsc.descr] = 1
            else: 
                if hsc.course_label in matchedLabel:
                    if hsc.descr in matchedLabel[hsc.course_label]:
                        matchedLabel[hsc.course_label][hsc.descr] += 1
                    else:
                        matchedLabel[hsc.course_label][hsc.descr] = 1
                else:
                    matchedLabel[hsc.course_label] = {hsc.descr: 1}
                if hsc.descr in matched:
                    matched[hsc.descr] += 1
                else: 
                    matched[hsc.descr] = 1
    return matched,notMatched,matchedLabel

def makeDf(data):
    clmns = ['first_term','last_term','grad_term','lastHsCourse']
    rowlist = []
    for e in data:
        lasthsc='placeholder' 
        row = [data[e].first_term, data[e].last_term,data[e].grad_term,lasthsc]
        rowlist.append(row)
    df = pd.DataFrame(rowlist,columns=clmns) 
    return df

def makecourseMatrix(dataSet):
    matrixDct = {}
    for k,s in dataSet.items():
        matrixDct[k] = {}
        for coursename in s.ccDict:
            matrixDct[k][coursename] = s.has_passed(coursename)
        if s.hasGraduated():
            matrixDct[k]['grad'] = 1
        else: 
            matrixDct[k]['grad'] = 0
        matrixDct[k]['last_term'] = int(s.last_term)
    return np.DataFrame(matrixDct).fillna(0)

def lastHS_FirstMath(dataSet):
    #lastMath = partitionBylastHSMath(dataSet)
    lastMath = mapOverNestedDct(dataSet,lambda x: x.first_math(),2)
    def something(indct):
        outdct={}
        for k,cname in indct.items():
            if cname in outdct:
                outdct[cname] += 1
            else: 
                outdct[cname] = 1
        return outdct
    return mapOverDct(lastMath,something)

def lastHS_OtherThing(dataSet,fn=lambda x: x.first_math()):
    #lastMath = partitionBylastHSMath(dataSet)
    lastMath = mapOverNestedDct(dataSet,fn,2)
    def something(indct):
        outdct={}
        for k,cname in indct.items():
            if cname in outdct:
                outdct[cname] += 1
            else: 
                outdct[cname] = 1
        return outdct
    return mapOverDct(lastMath,something)

#def Math_SAT_ANAL(dataSet):
#    tookSat = and_filter(dataSet,[lambda x: x.bestSATMath() != None])
#    avgMathByCat = {}
#    byCat = partitionByHSMathCategory(dataSet)
#    satByCat = mapOverNestedDct(byCat,lambda x: x.bestSATMath(),2)
#    avgMathByCat['all'] = mapOverDct(satByCat,lambda x: sum(x.values())/len(x))
#    grad_only = and_filter(tookSat,[lambda x: x.hasGraduated()])
#    no_grad = and_filter(tookSat,[lambda x: not(x.hasGraduated())])
#    byCat_grad_only = partitionByHSMathCategory(grad_only)
#    byCat_no_grad = partitionByHSMathCategory(no_grad)
#    sat_grad= mapOverNestedDct(byCat_grad_only,lambda x: x.bestSATMath(),2)
#    sat_no_grad =mapOverNestedDct(byCat_grad_only,lambda x: x.bestSATMath(),2)
#    avgMathByCat['grad'] = mapOverDct(sat_grad,lambda x: sum(x.values())/len(x),2)
#    avgMathByCat['non grad'] = mapOverDct(sat_no_grad,lambda x: sum(x.values())/len(x),2)
#    return avgMathByCat
#
def mathsatanal(dataset):
    tookSat = and_filter(
            DATASET,
            [lambda x: x.bestSATMath() != None])

    mapOverDct(
            mapOverNestedDct(
                partitionByHSMathCategory(tookSat),
                lambda x: x.bestSATMath(),2),
            lambda y: sum(y.values())/len(y))
def satanal(dataset):
    tookSat = and_filter(
            DATASET,
            [lambda x: x.bestSATComposite() != 0])

    mapOverDct(
            mapOverNestedDct(
                partitionByHSMathCategory(tookSat),
                lambda x: x.bestSATComposite(),2),
            lambda y: sum(y.values())/len(y))

def G12Math_BestSATMath(dataset):
    tookSat = and_filter(dataset, [lambda x: x.bestSATMath() != None,
        lambda x: int.__mod__(x.bestSATMath(),10) == 0])
    fun = lambda x: partitionStudents(x,lambda x: str(x.bestSATMath()))
    a = mapOverNestedDct(partitionByHSMathCategory(tookSat),fun,1)
    return a

def G12Math_SomeSATMath(dataset):
    tookSat = and_filter(dataset, [lambda x: x.sat_math != None,
        lambda x: int.__mod__(x.sat_math,10) == 0])
    fun = lambda x: partitionStudents(x,lambda x: str(x.sat_math))
    a = mapOverNestedDct(partitionByHSMathCategory(tookSat),fun,1)
    return a


def G11Math_BestSATMath(dataset):
    tookSat = and_filter(dataset, [lambda x: x.bestSATMath() != None,
        lambda x: int.__mod__(x.bestSATMath(),10) == 0])
    fun = lambda x: partitionStudents(x,lambda x: str(x.bestSATMath()))
    a = mapOverNestedDct(partitionByHSMathCategory(tookSat,gradelvl='11'),fun,1)
    return a

def satMathGradRate(dataset):
    tookSat = and_filter(dataset, [lambda x: x.bestSATMath() != None,
        lambda x: int.__mod__(x.bestSATMath(),10) == 0])
    def grad(y): 
        if y.hasGraduated():
            return "T"
        else:
            return "F"
    fun = lambda x: partitionStudents(x,
            lambda y: grad(y) )
    a = mapOverDct(partitionStudents(tookSat,lambda x: str(x.bestSATMath())),fun)
    b = mapOverNestedDct(a,len,2)
    def ratio(y):
        if 'T' in y:
            if 'F' in y:
                return y['T']/(y['T']+y['F'])
            else: return 1.0
        else:
            if 'F' in y:
                return 0.0
            else:
                return -1.0

    return mapOverDct(b,ratio)

def satGradRate(dataset):
    tookSat = and_filter(dataset, [lambda x: x.bestSATComposite() != 0,
        lambda x: int.__mod__(x.bestSATComposite(),10) == 0])
    def grad(y): 
        if y.hasGraduated():
            return "T"
        else:
            return "F"
    fun = lambda x: partitionStudents(x,
            lambda y: grad(y) )
    a = mapOverDct(partitionStudents(tookSat,lambda x: str(x.bestSATComposite())),fun)
    b = mapOverNestedDct(a,len,2)
    def ratio(y):
        if 'T' in y:
            if 'F' in y:
                return y['T']/(y['T']+y['F'])
            else: return 1.0
        else:
            if 'F' in y:
                return 0.0
            else:
                return -1.0

    return mapOverDct(b,ratio)

def satanal4(dataset):
    tookSat = and_filter(dataset, [lambda x: x.bestSATMath() != None,
        lambda x: int.__mod__(x.bestSATMath(),10) == 0])
    d1 = partitionByHSMathCategory(tookSat)
    def satandgrad(stdnt):
        g = -1
        if stdnt.hasGraduated(): g = 1
        return {'sat': stdnt.bestSATMath(), 'grad': g}
    return mapOverDct(d1,lambda x: mapOverDct(x,satandgrad))

def sat_first_math(dataset):
    data = and_filter(dataset,[lambda x: (x.hasSAT() and 
                                (x.first_math_course() != None))])
    d1={
        "first_math":{k:s.first_math() for k,s in data.items()},
        "first_math_grade":
            {k:s.first_math_course().grade_val for k,s in data.items()},
        "grade_letter":
            {k:s.first_math_course().grade_letter for k,s in data.items()},
        "SAT_math":{k:s.bestSATMath() for k,s in data.items()}
        }
    return d1
def test_first_math(dataset):
    data = and_filter(dataset,[lambda x: (x.hasSAT() and 
                                (x.first_math_course() != None)),
                                lambda x: x.hasELM()])
    d1={
        "first_math":{k:s.first_math() for k,s in data.items()},
        "first_math_grade":
            {k:s.first_math_course().grade_val for k,s in data.items()},
        "grade_letter":
            {k:s.first_math_course().grade_letter for k,s in data.items()},
        "SAT_math":{k:s.bestSATMath() for k,s in data.items()},
        "ELM":{k:s.bestELM() for k,s in data.items()}
        #"SAT_CR":{k:s.best
        }
    return d1
def first_math(dataset):
    data = and_filter(dataset, [lambda x: x.first_math_course() != None,
        lambda x: x.hasExams()])
    def cutoff(n,m,s):
        try:
            if m<=n: return None
            else: return m
        except:
            print(s.sid)
    d1={
        "first_math":{k:s.first_math() for k,s in data.items()},
        "first_math_grade":
            {k:s.first_math_course().grade_val for k,s in data.items()},
        "grade_letter":
            {k:s.first_math_course().grade_letter for k,s in data.items()},
        "SAT_math":{k:cutoff(-1,s.bestSATMath(),s) for k,s in data.items()},
        "ELM":{k:s.bestELM() for k,s in data.items()},
        #"SAT_Composite":{k:cutoff(-1,s.bestSATComposite(),s) 
        #    for k,s in data.items()},
        "MPT1":{k:s.getBestScore('MPT1') for k,s in data.items()},
        "MPT2":{k:s.getBestScore('MPT2') for k,s in data.items()},
        "grad?":{k:s.hasGraduated() for k,s in data.items()},
        "term_count":{k:s.number_of_terms() for k,s in data.items()},
        "time_to_grad":{k:cutoff(-1,s.time_to_grad(),s) for k,s in data.items()},
        "ACT":{k:s.getACTMath() for k,s in data.items()},
        "GRD11Math":{k:s.hsMathCategory('11') for k,s in data.items()},
        "GRD12Math":{k:s.hsMathCategory('12') for k,s in data.items()},
        "HSMATHgpa":{k:s.hsGPA() for k,s in data.items()},
        "ACTvsSAT":{k:s.ACTBetterThanSAT() for k,s in data.items()}
        }
    return d1

def first_math2(dataset):
    data = and_filter(dataset, [lambda x: x.first_math_course() != None,
        lambda x: x.hasExams()])
    def cutoff(n,m,s):
        try:
            if m<=n: return None
            else: return m
        except:
            print(s.sid)
    d1={
        #"first_math":{k:s.first_math() for k,s in data.items()},
        #"first_math_grade":
        #    {k:s.first_math_course().grade_val for k,s in data.items()},
        #"grade_letter":
        #    {k:s.first_math_course().grade_letter for k,s in data.items()},
        "SAT_math":{k:cutoff(-1,s.bestSATMath(),s) for k,s in data.items()},
        "ELM":{k:s.bestELM() for k,s in data.items()},
        #"SAT_Composite":{k:cutoff(-1,s.bestSATComposite(),s) 
        #    for k,s in data.items()},
        "MPT1":{k:s.getBestScore('MPT1') for k,s in data.items()},
        "MPT2":{k:s.getBestScore('MPT2') for k,s in data.items()},
        "grad?":{k:s.hasGraduated() for k,s in data.items()},
        "term_count":{k:s.number_of_terms() for k,s in data.items()},
        "time_to_grad":{k:cutoff(-1,s.time_to_grad(),s) for k,s in data.items()},
        "ACT":{k:s.getACTMath() for k,s in data.items()},
        "GRD11Math":{k:s.hsMathCategory('11') for k,s in data.items()},
        "GRD12Math":{k:s.hsMathCategory('12') for k,s in data.items()},
        "ACTvsSAT":{k:s.ACTBetterThanSAT() for k,s in data.items()}
        }
    return d1

def makingsomeboxplots(data=DATASET):
    d = mapOverDct(
            partitionByHSMathCategory(data),
            [lambda x: pd.DataFrame(first_math(x))])
    return d
