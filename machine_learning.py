import readData as rd
import Student
import pandas as pd


##
def filterByMajor(dct,major="Mathematics"):
    print("filterByMajor")
    outdct = {}
    debugStudent = ''
    try:
        for s in dct:
            debugStudent = s
            mj = dct[s].last_major
            if mj != None:
                if (mj.find(major))>=0:
                    outdct[s] = dct[s]
            #    outdct[s] = dct[s]
    except:
        print(debugStudent)
    return outdct

## returns dictionary with only the students who enrolled in at least
#  one course.
def took_courses(dct):
    dct_out = {}
    for e in dct:
        if len(dct[e].ccDict) > 0:
            dct_out[e] = dct[e]
    return dct_out



def find_courses(studentDCT):
    #get all column names.
    columnNames = {}
        #{'grad':'grad','m1':'m1','tm1':'tm1',
        #    'm2':'m2','tm2':'tm2','ml':'ml','tml':'tml','f':'f'}
    for key, stu in studentDCT.items():
        for cour in stu.ccDict:
            if cour in columnNames:
                columnNames[cour] +=1
            else: 
                columnNames[cour] = 1
    return columnNames  

def make_DCT(studentDCT,columnsDCT):
    matDct = {}
    for sid,stu in studentDCT.items():
        matDct[sid] = {}
        #for cN in columnsDCT:
        for cN in stu.ccDict:
            for e in stu.ccDict[cN]:
                if not(e.repeat):
                    matDct[sid][cN] = e.passed
       # else:
           #     matDct[sid][cN] = None
        # put in the other stuf
#        majors = stu.majors
#        majors.sort()
#        if len(majors) >= 1:
#            matDct[sid]['m1'] = majors[0][1] # I think term precedes major
#            matDct[sid]['tm1'] = majors[0][0]
#            matDct[sid]['flag']='1'
#        if len(majors) >= 2:
#            matDct[sid]['flag'] = '2'
#            matDct[sid]['m2'] = majors[1][1]
#            matDct[sid]['tm2'] = majors[1][0]
#        if len(majors) >= 3:
#            matDct[sid]['flag'] = '3'
#        #    matDct[sid]['ml'] = majors[2][1]
#        #    matDct[sid]['tml'] = majors[2][0]
#        if len(majors) > 3:
#            matDct[sid]['flag'] = '0'
        matDct[sid]['ml'] = stu.last_major
        #matDct[sid]['tml'] = majors[len(majors)-1][0]
    return matDct

def write_csv(matDct):
    f = open("math-majors.csv","w")
    df = pd.DataFrame(matDct).transpose()
    f.write(df.to_csv())
    return None

def read_all_and_filter():
    dataSet = rd.read_Progress(dct=rd.read_majors(dct=rd.read_College_Courses()))
    return took_courses(filterByMajor(dataSet))

def make_csv():
    data = read_all_and_filter()
    matDct = make_DCT(data, find_courses(data))
    write_csv(matDct)
    return matDct
