import readData as rd
import Student
import pickle
import pandas as pd
import courseMatcher as cm

# Provides numeric values for grade strings.
# Need to change scores for non-letter 
gradesMap = {  'A+':4.0, 'A':4.0,'A-':3.7, #need to update the grade values
                'B+':3.3,'B':3.0,'B-':2.7,
                'C+':2.3,'C':2.0,'C-':1.7, 
                'D+':1.3,'D':1.0,'D-':0.7,
                'F':0.0, 'W':0.0,'WU':0.0,   
                'CR':2.0, 'NC':0.0, 'RP':1.0 # RP stands for repeat
                #,'X1':?, 'X2':? # the grade not enterred symbols on app-dat
                }

## general filter for Student
# takes a list of functions
def and_filter(indct,fnlist):
    outdct = {}
    for stdnt in indct:
        st = indct[stdnt]
        clause = True
        for f in fnlist:
            clause = (clause and f(st))
        if clause:
            outdct[stdnt] = st
    return outdct


def filter_has_hs_and_college(data):
    l = {}
    for s in data:
        st = data[s]
        if ((len(st.hsCourses) > 0) and (len(st.cCourses) > 0) and 
                (int(st.cohort_term) >= 2040) ):
            l[s] = st
    return l

## filter by start term.
def term_filter(in_dct,term="2097"):
    termnum = int(term)
    out_dct={}
    for st in in_dct:
        if int(in_dct[st].first_term) >= termnum:
            out_dct[st] = in_dct[st]
    return out_dct


## take N from dictionary and return as list.
def takeN(dct,num=100):
    lout = []
    l = list(dct)
    for i in  range(num):
        lout.append(dct[l[i]])
    return lout

def makeDf(data):
    clmns = ['first_term','last_term','grad_term','lastHsCourse']
    rowlist = []
    for e in data:
        lasthsc='placeholder' 
        row = [data[e].first_term, data[e].last_term,data[e].grad_term,lasthsc]
        rowlist.append(row)
    df = pd.DataFrame(rowlist,columns=clmns) 
    return df

def make_traing_set(data):
    f = open("training2.txt",'w')
    lines = []
    for s in data:
        hsc = data[s].hsCourses
        if len(hsc[0].High_School) > 1:
            for c in hsc:
                lines.append("   ,"+str(c.High_School)+"  a,"+str(c.descr)+"\n")
    f.writelines(lines)
    f.close()

def filter_High_School(studentDct={}):
    outDct={}
    for e in studentDct:
        hsCs=studentDct[e].hsCourses
        for c in hsCs:
            if c.High_School != '':
                outDct[e]=studentDct[e] 
    return outDct

def student_hs():
    stdata= filter_High_School(readall())
    students_hs ={}
    for e in stdata:
        st=stdata[e]
        for h in st.hsCourses:
            studentSchools[h.High_School] = h.High_School
    return studentSchools

# result was neither student wound up matriculating.
def find_harvard_students(sdct={}):
    harvard_students = {}
    for st in sdct:
        for h in sdct[st].hsCourses:
            if h.High_School == 'HARVARD UNIVERSITY':
                harvard_students[st] = sdct[st]
    return harvard_students

# maybe there should be a class for all of this.
def set_hs_course_labels(sdct):
    mfun = cm.construct_matchfun()
    for k,s in sdct.items() : s.set_hs_course_labels(mfun)
    return sdct

def read_and_match():
    dct = filter_has_hs_and_college(readall())
    mfun = cm.construct_matchfun()
    for s in dct:
        dct[s].set_hs_course_labels(mfun)
    return dct

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

def tookCourse(dct,cname,label=False):
    outls = []
    for e in dct:
        if dct[e].tookHSCourse(cname,label):
            outls.append(dct[e])
    return outls

## Returns a dictionary of students who took algebra2 broken up by grade.
#  Students who repeated the course will be counted twice.
def took_algebra2_when(dct):
    g9=[]
    g10=[]
    g11=[]
    g12=[]
    ingrade = lambda glvl,hscourse: hscourse.hs_grade_level == glvl
    alg2 = lambda hscourse: hscourse.course_label == 'algebra2'
    for s in dct:
        tookcourse = dct[s].tookHSCourse_f
        if tookcourse(lambda hc: alg2(hc) and ingrade('9',hc)):
            g9.append(dct[s])
        if tookcourse(lambda hc: alg2(hc) and ingrade('10',hc)):
            g10.append(dct[s])
        if tookcourse(lambda hc: alg2(hc) and ingrade('11',hc)):
            g11.append(dct[s])
        if tookcourse(lambda hc: alg2(hc) and ingrade('12',hc)):
            g12.append(dct[s])
    return {'grade9':g9, 'grade10':g10, 'grade11':g11, 'grade12':g12}

def dct_by_gradelvl_math(dct,gradelvl='12'):
    outdct={'no_math':[]}
    for s in dct:
        no_g12_math = True
        dupcatch={} # add course labels to this to prevent duplicate students 
        for e in dct[s].hsCourses:
            if e.hs_grade_level == gradelvl:
                if not(e.course_label in  dupcatch):
                    dupcatch[e.course_label] = True
                    no_g12_math = False
                    if e.course_label in outdct:
                        outdct[e.course_label].append(dct[s])
                    else:
                        outdct[e.course_label] = [dct[s]]
        if no_g12_math:
            outdct['no_math'].append(dct[s])
    return outdct

## 'patitions' dict by math course in particular grade.
def partition_by_gradelvl_math(dct,gradelvl='12'):
    outdct={'no_math':{}}
    for s in dct:
        no_g12_math = True
        dupcatch={} # add course labels to this to prevent duplicate students 
        for e in dct[s].hsCourses:
            if e.hs_grade_level == gradelvl:
                if not(e.course_label in  dupcatch):
                    dupcatch[e.course_label] = True
                    no_g12_math = False
                    if e.course_label in outdct:
                        outdct[e.course_label][s] = dct[s]
                    else:
                        outdct[e.course_label]= {s:dct[s]}
        if no_g12_math:
            outdct['no_math'][s] = dct[s]
    return outdct


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

## returns a dictionary with start years as keys and val consisting of a LIST
#  of the students who started that year.
def startYear(data) -> "AVOID USING THIS!!!!":
    yrmap={ '204':'2004','205':'2005','206':'2006','207':'2007','208':'2008',
            '209':'2009','210':'2010','211':'2011','212':'2012','213':'2013',
            '214':'2014','215':'2015','216':'2016','217':'2017','203':'2003'}
    start_year = lambda x: str(int(x).__floordiv__(10))
    #data = readall()
    #data = filter_has_hs_and_college(readall())
    #data = rd.read_Progress(dct=rd.read_College_Seq())
    startTermDct = {}
    for e in data:
        if data[e].first_term != None:
            term = yrmap[start_year(data[e].first_term)]
        #if data[e].cohort_term != None:
        #    term = yrmap[start_year(data[e].cohort_term)]
            if term in startTermDct:
                startTermDct[term].append(data[e])
            else:
                startTermDct[term] = [data[e]]
    return startTermDct

## should also filter for incoming freshmen only
def graduationRateByStartYear(data):
    start_year = lambda x: str(int(x).__floordiv__(10))
    #data = readall()
    data = filter_has_hs_and_college(readall())
    #data = rd.read_Progress(dct=rd.read_College_Seq())
    startTermDct = {}
    for e in data:
        if data[e].first_term != None:
            term = start_year(data[e].first_term)
            if term in startTermDct:
                startTermDct[term].append(data[e])
            else:
                startTermDct[term] = [data[e]]
    return droppedOut(startTermDct)

## averages the grades of all students in a dictionary
def groupGPA(dct):
    outcomes = {}
    for e in dct:
        gsum =0
        usum=0
        for stdnt in dct[e]:
            for c in dct[e][stdnt].cCourses:
                gsum += c.grade_val * c.units
                usum += c.units
        if usum > 0:
            outcomes[e] = gsum/usum
    return outcomes

## partionByRetention
#  partitions dict into sub dicts based on retention
#   dropout is defined by a student having not taken a course since
#   for a year prior to fall 2017 and has not graduated.
def partitionByRetention(dct):
    outdct = {'drop':{},'current':{},'grad':{}}
    for e in dct:
        gradTerm = int(dct[e].grad_term)
        lastTerm = int(dct[e].last_term)
        thisTerm = 2167
        if gradTerm != 9999:
            outdct['grad'][e] = dct[e]
        elif (thisTerm - lastTerm) <= 10:
            outdct['current'][e] = dct[e]
        else: 
            outdct['drop'][e] = dct[e]
    return outdct

## assume the dictionary contains students.
def mapOverDct(dct,fn):
    dctout = {}
    for e in dct:
        dctout[e] = fn(dct[e])
    return dctout

## 
def foldOverDct(dct,fn):
    ls = list(dct)
    def foldover(l,d,f):
        if len(l)==1:
            return d[l.pop()]
        else:
            return f(d[l.pop()],foldover(l,d,f))
    return foldover(ls,dct,fn)

## converts a list of students to a dictionary
def stlstToDct(ls):
    dct={}
    for e in ls:
        dct[e.sid] = e
    return dct

#don't use this now
# for making a dictionary into pairs of dataname and data all in list
#   form
def dctToDataLists(dct):
    outlist=[]
    for e in dct:
        outlist.append([e,dct[e]])
    return outlist

## returns dict broken up by Cohort year
def partitionByCohortYear(dataSet,allowed_cohort_type=lambda x: True):
    outSet={}
    for sid,stdnt in dataSet.items():
        if allowed_cohort_type(stdnt):
            if stdnt.cohort_term in outSet:
                outSet[stdnt.cohort_term][sid] = stdnt
            else:
                outSet[stdnt.cohort_term] = {sid:stdnt}
    return outSet

## returns dict partitioned by last HS course(s)
def partitionBylastHSMath(dct):
    return mapOverDct(dct_by_gradelvl_math(dct),stlstToDct)

## depth must be an integer >= 1
def mapOverNestedDct(dictionary,function,depth):
    if depth == 1:
        return mapOverDct(dictionary,function)
    else:
        return mapOverNestedDct(dictionary,
                lambda x: mapOverDct(x,function),
                depth - 1)

## should really be cons function.
def idenfun(x,y=[]):
    return [x,y]

## a nested Fold function to use with dictionaries
def nestedFoldr(dictionary,accumulator,fun=idenfun,depth=1) -> "for dict":
    def foldr(dct,bin_fun,accum):
        acc = accum
        for key,e in dct.items():
            if acc == None:
                acc = e
            else:
                bin_fun(accum,e)
        return accum
    if depth == 1:
        return foldr(dictionary,fun,accumulator)
    else:
        accum2 = accumulator
        for key,val in dictionary.items():
            accum2 = nestedFoldr(val,fun,depth-1,accum2)
        return accum2


def showall(d):
    for x in d.keys():
        a = d[x]
        print(a.sid)
        print(a.hsCourses)
        print(a.collegeSeq)

#Maps a list of highschool courses to integer values via the 
#global hsClassesDict.
#Returns the sum of the class values if multiple in input
#Emptylists and unknownkeys are zero.
def multiHSCtoNum(hsClasses):
    resultRank = 0
    for e in hsClasses:
        if e in hsClassesDict:
            rank = hsClassesDict[e]
            resultRank = resultRank + rank
    return resultRank


def searchByHsScore(dictionary,mi,ma):
    foundlist = []
    for sid in dictionary:
        student = dictionary[sid]
        if (student.hs_score() > mi) and (student.hs_score() < ma):
            foundlist.append(sid)
            print(sid + "       "+ str(student.hs_score()))
    rcolCor[1]
    return foundlist


#doesn't even seem to work
#prob of ??? given course ? was taken
def everyoneThatTookHS(allStudents, courseName):
    setIcareAbout = []
    for s in allStudents:
        if s.tookHSCourse(courseName): 
            setIcareAbout.append(s)
    return setIcareAbout

#I think I can get rid of this one.
# a method to count all students who took a course but probably doesn't
# deduplicate
def countStudents(allstudents,l):
    n = 0
    for e in l:
        n += len(everyoneThatTookHS(allstudents, e))
    return n

#this implementation is dumb. Need to replace with dictionary based one later.
#A static method for finding the intersection of two student lists.
def intersection(a,b):
    c = []
    for x in a:
        for y in b:
            if x.sid == y.sid :
                c.append(y)
    return c

    
# can't remember what this is for
#def relabel_func(string ,dictionary=hsClassesDict):
#    courselist = list(dictionary.keys()) 
#    s = courseMatcher.justClean(string)
#    s = courseMatcher.findClosest(s,maxDist=4,listOfNames=courselist)
#    return dictionary[s]


#already deduplicates
def get_dict_by_courses(allstudent_info):
    info = {}
    for a_student in allstudent_info:
        for course in a_student.hsCourses:
            cname = course[0]
            if cname in info:
                info[cname][a_student.sid]= a_student
            else: 
                info[cname] = {}
                info[cname][a_student.sid] = a_student
    return info

def dict_to_list(d):
    ls = []
    for k in d.keys():
        ls.append(d[k])
    return ls

#can't remember if this has deduplication
def took_course(name,st_data_arr):
    count = 0
    students=[]
    for st in st_data_arr:
        took = 0
        for e in st.hsCourses:
            if e[0] == name:
                if took == 0: students.append(st)
                took = 1
        count += took
    return students

##Is intended to be given all student info in the form of a list of Student 
#objects. 
#Returns a dictionary of highschool course dictionaries each containing the
#students reported to have taken the class in their last year of highschool.
#
def get_dict_by_courses(allstudent_info):
    info = {}
    info['total'] = {}
    for a_student in allstudent_info:
        info['total'][a_student.sid] = a_student
        for course in a_student.hsCourses:
            cname = course[0]
            if cname in info:
                info[cname][a_student.sid]= a_student
            else: 
                info[cname] = {}
                info[cname][a_student.sid] = a_student
    return info

#need to rename
#currently only gives how many people took each course.
#Sum of all counts should be greater than the total students due to 
#intersection
def summary_counts(inf_d):
    for k in inf_d.keys():
        print(k)
        print(len(inf_d[k]))

## Checks for which students gave all grades.
# Probably has lots of bugs but don't want to bother fixing it because most
# students never inputed their grades so it's not even worth counting seriously.
def gave_all_grades(stList):
    count=0
    for es in stList:
        bad = 0
        for ec in es.hsCourses:
            if ( (ec[1] != 'X1' and ec[1] != 'X2') and 
                    (ec[2] != 'X1' and ec[2] != 'X2')):
                bad = 1
        count += bad
    return count

## Only one student at a time and returns pair where the first val is grades 
# submitted and second is how many classes.
# similar to gave_all_grades but actually worth implementing
# Still treats a blank as having submitted.
def grades_submitted_per_class(st):
    grades = 0
    classes = 0
    for c in st.hsCourses:
        classes += 1
        if c[1] != 'X1':
            grades += 1
        if c[2] != 'X2':
            grades += 1
    return (grades,classes)

def NestedDctTree(dct,depth=1):
    ls = []
    count=0
    for e in dct:
        if type(dct[e]) == dict:
            ls.append(NestedDctTree(dct[e], depth + 1))
    if len(ls) == 0:
        return depth
    else:
        return ls

def partitionByGraduationTerm(dataSet):
    outDCT = {}
    for k,e in dataSet.items():
        if e.grad_term in outDCT:
            outDCT[e.grad_term][k] = e
        else:
            outDCT[e.grad_term] = {k:e}
    return outDCT
        
def partitionByGraduationYear(dataSet):
    outDCT = {}
    for k,e in dataSet.items():
        if e.graduationYear() in outDCT:
            outDCT[e.graduationYear()][k] = e
        else:
            outDCT[e.graduationYear()] = {k:e}
    return outDCT

def partitionByHSMathCategory(dataSet,catMap=None):
    """ Breaks up students categorically
    """
    outDCT
    if catMap == None:
        catMap = {'calc':'Calculus',
                    'trigonometry' 'precalc' 'trig_and_precalc': 'Calculus Prep',
                    'algebra2': 'Algebra 2',
                    'none': 'None',
                    'stats': 'Statistics',
                    'adv_app_math' 'adv_math' 'geometry': 'Remedial',
                    'bad' : 'Other'}
    for s,k in dataSet.items():
        catMap[

    return 'incomplete'
