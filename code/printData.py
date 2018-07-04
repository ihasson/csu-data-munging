import readData as rd
import Student
import pandas as pd


##
def filterByMajor(dct,major="Mathematics"):
    print("filterByMajor")
    outdct = {}
    for s in dct:
        mj = dct[s].last_major
        if mj != None:
            if (mj.find(major))>=0:
                outdct[s] = dct[s]
    return outdct

## returns dictionary with only the students who enrolled in at least
#  one course.
def took_courses(dct):
    dct_out = {}
    for e in dct:
        if len(dct[e].cCourses) > 0:
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
        for cN in columnsDCT:
            if cN in stu.ccDict:
                s = ''
                for e in stu.ccDict[cN]:
                    #s+=e[0]+'|'+e[3]+'|'+e[2]+' '
                    s+=e.semester+'|'+e.grade_letter+'|'+str(e.units)+' '
                matDct[sid][cN] = s
           # else:
           #     matDct[sid][cN] = None
        # put in the other stuf
        majors = stu.majors
        majors.sort()
        if len(majors) >= 1:
            matDct[sid]['m1'] = majors[0][1] # I think term precedes major
            matDct[sid]['tm1'] = majors[0][0]
            matDct[sid]['flag']='1'
        if len(majors) >= 2:
            matDct[sid]['flag'] = '2'
            matDct[sid]['m2'] = majors[1][1]
            matDct[sid]['tm2'] = majors[1][0]
        if len(majors) >= 3:
            matDct[sid]['flag'] = '3'
        #    matDct[sid]['ml'] = majors[2][1]
        #    matDct[sid]['tml'] = majors[2][0]
        if len(majors) > 3:
            matDct[sid]['flag'] = '0'
        matDct[sid]['ml'] = majors[len(majors)-1][1]
        matDct[sid]['tml'] = majors[len(majors)-1][0]
    return matDct

def write_csv(matDct):
    f = open("math-majors.csv","w")
    df = pd.DataFrame(matDct).transpose()
    f.write(df.to_csv())
    return None

def read_all_and_filter():
    dataSet = rd.read_Progress(dct=rd.read_majors(dct=rd.read_College_Courses()))
    return took_courses(filterByMajor(dataSet))

def something():
    data = read_all_and_filter()
    matDct = make_DCT(data, find_courses(data))
    return matDct

def make_csv(
            out_file="math-majors.csv",
            course_file="data/courses-and-grades-by-term.txt",
            majors_file="data/majors.txt",
            major="Mathematics"
            ):
    """ Use this to make a csv file for the given major.
    """
    dataSet = rd.read_College_Courses(dct={},fname=course_file)
    dataSet = rd.read_majors(dct=dataSet,fname=majors_file)
    dataSet = took_courses(filterByMajor(dataSet,major))
    matDct =  make_DCT(dataSet,find_courses(dataSet))
    f = open(out_file,"w")
    df = pd.DataFrame(matDct).transpose()
    f.write(df.to_csv())
    f.close()

#def add_student_to_transitMatrix(student,term1,term2,tt=term_transition):
#    for cname1 in term1:
#        if not(cname1 in tm): tt[cname1] = {}
#        for cname2 in term2:
#            if cname2 in tm[cname1]: tt[cname1][cname2] +=1
#            else: tt[cname1][cname2] = 0
#    return tt


def termTransitionSeries(numTerms):
    """ support function for transitionMat 
    """
    term = 'term'
    terms=[]
    transitions = []
    for e in range(1,numTerms+1):
        terms.append(term+str(e))
    for i in range(numTerms-1):
        transitions.append([terms[i],terms[i+1]])
    return transitions

def transitionMat(dataSet):
    """ Give this a dictionary of Students
    """
    def addToTM(t_c,term1,term2,transition):
        if not(term1 in t_c) or not(term2 in t_c):
            return transition

        t1_courses = t_c[term1]
        t2_courses = t_c[term2]
        for course1 in t1_courses:
            if not(course1 in transition): transition[course1] = {}
            for course2 in t2_courses:
                if course2 in transition[course1]:
                    transition[course1][course2] += 1
                else:
                    transition[course1][course2] = 1
        return transition
    transitions = {}
    maxterms = 0
    student_term_courses = {}
    termTrans = []
    for s in dataSet:
        if dataSet[s].number_of_terms() > maxterms: 
            maxterms = dataSet[s].number_of_terms()
        student_term_courses[s] = dataSet[s].courses_by_term()
    
    termTrans = termTransitionSeries(maxterms)

    for tpre,tnext in termTrans:
        transName = tpre+'_to_'+tnext
        transitions[transName] = {}
        transit = transitions[transName]
        for stdnt,terms_courses in student_term_courses.items():
            transit = addToTM(terms_courses,tpre,tnext,transit)
    return transitions

def transitionsList(transmat):
    """ Takes one transition Dictionary and prints it as one transition per line
        into a text file.
    """
    lines = []
    transitions = []
    for k1,vct in transmat.items():
        for k2,val in vct.items():
            transitions.append([val,k1,k2])
    transitions.sort()
    for e in transitions:
        lines.append(e[1]+'['+str(e[0])+']_'+e[2]+'\n')
    f = open('transitions.txt','w')
    f.writelines(lines)
    f.close()

def mergeAllTerms(transmat):
    """ Merges all the transition dictionaries into a single transition 
        dictionary.
    """
    mergedTrans = {}
    for term,termTrans in transmat.items():
        for start_course,to_courses in termTrans.items():
            if not(start_course in mergedTrans):
                mergedTrans[start_course] = {}
            for end_course,num in to_courses.items():
                if end_course in mergedTrans[start_course]:
                    mergedTrans[start_course][end_course] += num
                else: 
                    mergedTrans[start_course][end_course] = num
    return mergedTrans
