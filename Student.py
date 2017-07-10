# Provides numeric values for grade strings.
# Need to change scores for non-letter 
gradesMap = {  'A+' 'A':4.0,'A-':3.7, #need to update the grade values
                'B+':3.3,'B':3.0,'B-':2.7,
                'C+':2.3,'C':2.0,'C-':1.7, 
                'D+':1.3,'D':1.0,'D-':0.7,
                'F':0.0, 'W':0.0,'WU':0.0,   
                'CR':2.0, 'NC':0.0, 'RP':0.94 # RP stands for repeat
                #,'X1':?, 'X2':? # not enterred symbols on app-dat
                }


## class definition for student may want to create sub classes for
# highschool application and 
class Student:
    
    def __init__(self,sid):
        self.sid = sid   # Must be base64 encoded and uniquely identifying.
        self.hsCourses = [] # each course has pattern [name,grade1,grade2]
        self.hsOldCNames = [] # Course names prior to labeling.
        self.collegeSeq = [] # old list format
        self.ccDict = {} # quick lookup dictionary of college courses
        #self.zipcode = None #Don't have this
        self.first_term = None
        self.last_term = None
        self.grad_term = None
        self.current_major = None
        self.majors = []
        self.cCourses = [] # has new object format
        #self.college course info and progress
##### enrollment info #####
        self.sequential_term_classification = []

## collegeSeq to ccDict and cCourses
    def oldCourseInfoToNew(self):
        if len(self.cCourses) == 0:
            for e in self.collegeSeq:
                self.cCourses.append(Course(e[0],e[1],e[3],e[2]))
        if len(self.ccDict) == 0:
            for e in self.cCourses:
                if e.name in self.ccDict:
                    self.ccDict[e.name].append(e)
                else:
                    self.ccDict[e.name] = [e]
                

## gpa_raw e.g. not adjusted for things like retakes
    def gpa_raw(self):
        grade_sum = 0 #grade val times units
        unit_sum = 0
        for c in self.cCourses:
            unit_sum+= c.units
            grade_sum += (c.grade_val * c.units)
        return grade_sum/unit_sum
     
##
## gpa_adjusted 
   # def gpa(self):

## returns a list of courseNames
    def hs_course_names(self):
        lsOfCnames = []
        for course in self.hsCourses:
            lsOfCnames.append(course.getCourseName())
        return lsOfCnames

## Sets the courselabels for all hs courses using the function provided
# 
    def set_hs_course_labels(self,matchfun):
        for h in self.hsCourses:
            h.set_course_label(matchfun)

## only the comments need to be updated
# Can take either string or list of strings. 
# True if student has taken any of the strings.
# Currently does not check grades.
# return a boolean
    def tookHSCourse(self, nameOfCourse,label=False):
        for hsc in self.hsCourses:
            if label:
                if nameOfCourse == hsc.course_label:
                    return True
            else:
                if nameOfCourse == hsc.descr:
                    return True
        return False
## similar to tookHSCourse but takes a function as an argument
#  the function this takes must return a boolean.
#  returns true as soon as in function returns true.
    def tookHSCourse_f(self, function):
        for hsc in self.hsCourses:
            if function(hsc):
                return True
        return False

#should remove soon.
## extract some number from the college course sequences to use as a feature
#    def col_seqScore(self):
#        best = 0
#        for course in self.collegeSeq :
#            if grade(course) in gradesMap:
#                cnum = int(re.findall('[0-9]+',cname(course))[0])
#                if gradesMap[grade(course)] > 0 and cnum > best:
#                    best = cnum
#        return best

## make dictionary for single student's college sequences
    def dictizeCSeq(self):
        dictionary = []
        for c in self.collegeSeq :
            dictionary.append({'course name': cname(c), 
                    'grade':gradesMap[grade(c)],
                    'units':units(c), 'term':term(c)
                    })
        return dictionary
    
## show college course info
    def show_collegeSeq(self):
        print(self.collegeSeq)

## need to update Still?
# show highschool course info
    def show_hsCourses(self):
        for c in self.hsCourses:
            c.showAll()

# make dictionary for single student's highschool records.
    def dictizeHSC(self):
        return self.hsCourses[0][0]
 #not sure if still need this   
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
#not suer if still need this.
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

## math course student took at csun returns first course the student took
#
    def first_math(self):
        earliest = self.collegeSeq[0]
        for e in self.collegeSeq:
            if e[0].isnumeric():
                if int(earliest[0]) > int(e[0]):
                    earliest = e
            else: print("error in Student.fist_math()" + str(earliest[0]) )
        return earliest

## Shows all available information about the student
    #def showall(self):




class HSCourse:
    def __init__(self):
        self.hs_crs_nbr = None
        self.hs_grade_level = None
        self.descr = None #name
        self.fall_gr = None
        self.spr_gr = None
        self.summer_gr = None
        self.honors = None
        self.sum2_gr = None
        #self.cman not a clue what this means
        self.High_School = None
        self.course_source =None # options seem to be "LIST" or "MANL"
        # this is the part where it actually gets alterred
        self.course_best_match=None
        self.course_label =None
        
    def asList(self):
       return [self.hs_crs_nbr, 
               self.hs_grade_level,
               self.descr,
               self.fall_gr,
               self.spr_gr,
               self.summer_gr,
               self.honors,
               self.sum2_gr,
               self.High_School,
               self.course_source, 
               self.course_label] 

    def showAll(self):
        print(str(self.descr))

## Sets the course_label using the passed in function
#
    def set_course_label(self,matchfun):
        self.course_label = matchfun(self.descr)

## Returns a course name. Should not be used with course match.
    def getCourseName(self):
        if self.course_label != None:
            return self.course_label
        else:
            return self.descr

## Match the course name to something else:
#   
#   manipfunc : str -> str
#               Massages the input to make it easier to work with.
#               Default is the identity function.
#   dictionary contains a dictionary of courses to compare against.
#    def matchName(self,manipfunc=(lambda x, x),dictionary):
#        return False ##NOT YET IMPLEMENTED.

## College Course
class Course:
    def __init__(self,nam=None,sem=None,gra=None,un=None):
        self.name = nam
        self.semester = sem
        self.grade_letter = gra
        self.units = int(un)
        self.grade_val = None
        self.repeat = gra == 'RP' # this course's grade got replaced
        if gra in gradesMap:
            self.grade_val = gradesMap[gra] 
        else:
            self.grade_val = 0.0
            self.units = 0

## Major info (perstudent)
#
#class Major:
#    def __init__(self):
#        self.

# some functions to help find info in the collegeSeq's
def term(colCor): 
    return colCor[0]

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

