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

def readall():
    data = {}
    data = rd.read_Large_HS(dictionary=data)
    data = rd.read_College_Seq(dct=data)
    data = rd.read_Progress(dct=data)
    for e in data:
        data[e].oldCourseInfoToNew()
    return data

## general filter for Student
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


def filter1(data):
    l = {}
    for s in data:
        st = data[s]
        if ((len(st.hsCourses) > 0) and (len(st.collegeSeq) > 0) and 
                (int(st.first_term) >= 2040) ):
            l[s] = st
    return l

def save(dct):
    with open("datafile.txt","wb") as f:
        pickle.dump(dct, f)
        #f.close()

def load_data():
    with open("datafile.txt","rb") as f:
        return pickle.load(f)

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

## result was neither student wound up matriculating.
def find_harvard_students(sdct={}):
    harvard_students = {}
    for st in sdct:
        for h in sdct[st].hsCourses:
            if h.High_School == 'HARVARD UNIVERSITY':
                harvard_students[st] = sdct[st]
    return harvard_students


def read_and_match():
    dct = filter1(readall())
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


## Takes a dictionary of lists as input. Returns what the key implies in
#   terms of passing or failing or failing the first math course.
#   
def first_course_grades(dct):
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
            current_term = 2177
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

def startYear(data):
    start_year = lambda x: str(int(x).__floordiv__(10))
    #data = readall()
    #data = filter1(readall())
    #data = rd.read_Progress(dct=rd.read_College_Seq())
    startTermDct = {}
    for e in data:
        if data[e].first_term != None:
            term = start_year(data[e].first_term)
            if term in startTermDct:
                startTermDct[term].append(data[e])
            else:
                startTermDct[term] = [data[e]]
    return startTermDct

## should also filter for incoming freshmen only
def graduationRateByStartYear():
    start_year = lambda x: str(int(x).__floordiv__(10))
    #data = readall()
    data = filter1(readall())
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

def partitionByRetention(dct):
    outdct = {'drop':{},'current':{},'grad':{}}
    for e in dct:
        gradTerm = int(dct[e].grad_term)
        lastTerm = int(dct[e].last_term)
        thisTerm = 2177
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

def stlstToDct(ls):
    dct={}
    for e in ls:
        dct[e.sid] = e
    return dct

        
