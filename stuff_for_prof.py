from analysis import *
from matplotlib import pyplot as plt
#import transitionMatrix as tm
import re
#from set_operations import *

#fixing the transition matrix.
def sankey():
    dct = mapOverDct(partitionByHSMathCategory(DATASET), 
            lambda hsc: partitionStudents(hsc, lambda x: x.first_math()))
    dct = mapOverNestedDct(dct,len,2)
    transitions = [(i,k) for k,i in dct['Calculus Prep'].items()]
    transitions.sort()
    lines = []
    for e in transitions:
        lines.append('Calculus Prep'+'['+str(e[0])+']_'+e[1]+'\n')
    f = open('transitions.txt','w')
    f.writelines(lines)
    f.close()
    return transitions

def something():
    dat = partitionByHSMathCategory(DATASET,gradelvl='12')
    dct = mapOverDct(partitionByHSMathCategory(dat['No Math'],gradelvl='11'), 
            lambda hsc: partitionStudents(hsc, lambda x: x.first_math()))
    dct = mapOverNestedDct(dct,len,2)
    def transit_sankey(subject,dct):
        transitions = [(i,k) for k,i in dct[subject].items()]

        transitions.sort()
        lines = []
        for e in transitions:
            lines.append(subject+'['+str(e[0])+']_'+e[1]+'\n')
        f = open('transitions/' + subject + '_transitions.txt','w')
        f.writelines(lines)
        f.close()
        #return transitions
    for subj in dct.keys():
        transit_sankey(subj,dct)

def took_college_alg_in_hs():
    took_c_alg= {}
    for k,s in DATASET.items():
        for hscs in s.hsCourses:
            if re.search("college algebra", hscs.descr, re.IGNORECASE):
                took_c_alg[k]= s
    return took_c_alg

def took_AP_Calc():
    took_Calc = {}
#    took_Calc = {'AB':{},'BC':{},'Neither':{}}
    for k,s in DATASET.items():
        for hscs in s.hsCourses:
            if (re.search("AP", hscs.descr, re.IGNORECASE) and
                hscs.course_label == 'calculus'):
                    took_Calc[k] = s
    return took_Calc

def took_AP_Stats():
    took_Stats= {}
    
    for k,s in DATASET.items():
        for hscs in s.hsCourses:
            if (re.search("AP", hscs.descr, re.IGNORECASE) and
                hscs.course_label == 'stats'):
                    took_Stats[k] = s
    return took_Stats

def took_IB():
    took_IB = {}
    for k,s in DATASET.items():
        for hscs in s.hsCourses:
            if (re.search("IB", hscs.descr, re.IGNORECASE) and
                re.search("SL", hscs.descr, re.IGNORECASE)):
                took_IB[k]=hscs.descr
    return took_IB

def getAPMathStuff():
    apMath_searches = [ ['AP','ANY','Calculus AB'],
                        ['AP','ANY','Calculus BC'],
                        ['AP','ANY','Statistics']   ]
    apMathStudents = {}
    for k,s in DATASET.items():
        for i in range(3):
            if len(s.getScores2(apMath_searches[i])) > 0 : 
                apMathStudents[k] = s
    
    return spMathStudents

def cats(df): #must be a pandas data frame
    #df = pd.DataFrame(big_table(data))

    df["CATEGORY_1"] = (( 
        (df["AP_Calculus_AB"] >= 3) |
        (df["AP_Calculus_BC"] >= 3) |
        (df["AP_Calc_AB_S"] >= 3  ) |
        (df["AP_Calc_BC_S"] >= 3  ) |
        (df["AP_Statistics"] >=3  ) ) 
        & ((df["ACT_Math"] > 0) | (df["SAT_math"] > 0))
        & (df["HS_Math_GPA"] > 0))

    df["CATEGORY_2"] =  (
        ((df["ACT_Math"]>=23) | (df["SAT_math"]) >= 550) | 
        ((df["ACT_Math"]>=20) | (df["SAT_math"] >= 490) 
               & (df["max_hs_math_level"] >= 11.0)) &
        (df["HS_Math_GPA"] >= 3) )

    df["CATEGORY_3"] = ( 
        ~(df["ACT_Math"] >= 20) & 
        ~(df["SAT_math"] >= 490) &
        (df["HS_Math_GPA"] >= 3.3) )

    df["CATEGORY_4"] = (
        ~(  df["CATEGORY_1"] |
            df["CATEGORY_2"] |
            df["CATEGORY_3"]    ) )

    df["CAT_1"] = df["CATEGORY_1"]*1
    df["CAT_2"] = (df["CATEGORY_2"] & ~(df["CATEGORY_1"]))*1
    df["CAT_3"] = (df["CATEGORY_3"] & ~(df["CATEGORY_1"]) & ~(df["CATEGORY_2"]))*1
    df["CAT_4"] = df["CATEGORY_4"] # CAT_4 contains cat_4*
    df["cat_4*"] = (
            ((~(df["ACT_Math"] >= 20) & (df["SAT_math"] < 490)) |
            ((df["ACT_Math"] < 20) & ~(df["SAT_math"] >= 490)))
            & (df["CAT_1"] == 0)
            & ~(df["HS_Math_GPA"] >= 3.3))*1
   #CAT_5 for unkown
    df["CAT_5"] = df["CAT_4"]-df["cat_4*"]
    return df
#graduationRates(DATASET)
#graduationRates1(DATASET)
#
#df = pd.DataFrame(first_math(DATASET))
#
##get prof the graduation rates data.
##bycourse grd12math and cohort
##also should get just yearly gradnumbers.
##
#def bool_to_num(x):
#    if type(x) == bool:
#        if x: return 1
#        else: return 0
#    elif type(x) == str:
#        if x == 'True': return 1
#        elif x == 'False': return 0
#        else: return None
#    else: return None
#
#df['grad'] = df['grad?'].apply(bool_to_num)
#
#gradinf = df.groupby(['Cohort', 'GRD12Math', 'grad'])
#
##totals for each labeling. without newest modification.
##{'Algebra 2': 6995,
## 'Calculus': 6485,
## 'Calculus Prep': 13709,
## 'Geometry': 1748,
## 'No Math': 16155,
## 'Other': 4509,
## 'Remedial': 835,
## 'Statistics': 5966}
#
#
#df_fall_05 = df.loc[df['Cohort']=='2057']
#df_F_05 = df_fall_05.groupby('GRD12Math')
#a5 = df_F_05['grad?'].mean()
#a = df.groupby(['Cohort','grad?','GRD12Math'])
#df_fall_04 = df.loc[df['Cohort']=='2067']
#df_F_04 = df_fall_04.groupby('GRD12Math')
#a4=df_F_04['grad?'].mean()
#
#df_fall_06 = df.loc[df['Cohort']=='2067']
#df_F_06 = df_fall_06.groupby('GRD12Math')
#a6=df_F_06['grad?'].mean()
#
#
#df_fall_07 = df.loc[df['Cohort']=='2077']
#df_F_07 = df_fall_07.groupby('GRD12Math')
#a7= df_F_07['grad?'].mean()
#
#df_fall_08 = df.loc[df['Cohort']=='2087']
#df_F_08 = df_fall_08.groupby('GRD12Math')
#a8= df_F_08['grad?'].mean()
#
#df_fall_09 = df.loc[df['Cohort']=='2097']
#df_F_09 = df_fall_09.groupby('GRD12Math')
#a9 = df_F_09['grad?'].mean()
#
#
#
