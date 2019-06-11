import pandas as pd
from matplotlib import pyplot as plt
import re
import csv
from stuff_for_prof import *

filter_rules = [lambda x: int(x.cohort_term)>=2067, 
        lambda x: x.weighted_hs_Math_GPA() != None]      

def desiredterm(x): 
    return( (int(x.term) >= 2040) and (str.endswith(str(x.term),'7')))

attendance = pd.read_csv("csv/start_end_and_grad_terms.csv")
attendance.set_index("studentid",inplace=True)
gpas = pd.read_csv("data/hsgpa.csv",quoting=csv.QUOTE_NONE)
gpas.set_index('sid',inplace=True)
cohorts = pd.read_csv("data/cohorts.txt",sep='|',quoting=csv.QUOTE_NONE)
ftf = cohorts[cohorts['cohort']=='FTF']
ftf.set_index("studentid",inplace=True)
ftf = ftf.join(gpas)
ftf_retention = ftf.join(attendance)
df = pd.DataFrame(big_table(DATASET,filter_rules))
#df.set_index("sid",inplace=True) don't need this line
df = df.join(ftf)
df['HS_GPA'] = df['hsgpa']
EnglishCategories(df)
MathCategories3(df)

students = pd.read_csv("database/valid_students.csv")
students.set_index('sid',inplace=True)

# the need to figure out why missing 79 students.
# probably they don't have any valid math grades.
inter = pd.concat([students,df],axis=1,join='inner')

data = pd.DataFrame()
data['MathCAT'] = inter['MCAT']
data['HS_GPA'] = inter['HS_GPA']
data['first_math'] = inter['first_math']
data['HS_Math_GPA'] = inter['HS_Math_GPA']
data['Cohort'] = inter['Cohort']
data['first_math_grade'] = inter['first_math_grade']

relevent = ['MATH93','MATH92','MATH102', 'MATH140','MATH131', 
            'MATH103','ESM96LII','NONE','ESM96LI']
