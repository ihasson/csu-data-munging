## @package readData
# NEED NEW DESCRIPTION!
#  
#
#    Copyright (C) 2017 Izzy Hasson <izzy.hasson.925@my.csun.edu>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 

#need to find out what WU means in gradesMap!
import binascii
import courseMatcher
import re
import sys
from Student import HSCourse
from Student import Student
from Student import Course
import pickle
#from Student import CollegeSequence

# For mapping highschool course names to integers.
# The assumed scoring system is the sum of the integers with 0 for things 
# not in the dictionary or if there was never anything to begin with
hsClassesDict = { #Depricated#
        'algebra 1':2,  'algebra 2':8,  'geometry':4,   'calculus':64,
        'pre-calculus':16,  'trigenometry':16,  'statistics':32,
        'math analysis':16,   'trig/alg':16,  'alg/trig':16,  'algebra':0,
        'unknown':-1
        }

#note: precalc equivalencies may be subject to change.
apparent_equivs = {'adv_app_math' 'geometry' : 'geometry',
        'math_anal' 'trigonometry' 'geo_alg_trig' 'precalc': 'precalc'}

hsClasslevels = {'algebra1':8, 'geometry':9, 'algebra2':10, 'precalc':11,
        'stats':11, 'calculus':12, 'bad':0, 'unknown':0}
        #, 'data_science':,'discrete_math': }# to be determined

# Provides numeric values for grade strings.
# Need to change scores for non-letter 
gradesMap = {  'A+' 'A':4.0,'A-':4, #need to update the grade values
                'B+':3,'B':3,'B-':3,
                'C+':2,'C':2,'C-':2, 
                'D+':1,'D':1,'D-':1,
                'F':0, 'W':0,'WU':0,   
                'CR':2, 'NC':0, 'RP':1 # RP stands for repeat
                #,'X1':?, 'X2':? # the grade not enterred symbols on app-dat
                }


def b16tob64(str16):
    return bytes.decode(binascii.unhexlify(str16))

# Only for those 3 highschools. 
# Returns a list of Students with their highschool classes.
# Will make the adding students to dictionary and figuring out what the
# courseString maps to in different function.
def read_High_School_Data(filesList):
    studentList = []
    errors = 0
    for filename in filesList:
        with open(filename, 'r') as f:
            linenum = 0 # for errorprinting
            #format studentid==|course|??|??|
            for line in f.readlines():
                linenum +=1
                line = line.rstrip()
                idstring,sep,rest = line.partition("|")
                newStudent = Student(idstring)
                vals = []
                vals = rest.split('|')
                #since each course should have a name and <=two grades
                if (len(vals)%4) != 0:
                    print(vals)
                    errors += 1
                    print( "Misformatted Input!  " + 
                        "line "+str(linenum)+ " in " + filename)
                else : 
                    for i in range(int(len(vals)/4)):
                        newStudent.hsOldCNames.append(vals[4*i+0])
                    #    if i > 1: print(idstring + "    "+ str(i))
                        acourse = (
                                    courseMatcher.findClosest(
                                                cleanHSCstr(vals[4*i+0])), 
                                    vals[4*i+1],
                                    vals[4*i+2])
                        newStudent.hsCourses.append(acourse)
                    studentList.append(newStudent)
    return studentList

# read data and also find what appears to be the closest match for the 
# course name.
def readAndClean(fileList):
    dataset = []
    for fname in fileList:
        with open(fname,'r') as f:
            for line in f:
                vals = line.split('|')
                cname = vals[1]
                cname = cname.replace('II','2')
                cname = cname.lower()
                cname = re.sub("\(.*\)","",cname)
                cname = re.sub("common core","",cname)
                cname = re.sub("honors","",cname)
                cname = re.sub("ap ","",cname)
                cname = re.sub("h(\.)? ","",cname)
                cname.strip()
                closest = findClosest(cname)
                dataset.append((vals,cname,closest))
                #print( cname +"\t" + closest )
    return dataset

#clean hsdata
def cleanHSCstr(string):
    cname = string
    cname = cname.replace('II','2')
    cname = cname.lower()
    cname = re.sub("\(.*\)","",cname)
    cname = re.sub("common core","",cname)
    cname = re.sub("honors","",cname)
    cname = re.sub("ap ","",cname)
    cname = re.sub("h(\.)? ","",cname)
    cname.strip()
    return cname

# Will be depricating soon.
# for college sequences
def read_a_sequence(line):
    line = line.strip()
    sid,placeholder,seq = line.partition("|")
    fields = seq.split("|")
    cInfoList = []
    if len(fields)%4 == 0:
        numbOfCourses = int(len(fields)/4)
        for x in range(numbOfCourses):
            cInfo = []
            cInfo.append(fields[(4*x)+0])
            cInfo.append(fields[(4*x)+1])
            cInfo.append(fields[(4*x)+2])
            cInfo.append(fields[(4*x)+3])
            cInfoList.append(cInfo)
        student = Student(sid)
        student.collegeSeq = cInfoList
        return student
    else:
        print("Malformed Course Sequence! Not enough fields.")
        return None

#Both inputs should be dictionaries filled with Student objects.
#For use because simple intersection cannot combine the info.
def mergeHSandColSeq(hs,cseq):
    mergedDict = {}
    indexNumb = 0
    for student in hs.keys():
        if student in cseq.keys():
            indexNumb += 1
            csunStudent = Student(student)
            csunStudent.squeezedID = indexNumb
            csunStudent.hsCourses = hs[student].hsCourses
            csunStudent.hsOldCNames = hs[student].hsOldCNames
            csunStudent.collegeSeq = cseq[student].collegeSeq
            mergedDict[student] = csunStudent
    return mergedDict

def get_sequences(fileName):
    sList = []
    with open(fileName, 'r') as f:
        for line in f.readlines():
            sList.append(read_a_sequence(line))
    return sList

## Construct dictionary for 3 school anal
#convenient command for construction of dictionary of student information
def constructDictionary():
    hsdict = {}
    seqdict = {}
    highschoolfiles = ['encrypted-grant-grades.txt',
            'encrypted-poly-grades.txt',
            'encrypted-taft-grades.txt']
    seqFile = 'Encrypted-Math-Sequences.txt'
    highschooldata = read_High_School_Data(highschoolfiles)
    seqList = get_sequences(seqFile)
    for student in highschooldata:
        hsdict[student.sid] = student
    for student in seqList:
        seqdict[student.sid] = student
    return mergeHSandColSeq(hsdict,seqdict)

#single command for constructing list of student objects.
def makeStList():
    stdict = constructDictionary()
    stlist =[]
    for key in stdict:
        stlist.append(stdict[key])
    return stlist

#can't remember what this is for
def constructDataTable():
    students = makeStList()
    dataForMatching = []
    for stu in students:
        dataForMatching.append([stu.oldCnames[0],stu.hsCourses[0]])


## reads a particular formatted file of student transcripts
#  not sure what to do with this now that it is clear that the highschool data
# was encoded differently from everything else.
def read_Large_HS(filename='hs-math.csv',dictionary={}):
    with open(filename,'r') as f:
        f.readline()
        for line in f.readlines():
            line = line.rstrip()
            st_inf = line.split(',')
            sid = st_inf[0]
            st=None
            if sid in dictionary:
                st = dictionary[sid]
            else:
                st = Student(sid)
                dictionary[sid] = st
            c_inf = HSCourse()
            # st_inf[1] is always '2'
            c_inf.hs_crs_nbr = st_inf[2]
            c_inf.hs_grade_level   = st_inf[3]
            c_inf.descr            = st_inf[4]
            c_inf.fall_gr          = st_inf[5]
            c_inf.spr_gr           = st_inf[6]
            c_inf.summer_gr        = st_inf[7]
            c_inf.honors           = st_inf[8]
            c_inf.sum2_gr          = st_inf[9]
            #c_inf.cman             = st_inf[10] no clue what this is
            c_inf.High_School      = str.upper(st_inf[11])
            c_inf.course_source    = st_inf[12]
            #c_inf.course_label     = somecoursematcher( descr )
            st.hsCourses.append(c_inf)
    return dictionary

## reads college sequences only for those 3 schools.
# 
def read_3sCgrades(filename='Encrypted-Math-Sequences.txt',dictionary={}):
    with open(filename,'r') as f:
        for line in f.readlines():
            line = line.rstrip()
            line = line.split("|")
            sid = line[0]
            fields = line
            st = None
            if sid in dictionary:
                st = dictionary[sid]
            else:
                st = Student(sid)
                dictionary[sid] = st
            for x in range(int( len(line)/4 ) ):
                st.collegeSeq.append(
                    [line[4*x+1],line[4*x+2],line[4*x+3],line[4*x+4]])
    return dictionary

# only reads math courses
def read_College_MATH(fname='Encrypted-Math-Sequences.txt',dct={}):
    f = open(fname,'r')

    for l in f.readlines():
        st = read_a_sequence(l)
        if st.sid in dct:
            dct[st.sid].collegeSeq = st.collegeSeq
        else: 
            dct[st.sid] = st
    return dct

## read the major information.
# Currently do not know how to identify double major
#  formatting as follows:
#  studentid|term|major|term|major (variable number of fields)\n
def read_majors(fname='data/majors.txt',dct={}):
    print("read_majors")
    #counter =100
    f = open(fname,'r')
    header = f.readline()
    for l in f.readlines():
        l=l.rstrip()
        sid,sep,tm = l.partition('|')
        tm = tm.split('|')
        if not(sid in dct): 
            dct[sid] = Student(sid)
        st = dct[sid]
        for k in range(int(len(tm)/2)):
            i=2*k
            st.majors.append([tm[i],tm[i+1]])
            #if counter > 0:
                #print(tm[i])
                #print(tm[i+1])
                #print("\n")
            #    counter += -1
        st.majors.sort()
        st.majors.reverse()
        st.last_major = st.majors[0][1]
    return dct

## read the major data
def read_Majors(filename='data/majors.txt',dct={},header=True):
    f = open(filename,'r')
    if header: f.readline()
    for line in f.readlines():
        sid,*tm = line.strip().split('|')
        if not(sid in dct):
            dct[sid] = Student(sid)
        for i in range(int(len(tm)/2)): # something might be off here.
            dct[sid].majors.append((tm[i+0],tm[i+1]))
        firstMajor = 9999
        lastMajor = 0000
        for m in dct[sid].majors:
            if int(m[0]) > lastMajor:
                dct[sid].last_major = m[1]
            if int(m[1]) < firstMajor:
                dct[sid].first_major = m[1]
    return dct


## reads the terms-codes-graddates file
def read_Progress(filename='data/terms-codes-graddates.txt',dct={}):
    f = open(filename,'r')
    f.readline()
    for line in f.readlines():
        l = line.split('|')
        if not(l[0] in dct):
            dct[l[0]] = Student(l[0])
        st = dct[l[0]]
        st.first_term = l[1]
        st.last_term = l[2]
        st.grad_term = l[3]
    f.close()
    return dct

## need to change the names of the input variables to avoid confusion.
def big_merge(hsd,csd):
    combined = {}
    stl = None
    if len(hsd)>len(csd):
        stl = list(csd)
    else:
        stl = list(hsd)
    for s in stl:
        if (s in csd) and (s in hsd):
            combined[s] = hsd[s]
            combined[s].collegeSeq = csd[s].collegeSeq
    return combined

## read a file that has the name of every school in California and get the 
#   highschool names.
def read_CA_SCHOOL_FILE():
    f= open("CA-school-names.txt",'r')
    hsnames={}
    f.readline()
    for line in f.readlines():
        sinfo = line.split('\t')
        if int(sinfo[19]) > 0: # index 19 is number of 12th grade students
            #hsnames[sinfo[3]]= [sinfo[0],sinfo[3],sinfo[19]]
            hsnames[str.upper(sinfo[3][:20])]=str.upper(sinfo[3][:20])
    return hsnames

# will need to modify this and Student
## reads the cohorts information
def read_Cohorts(fname='data/cohorts.txt',dct={},header=True):
    f = open(fname,'r')
    if header: f.readline()
    for line in f.readlines():
        line = line.strip()
        sid,cohort,term=line.split('|')
        if not(sid in dct):
            dct[sid] = Student(sid)
        stdnt = dct[sid]
        stdnt.cohort_term = term
        stdnt.cohort_type = cohort
    f.close()
    return dct

def read_Math_SAT(fname='data/sat-data.txt',dct={},header=True):
    f = open(fname,'r')
    if header: f.readline()
    for line in f.readlines():
        line = line.strip()
        sid,score = line.split('|')
        if not(sid in dct):
            dct[sid] = Student(sid)
        dct[sid].sat_math
    return dct

def read_College_Courses(fname='data/courses-and-grades-by-term.txt',dct={},
        header=True):
    f = open(fname,'r')
    if header: f.readline
    def breakthrees(lst,accum=[]):
        if len(lst) < 3:
            return accum,lst
        elif len(lst) == 3:
            a,b,c = lst
            accum.append([a,b,c])
            return accum,[]
        else:
            a,b,c,*rest = lst
            accum.append([a,b,c])
            return breakthrees(rest,accum)
    for line in f.readlines():
        sid,term,*rest = line.strip().split('|')
        if not(sid in dct):
            dct[sid] = Student(sid)
        courses,leftover = breakthrees(rest,[])
        if len(leftover) > 0: print(leftover)
        for c in courses:
            nc = Course(nam=c[0],sem=term,gra=c[2],un=c[1])
            dct[sid].cCourses.append(nc)
            dct[sid].add_to_ccDict(nc)
    f.close()
    return dct

## a read all the data I have function
def readall():
    data = {}
    data = rd.read_Large_HS(dictionary=data)
    rd.read_College_Courses(dct=data)
    #data = rd.read_College_Seq(dct=data # possibly need to reenable this.)
    data = rd.read_Progress(dct=data)
    data = rd.read_Cohorts(dct=data)
    data = rd.read_MATH_SAT(dct=data)
    #for e in data:                     #and this
    #    data[e].oldCourseInfoToNew()
    return data

## convenient save function
def save(dct):
    with open("datafile.txt","wb") as f:
        pickle.dump(dct, f)
        f.close()
## loads back the data from the above save
def load_data():
    with open("datafile.txt","rb") as f:
        d = pickle.load(f)
        return d

