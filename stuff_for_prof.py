from analysis import *
from matplotlib import pyplot as plt
#import transitionMatrix as tm
import re
#from set_operations import *
import Label_Maps as LM
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

# returns transitions
def something_transitions(): #need to change name
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

#Really need to go over those logical quantifiers.

def MathCategories(df): #must be a pandas data frame
    #df = pd.DataFrame(big_table(data))
### might have gotten 'and' and or mixed up.
    df["CATEGORY_1"] = (( 
        (df["AP_Calculus_AB"] >= 3) |
        (df["AP_Calculus_BC"] >= 3) |
        (df["AP_Calc_AB_S"] >= 3  ) |
        (df["AP_Calc_BC_S"] >= 3  ) |
        (df["AP_Statistics"] >=3  ) ) 
        & ((df["ACT_Math"] > 0) | (df["SAT_math"] > 0))
        & (df["HS_Math_GPA"] > 0))

    df["CATEGORY_2"] =(  (
        ((df["ACT_Math"]>=23) | (df["SAT_math"]) >= 550) | 
        ((df["ACT_Math"]>=20) | (df["SAT_math"] >= 490) 
            & (df["max_hs_math_level"] >= 11.0)) | # this could be a problem
        (df["HS_Math_GPA"] >= 3.5)) 
        & (((df["ACT_Math"] > 0) | (df["SAT_math"] > 0)) & (df["HS_Math_GPA"]> 0))
        )

    df["CATEGORY_3"] = (( 
        ((df["ACT_Math"] >= 20) | 
         (df["SAT_math"] >= 490) ) |
        (df["HS_Math_GPA"] >= 3.3) ) 
        & (((df["ACT_Math"] > 0) | (df["SAT_math"] > 0)) & (df["HS_Math_GPA"] > 0)))

    df["CATEGORY_4"] = (
        ~(  df["CATEGORY_1"] |
            df["CATEGORY_2"] |
            df["CATEGORY_3"]) 
        & (((df["ACT_Math"] > 0) | (df["SAT_math"] > 0)) & (df["HS_Math_GPA"]> 0)))

    df["CAT_1"] = df["CATEGORY_1"]*1
    df["CAT_2"] = (df["CATEGORY_2"] & ~(df["CATEGORY_1"]))*1
    df["CAT_3"] = (df["CATEGORY_3"] & ~(df["CATEGORY_1"]) & ~(df["CATEGORY_2"]))*1
    df["CAT_4"] = df["CATEGORY_4"]*1 # CAT_4 contains cat_4*
    df["cat_4*"] = (
            ((~(df["ACT_Math"] >= 20) & (df["SAT_math"] < 490)) |
            ((df["ACT_Math"] < 20) & ~(df["SAT_math"] >= 490)))
            & (df["CAT_1"] == 0)
            & ~(df["HS_Math_GPA"] >= 3.3))*1

    
    df["CAT_5"] = (~(df["CATEGORY_1"] | df["CATEGORY_2"] |
            df["CATEGORY_3"] | df["CATEGORY_4"]))*1
   
    return df

def EnglishCategories(df):
# all categories come from Cal state except Category 5
# Category 5 is for students missing information for placement
# I.E. lacks both SAT Verbal and ACT Verbal or it lacks a gpa
    df["E_Category_1"] = ((
        (df["AP_English_Comp_&_Lit."] >= 3) |
        (df["AP_English_Lang_&_Comp"] >= 3)) 
        & ((df["ACT_English"] > 0) | (df["SAT_Verbal"] > 0))
        & (df["HS_English_GPA"] > 0))
                            
    df["E_Category_2"] =( ~(df["E_Category_1"]) & (
            (df["SAT_Verbal"] >= 500)  |
            (df["ACT_English"] >= 22) |
            (df["HS_English_GPA"] >= 3.3)) 
            & (((df["ACT_English"] > 0) | (df["SAT_Verbal"] > 0)) & 
                (df["HS_English_GPA"] > 0)))

    df["E_Category_3"] =( ~(df["E_Category_1"] | df["E_Category_2"]) & (
            ((df["SAT_Verbal"] < 500) & 
             (df["SAT_Verbal"] >= 460)) |
            ((df["ACT_English"] >= 19) & (df["ACT_English"] <22 )) |
            ((df["HS_English_GPA"] >= 3.0) &
                (df["HS_English_GPA"] < 3.3))) & 
            (((df["ACT_English"] > 0) | (df["SAT_Verbal"] > 0)) & 
                (df["HS_English_GPA"] > 0)))

    df["E_Category_4"] = ~(
        (df["AP_English_Comp_&_Lit."] >= 3) |
        (df["AP_English_Lang_&_Comp"] >= 3) | 
        (df["HS_English_GPA"] >= 3.0) |
        (df["ACT_English"] >= 19) |
        (df["SAT_Verbal"] >= 460) )
    df["E_C1"] = (df["E_Category_1"])*1
    df["E_C2"] = (df["E_Category_2"])*1
    df["E_C3"] = (df["E_Category_3"])*1
    df["E_C4"] = (df["E_Category_4"])*1
    df["E_C5"] = (~(df["E_Category_4"] |
            df["E_Category_3"] | df["E_Category_2"] | df["E_Category_1"]))*1

    def engcatcol(c1,c2,c3,c4,c5):
        result=""
        if c1: result = result+'1'
        if c2: result = result + '2'
        if c3: result = result+'3'
        if c4: result = result+'4'
        if c5: result = result+ '5'
        return result

    df["English_Category"]= df.apply(
            lambda x: engcatcol(x['E_C1'],x['E_C2'],x['E_C3'],x['E_C4'],x['E_C5']),
            axis=1)
    return df


def write_all_Math_and_labels_to_file():
    f = open("allMath_and_cats.txt", 'w')
    for sid,s in DATASET.items():
        for c in s.hsMath:
            f.write("\t|\t"+c.descr+ "\t|\t" + c.courseCategory()+"\n")
    f.close()

def get_unweighted_grade(row):
    grMap = LM.Label_Maps.gradesMap 
    grades = []
    try:
        if pd.notnull(row.Fall_Gr):
            grades.append(grMap[row.Fall_Gr])
        if pd.notnull(row.Spr_Gr):
            grades.append(grMap[row.Spr_Gr])
        if pd.notnull(row.Sum_Gr):
            grades.append(grMap[row.Sum_Gr])
        if pd.notnull(row.Sum2_Gr):
            grades.append(grMap[row.Sum2_Gr])
        if len(grades) != 0:
            return(sum(grades)/len(grades))
        else: return(None)
    except KeyError:
        unweighted_grade_error = open("grade_erro.txt",'a')
        unweighted_grade_error.write(str(row.sid)+","+str(row.Fall_Gr)
                +","+str(row.Spr_Gr)+","+str(row.Sum_Gr)+
                ","+str(row.Sum2_Gr)+"\n")
        unweighted_grade_error.close()
        return(None)

def get_weighted_grade(row):
    def isAP(descr):
       return(bool(re.search(pattern="[( ](AP)|(ap)[) \\n]",string=descr)))

    def weight(descr,grade,honors):
        if pd.notnull(honors):
            return( grade + 0.5)
        elif isAP(descr):
            return(grade + 1.0)
        else:
            return grade

    grMap = LM.Label_Maps.gradesMap 
    grades = []
    if pd.isnull(row.Descr): return(None)
    try:                            # need to add this in.
        if pd.notnull(row.Fall_Gr) and row.Fall_Gr in grMap:
            grades.append(weight(row.Descr,grMap[row.Fall_Gr],row.Honors))
        if pd.notnull(row.Spr_Gr) and row.Spr_Gr in grMap:
            grades.append(weight(row.Descr,grMap[row.Spr_Gr],row.Honors))
        if pd.notnull(row.Sum_Gr) and row.Sum_Gr in grMap:
            grades.append(weight(row.Descr,grMap[row.Sum_Gr],row.Honors))
        if pd.notnull(row.Sum2_Gr) and row.Sum2_Gr in grMap:
            grades.append(weight(row.Descr,grMap[row.Sum2_Gr],row.Honors))
        if len(grades) != 0:
            return(sum(grades)/len(grades))
        else: return(None)
    except KeyError:
        unweighted_grade_error = open("grade_erro.txt",'a')
        unweighted_grade_error.write(str(row.sid)+","+str(row.Fall_Gr)
                +","+str(row.Spr_Gr)+","+str(row.Sum_Gr)+
                ","+str(row.Sum2_Gr)+"\n")
        unweighted_grade_error.close()
        return(None)

def MathCategories2(df): #must be a pandas data frame
    #df = pd.DataFrame(big_table(data))
### might have gotten 'and' and or mixed up.
    def rank(row):
        if row.CAT_5 == 1:
            return 5
        elif row.CAT_4 == 1:
            return 4
        elif row.CAT_3 == 1:
            return 3
        elif row.CAT_2 == 1:
            return 2
        elif row.CAT_1 == 1:
            return 1
        else: return None

    df["CATEGORY_1"] = (( 
        (df["AP_Calculus_AB"] >= 3) |
        (df["AP_Calculus_BC"] >= 3) |
        (df["AP_Calc_AB_S"] >= 3  ) |
        (df["AP_Calc_BC_S"] >= 3  ) |
        (df["AP_Statistics"] >=3  ) ) 
        & ((df["ACT_Math"] > 0) | (df["SAT_math"] > 0))
        & (df["HS_Math_GPA"] > 0))

    df["CATEGORY_2"] =(  (
        ((df["ACT_Math"]>=23) | (df["SAT_math"]) >= 550) | 
        ((df["ACT_Math"]>=20) | (df["SAT_math"] >= 490) 
            & (df["max_hs_math_level"] >= 11.0)) | # this could be a problem
        ((df["HS_Math_GPA"] >= 3.5) | (df["HS_GPA"] >= 3.7) )) 
        & (((df["ACT_Math"] > 0) | (df["SAT_math"] > 0)) & (df["HS_Math_GPA"]> 0))
        )

    df["CATEGORY_3"] = (( 
        ((df["ACT_Math"] >= 20) | 
         (df["SAT_math"] >= 490) ) |
        (df["HS_Math_GPA"] >= 3.3) |
        (df["HS_GPA"] >= 3.0) )
        & (((df["ACT_Math"] > 0) | (df["SAT_math"] > 0)) & (df["HS_Math_GPA"] > 0)))

    df["CATEGORY_4"] = (
        ~(  df["CATEGORY_1"] |
            df["CATEGORY_2"] |
            df["CATEGORY_3"]) 
        & (((df["ACT_Math"] > 0) | (df["SAT_math"] > 0)) & (df["HS_Math_GPA"]> 0)))

    df["CAT_1"] = df["CATEGORY_1"]*1
    df["CAT_2"] = (df["CATEGORY_2"] & ~(df["CATEGORY_1"]))*1
    df["CAT_3"] = (df["CATEGORY_3"] & ~(df["CATEGORY_1"]) & ~(df["CATEGORY_2"]))*1
    df["CAT_4"] = df["CATEGORY_4"]*1 # CAT_4 contains cat_4*
    df["cat_4*"] = (
            ((~(df["ACT_Math"] >= 20) & (df["SAT_math"] < 490)) |
            ((df["ACT_Math"] < 20) & ~(df["SAT_math"] >= 490)))
            & (df["CAT_1"] == 0)
            & ~(df["HS_Math_GPA"] >= 3.3))*1

    
    df["CAT_5"] = (~(df["CATEGORY_1"] | df["CATEGORY_2"] |
            df["CATEGORY_3"] | df["CATEGORY_4"]))*1
    df["MCAT"] = df.apply(rank,axis=1)

    return df

def MathCategories3(df): #must be a pandas data frame
    #df = pd.DataFrame(big_table(data))
### might have gotten 'and' and or mixed up.
    def rank(row):
        if row.CAT_5 == 1:
            return 5
        elif row.CAT_4 == 1:
            return 4
        elif row.CAT_3 == 1:
            return 3
        elif row.CAT_2 == 1:
            return 2
        elif row.CAT_1 == 1:
            return 1
        else: return None

    df["CATEGORY_1"] = (( 
        (df["AP_Calculus_AB"] >= 3) |
        (df["AP_Calculus_BC"] >= 3) |
        (df["AP_Calc_AB_S"] >= 3  ) |
        (df["AP_Calc_BC_S"] >= 3  ) |
        (df["AP_Statistics"] >=3  ) ) 
        & (df["HS_Math_GPA"] > 0))

    df["CATEGORY_2"] =(  (
        ((df["ACT_Math"]>=23) | (df["SAT_math"]) >= 550) | 
        ((df["ACT_Math"]>=20) | (df["SAT_math"] >= 490) 
            & (df["max_hs_math_level"] >= 11.0)) | # this could be a problem
        ((df["HS_Math_GPA"] >= 3.5) | (df["HS_GPA"] >= 3.7) 
            | ((df["HS_GPA"] >= 3.0)&(df["HS_Math_Course_count"] >= 5)))) 
        & (df["HS_Math_GPA"]> 0))
        

    df["CATEGORY_3"] = (( 
        ((df["ACT_Math"] >= 20) | 
         (df["SAT_math"] >= 490) ) |
        (df["HS_Math_GPA"] >= 3.3) |
        (df["HS_GPA"] >= 3.0) )
        &  (df["HS_Math_GPA"] > 0))

    df["CATEGORY_4"] = (
        ~(  df["CATEGORY_1"] |
            df["CATEGORY_2"] |
            df["CATEGORY_3"]) 
        & (df["HS_Math_GPA"]> 0))

    df["CAT_1"] = df["CATEGORY_1"]*1
    df["CAT_2"] = (df["CATEGORY_2"] & ~(df["CATEGORY_1"]))*1
    df["CAT_3"] = (df["CATEGORY_3"] & ~(df["CATEGORY_1"]) & ~(df["CATEGORY_2"]))*1
    df["CAT_4"] = df["CATEGORY_4"]*1 # CAT_4 contains cat_4*
    df["cat_4*"] = (
            ((~(df["ACT_Math"] >= 20) & (df["SAT_math"] < 490)) |
            ((df["ACT_Math"] < 20) & ~(df["SAT_math"] >= 490)))
            & (df["CAT_1"] == 0)
            & ~(df["HS_Math_GPA"] >= 3.3))*1

    
    df["CAT_5"] = (~(df["CATEGORY_1"] | df["CATEGORY_2"] |
            df["CATEGORY_3"] | df["CATEGORY_4"]))*1
    df["MCAT"] = df.apply(rank,axis=1)

    return df

gpals = [i/100 for i in range(200,300)]
gpals.reverse()
satls = [i for i in range(510,1310,10)]
satls.extend([i for i in range(540,1310,40)])
satls.sort()
eligibility_index = list(zip(gpals, satls))

def is_eligible(gpa,sat):
    if gpa >= 3.0:
        return True
    for g,s in eligibility_index:
        if (gpa >= g) and (sat >= s):
            return True
    return False
