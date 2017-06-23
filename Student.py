

# class definition for student may want to create sub classes for
# highschool application and 
class Student:
    
    def __init__(self,sid):
        self.sid = sid   # Must be base64 encoded and uniquely identifying.
        self.hsCourses = [] # each course has pattern [name,grade1,grade2]
        self.hsOldCNames = [] # Course names prior to labeling.
        self.collegeSeq = []
    
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
    
# show college course info
    def show_collegeSeq(self):
        print(self.collegeSeq)

# show highschool course info
    def show_hsCourses(self):
        print(self.hsCourses)

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

#not sure if this should be college course sequence or just single course info
class CollegeSequence:
    def __init__(self):

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

