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
import base64
import courseMatcher
import re
import sys
import numpy as np
import xarray as xr

# For mapping highschool course names to integers.
# The assumed scoring system is the sum of the integers with 0 for things 
# not in the dictionary or if there was never anything to begin with
hsClassesDict = { #Depricated#
        'algebra 1':2,  'algebra 2':8,  'geometry':4,   'calculus':64,
        'pre-calculus':16,  'trigenometry':16,  'statistics':32,
        'math analysis':16,   'trig/alg':16,  'alg/trig':16,  'algebra':0,
        'unknown':-1
        }

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

# class definition for student may want to create sub classes for
# highschool application and 
class Student:
    
    def __init__(self,sid):
        self.sid = sid   # Must be base64 encoded and uniquely identifying.
        self.hsCourses = [] # each course has pattern [name,grade1,grade2]
        self.hsOldCNames = [] # Course names prior to labeling.
        self.collegeSeq = []
#        self.sqeezedID = None #for use if want something more reasonable 
                              # unique identifier than a really large 
                              # integer

#deprecate soon!
# Undo the removal of padding from base64.
    def sid64(self):
        return self.sid + "=="
# 
#    def sidInt(self):
#        if self.squeezedID:
#            return self.squeezedID
#        else:
#            return int.from_bytes(base64.b64decode(self.sid64()),'big')

# returns a list of courseNames
    def hs_course_names(self):
        lsOfCnames = []
        for course in self.hsCourses:
            lsOfCnames.append(course[0])
        return lsOfCnames

# returns the (guessed) valuation of how much math the student did
    def hs_score(self):
        return multiHSCtoNum(self.hs_course_names())
        
# Can take either string or list of strings. 
# True if student has taken any of the strings.
# Currently does not check grades.
# return a boolean
    def tookHSCourse(self, nameOfCourse):
        if nameOfCourse is str:
            coursesTaken = self.hs_course_names()
            courseIdNum = hsClassesDict[nameOfCourse]
            for e in coursesTaken:
               if hsClassesDict[e] == courseIdNum:
                   return True
            return False
        elif nameOfCourse is list:
            if len(nameOfCourse) >=1: 
                return (tookHSCourse(nameOfCourse.pop) or 
                        tookHSCourse(nameOfCourse))
        else: 
            return False
        
# extract some number from the college course sequences to use as a feature
    def col_seqScore(self):
        best = 0
        for course in self.collegeSeq :
            if grade(course) in gradesMap:
                cnum = int(re.findall('[0-9]+',cname(course))[0])
                if gradesMap[grade(course)] > 0 and cnum > best:
                    best = cnum
        return best

#make dictionary for single student's college sequences
    def dictizeCSeq(self):
        dictionary = []
        for c in self.collegeSeq :
            dictionary.append({'course name': cname(c), 
                    'grade':gradesMap[grade(c)],
                    'units':units(c), 'term':term(c)
                    })
        return dictionary
    def listifyCSeq(self):
        l = []
        for c in self.collegeSeq :
            l.append([cname(c), gradesMap[grade(c)],units(c),term(c)])
        return l

# make dictionary for single student's highschool records.
    def dictizeHSC(self):
        return self.hsCourses[0][0]
    
    def datarrayCSeq(self):
        names = []
        grades = []
        units = []
        terms = []
        l = []
        for c in self.collegeSeq :
            l0 = cname(c)
            g = gradesMap[grade(c)]
            l1 = g
            l2 = int(c[2])
            l3 = int(c[0])
            l.append([l0,l1,l2,l3])
        return l
    
    def tolistOfArrays(self):
        ls = []
        hinfo = self.hs_score()
        for c in self.collegeSeq:
            name = self.sidInt()
            semester = int(term(c))
            coursename = cname(c)
            gradeval = int(gradesMap[grade(c)])
            unitnumb = int(units(c))
            ls.append([name,hinfo,coursename,gradeval,unitnumb,semester])
        return ls

# Make a dictionary object
    def dictize(self):
        #s = int.from_bytes(base64.b64decode(self.sid +"=="),'big')
        return {'SID': self.sidInt(), 'CS': self.listifyCSeq()[0][0],
                'HS':self.hs_score() 
                }

# some functions to help find info in the collegeSeq's
def term(colCor): return colCor[0]
def cname(colCor): 
    return int(re.findall('[0-9]+',colCor[1])[0])

# Converts the base64 encoded student id from the highschooldata to 
# base16 encoding to conform with the new data.
# Some massaging of the out put string may be needed.
def sid64tosid16(str64):
    if not(str64.find("==")):
        str64 = str64 + "=="
    return base64.b16encode(base64.b64decode(str64))

# Takes a course from the college sequences and returns the info from the 
# term field.
def readTerm(courseInf):
    century = {'0':1900, '2':2000}
    semesterdict = {'1':'winter',   '3':'spring',   
                    '5':'summer',   '7':'fall'
                    }
    termStr = courseInf[0]
    cent = termStr[0]
    year = termStr[1:3]
    semester = termStr[3]
    return (century[cent] + int(year) , semesterdict[semester]) 

# extracts the number from the name of a course
def colCourseToNum(cname):
    cnum = int(re.findall('[0-9]+',cname))
    return cnum

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
                idstring,rest = line.split("==|")
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

# for college sequences
def read_a_sequence(line):
    line = line.strip()
    sid,seq = line.split("==|")
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


#prob of ??? given course ? was taken
def everyoneThatTookHS(allStudents, courseName):
    setIzcareAbout = []
    for s in allStudents:
        if s.tookHSCourse(courseName): 
            setIcareAbout.append(s)
    return setIcareAbout

def countStudents(allstudents,l):
    n = 0
    for e in l:
        n += len(everyoneThatTookHS(allstudents, e))
    return n

#seems to be a static method for finding the intersection of two student lists
def intersection(a,b):
    c = []
    for x in a:
        for y in b:
            if x.sid == y.sid :
                c.append(y)
    return c

def constructDataTable():
    students = makeStList()
    dataForMatching = []
    for stu in students:
        dataForMatching.append([stu.oldCnames[0],stu.hsCourses[0]])

def relabel_func(string ,dictionary=hsClassesDict):
    courselist = list(dictionary.keys()) 
    s = courseMatcher.justClean(string)
    s = courseMatcher.findClosest(s,maxDist=4,listOfNames=courselist)
    return dictionary[s]

