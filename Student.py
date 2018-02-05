## @package Student
# Defines the student object and some methods for getting usefull information
# on a per student basis.
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

from Label_Maps import Label_Maps
import re
get_grade_failed = []
## class definition for student may want to create sub classes for
# highschool application and 
class Student:
    
    def __init__(self,sid):
        self.sid = sid   # Must be base64 encoded and uniquely identifying.
        self.hsCourses = [] # each course
        self.hsEnglish = []
        self.hsOldCNames = [] # Course names prior to labeling.
        #self.collegeSeq = [] # old list format
        self.ccDict = {} # quick lookup dictionary of college courses
        #self.zipcode = None #Don't have this
        self.first_term = None
        self.last_term = None
        self.grad_term = None
        #self.current_major = None
        self.majors = []
        self.first_major = None
        self.last_major = None
        self.cCourses = [] # has new object format
        #self.college course info and progress
##### enrollment info #####
        self.sequential_term_classification = []
        self.cohort_type = None # should be FTF or FTT
        self.cohort_term = None 
        self.sat_math = None # deprecating
        self.exams_tree = None


## the structure should be 
#((test(date (subtest1,score1),(subtest2,score2)...)), 
#     (test (date (subtest,score)),...),...)
    def setExams(self,exams):
        self.exams_tree = exams

## adds course to ccDict
    def add_to_ccDict(self,crs) -> "input must be Course":
        if crs.name in self.ccDict:
            self.ccDict[crs.name].append(crs)
        else:
            self.ccDict[crs.name] = [crs]

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
## grade12 math
    def grd12math(self):
        """ by label """
        out = {}
        for e in self.hsCourses:
            if e.hs_grade_level == '12':
                out[e.course_label] = self.sid
        if len(out) == 0: #print('no course name?!?')
            out['None'] = self.sid
        return out

    def grd12mathCateg(self):
        """ by category """
        out = {}
        labelmap = Label_Maps.hs_label_categ
        for e in self.hsCourses:
            if e.hs_grade_level == '12':
                out[labelmap[e.course_label]] = self.sid
        if len(out) == 0: #print('no course name?!?')
            out['None'] = self.sid
        return out
    
    def getGradeLevelMath(self, grade_level='12')->"non-empty set of strings":
        """
        Takes grade level as string.
        Returns the set of all course_labels such that
        the course was taken in the matching grade.
        If no courses were taken in that grade then 
        returns a set containing 'None'.
        """
        out = set()
        for e in self.hsCourses:
            if e.hs_grade_level == grade_level:
                out.add(e.course_label)
        if len(out) == 0:
            out.add('None')
        return out
    
    def hsMathCategory(self, grd_lvl)->"one label output.": 
        """ takes grade lvl and returns the best course.
        """
        courses = self.getGradeLevelMath(grd_lvl)
        categorized = list(map(lambda x: Label_Maps.hs_label_categ[x], courses))
        if len(categorized) > 1:
            # as a place holder rule
            return 'Multiple'
        else:
            return categorized[0]
        
## gets hs courses
    def hs_courses(self, labeled=True):
        out = {}
        for e in self.hsCourses:
            out[e.course_label] = self.sid
        return out

## returns boolean
    def hasGraduated(self): 
        return self.grad_term != '9999'

## gpa_raw e.g. not adjusted for things like retakes
    def gpa_raw(self):
        grade_sum = 0 #grade val times units
        unit_sum = 0
        for c in self.cCourses:
            unit_sum+= c.units
            grade_sum += (c.grade_val * c.units)
        try:
            return grade_sum/unit_sum
        except ZeroDivisionError as err:
            print('bad student: ',self.sid)
            return -1

## has first term instead of cohort
    def length_of_stay(self):
        return int(self.last_term) - int(self.first_term)

## more convenient time to graduate
    def time_to_grad2(self):
        return int(self.grad_term)-int(self.cohort_term)

## time to graduate
    def time_to_grad(self):
        gt = int(self.grad_term)
        if gt == 9999:
            return -1
        else :
            return gt -int(self.cohort_term)

## for use with the transition matrix
    def courses_by_term(self):
        semesterDct = {}
        outDct = {}
        for e in self.cCourses:
            if not(e.semester in semesterDct):
                semesterDct[e.semester] = []
            semesterDct[e.semester].append(e.name)
        termMap = {}
        term = 'term'
        i = 1
        semesterlist = list(semesterDct)
        semesterlist.sort()
        for k in semesterlist:
            termN = term+str(i)
            termMap[k]=termN
            i+=1
        for c in semesterDct:
            outDct[termMap[c]] = semesterDct[c]
        return outDct

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

    def fourYearGrad(self):
        return (int(self.grad_term) - int(self.cohort_term) < 50)

    def sixYearGrad(self):
        return (int(self.grad_term)-int(self.cohort_term) < 70)

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

## Has graduated college?
    def hasGraduated(self):
        return (int(self.grad_term) < 9999)

## make dictionary for single student's college sequences
    def dictizeCSeq(self):
        dictionary = []
        for c in self.collegeSeq :
            dictionary.append({'course name': cname(c), 
                    'grade':gradesMap[grade(c)],
                    'units':units(c), 'term':term(c)
                    })
        return dictionary

##  number of semesters with summer counted as half
    def number_of_terms(self):
        semesters={}
        for e in self.cCourses:
            semesters[e.semester] = 1
        return len(semesters)

## number of units total
    def units_total(self):
        units = 0
        for e in self.cCourses:
            units += e.units
        return units

## grade-counts
# need a better description
    def grade_counts(self):
        grades = {}
        for e in self.cCourses:
            if e.grade_letter in grades:
                grades[e.grade_letter] += 1
            else:
                grades[e.grade_letter] = 1
        return grades

# this doesn't work
# graduating major
# should have ben last major
    def last_major(self):
        try:
            self.majors.sort()
            self.majors.reverse()
            return self.majors[0][1]
        except IndexError as err:
            print('abberant student:    ',self.sid)
            return 'None'

## gives a stat summary    
    def results(self,highschool=False):
        summary={
                'cohort_type': self.cohort_type,
                'cohort_term': self.cohort_term,
                'grad':self.hasGraduated(),
                'last_term': self.last_term,
                #'time_at_csun':self.length_of_stay(),
                'term_count':self.number_of_terms(),
                'units_total':self.units_total(),
                'last_major':self.last_major,
                'rough_gpa': self.gpa_raw(),
                }
        for key,num in self.grade_counts().items():
            summary[key] = num
        if highschool:
            summary['num_g12_math'] = len(self.grd12math())
            summary['g12_math']=list(self.grd12math())
            summary['MATH_SAT']=self.sat_math
        return summary
    
    def featureVector(self):
        return [self.cohort_term,
                self.hasGraduated(),
                self.last_major,
                self.last_term,
                self.units_total(),
                self.gpa_raw()]

    def showHSCourses(self):
        """show hs course info"""
        for e in self.hsCourses:
            e.showall()

# needs to be replaced
## show college course info
#    def show_collegeSeq(self):
#        print(self.collegeSeq)

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
#    def first_math(self):
#        earliest = self.collegeSeq[0]
#        for e in self.collegeSeq:
#            if e[0].isnumeric():
#                if int(earliest[0]) > int(e[0]):
#                    earliest = e
#            else: print("error in Student.first_math()" + str(earliest[0]) )
#        return earliest
    def first_math(self):
        try:
            mathCourses = []
            for course in self.cCourses:
                if ('MATH' in course.name) or ('ESM' in course.name):
                    mathCourses.append([int(course.semester),course.name])
            mathCourses.sort()
            return mathCourses[0][1]
        except:
            return 'NONE'

    def first_math_course(self)->"returns a course object rather than name":
        try:
            mathCourses = []
            for course in self.cCourses:
                if ('MATH' in course.name) or ('ESM' in course.name):
                    mathCourses.append([int(course.semester),course])
            mathCourses.sort()
            return mathCourses[0][1]
        except:
            return None  # need to handle this error better.

## graduation year without term
    def graduationYear(self):
        gy = str(int(self.grad_term).__floordiv__(10))
        if gy in yrmap:
            return yrmap[gy]
        else:
            return '9999'

## Shows all available information about the student
    #def showall(self):

    def has_passed(self,course_name):
        if course_name in self.ccDict:
            for c in self.ccDict[course_name]:
                if c.passed == 1: return 1
        return 0

    def getScores(self,test='ELM'):
        """ search exams_tree for scores for a given test"""
        def getscores(treeDct,accum):
            if type(treeDct) == dict:
                for e in treeDct.values():
                    getscores(e,accum)
            else:
                accum.append(treeDct)
        def search(treeDct,test,accum):
            if type(treeDct) == dict:
                if test in treeDct:
                    getscores(treeDct[test],accum)
                else:
                    for e in treeDct.values():
                        search(e,test,accum)
        
        scores = []
        search(self.exams_tree,test,scores)
        return scores
#Need to change the name of this function
    # if len(test) == 0 then get scores
    # if tree hits bottom and test not empty no test 
    # if hd of test in dict get scores from test[hd] tail(test)
    def getScores2(self,test=['SAT','ANY','Math']) -> "returns list of strings":
        
        def getscores(treeDct,accum):
            if type(treeDct) == dict:
                for e in treeDct.values():
                    getscores(e,accum)
            else:
                accum.appendd(treeDct)
            return accum

        def search(treeDct,testnames,accum):
            if len(testnames)==0: 
                if type(treeDct) != dict:
                    accum.append(treeDct)
                else: #type(treeDct)==dict
                    getscores(treeDct,accum)
            else:
                try:
                    if testnames[0] == 'ANY':
                        for t in treeDct.values():
                            search(t,testnames[1:],accum)
                    elif testnames[0] in treeDct:
                        search(treeDct[testnames[0]],testnames[1:],accum)
                    else:
                        pass
                except: print(self.sid)
            return None
    
        acc = []
        if self.exams_tree != None:
            search(self.exams_tree,test,acc)
        return acc
    
    def getBestScore(self,test='MPT1'):
        scores = list(map(lambda x: int(x), self.getScores(test)))
        if len(scores) > 0:
            return max(scores)
        else: return None

    def getBestScore2(self,test=['AP','ANY','Calculus AB']):
        scores = list(map(lambda x: int(x), self.getScores2(test)))
        if len(scores) > 0:
            return max(scores)
        else: return None

    def hasExams(self):
        """ if student has any exams in the full exams database returns true.
        """
        if self.exams_tree == None:
            return False
        elif len(self.exams_tree) > 0:
            return True
        else: 
            return False

    def hasSAT(self):
        """ Returns True if the student has done the SAT
        """
        if self.hasExams():
            if 'SAT' in self.exams_tree:
                return True
        return False

    def bestSATMath(self):
        """ Returns the best SAT math score regardless of whether the combined
            SAT is better or whether there was a better ACT.
            returns -1 if no math SAT
        """
        best = -1
        if 'SAT' in self.exams_tree:
            for test_date,subtests in self.exams_tree['SAT'].items():
                if 'Math' in subtests:
                    if int(subtests['Math']) > best:
                        best = int(subtests['Math'])
            return best
        else: 
            return None
    
    def getACTMath(self):
        scores = self.getScores2(['ACT','ANY','Math'])
        return list(map(lambda x: int(x),scores))
    
    def hasACT(self):
        if self.hasExams():
            return len(self.getACTMath()) > 0
        else: 
            return False

    def bestACTMath(self):
        scores = self.getACTMath()
        if len(scores) == 0:
            return None
        else: 
            return max(scores)

    def getSATComposite(self) -> "list of (int,int)":
        """ returns list of pairs of all of the student's SATs in the form
            [[math1,verbal1],[math2,verbal2]...] or if no SAT composite
            then [].
        """
        sats = []
        if self.hasSAT():
            for test_date,subtests in self.exams_tree['SAT'].items():
                if 'Math' in subtests and 'Verbal' in subtests:
                    sats.append([int(subtests['Math']),int(subtests['Verbal'])])
        return sats

    def bestSATComposite(self):
        best = -1
        if self.hasSAT():
            for test__date,subtests in self.exams_tree['SAT'].items():
                if 'Math' in subtests and 'Verbal' in subtests:
                    c = int(subtests['Math'])+int(subtests['Verbal'])
                    if c > best:
                        best = c
        if best == -1: return None
        else: return best
    
    def bestSATCompositeWithACT(self):
        """ Takes ACT scores and converts them to SAT before figuring out
            which score is best.
        """
        best = self.bestSATComposite()
        acts = self.getScores2(['ACT','ANY','Composite'])
        sat_from_act = list(map(lambda x: Label_Maps.actTOsat[x],acts))
        if len(sat_from_act) > 0:
            best_satact = max(map(lambda x: int(x),sat_from_act))
            if best_satact > best: best = best_satact
        return best
    
    def ACTBetterThanSAT(self):
        try:
            if self.hasSAT():
                sat = self.bestSATComposite()
                act = self.bestSATCompositeWithACT()
                return act > sat
            else: 
                return self.hasACT()
        except:
            return True

    def hasELM(self):
        if self.hasExams():
            if 'ELM' in self.exams_tree:
                return True
        return False

    def bestELM(self):
        if self.hasELM():
            return max(map(lambda x: int(x), self.getScores('ELM')))
        else: return None

    def hasTheirShitTogether(self):
        #has math in order
        if len(self.hsCourses) >= 3:
            for e in self.hsCourses:
                if e.High_School == None or len(e.High_School) < 2:
                    return False
        if len(self.hsEnglish) >= 3:
            for e in self.hsEnglish:
                if e.High_School == None or len(e.High_School) < 2:
                    return False
        if not(self.hasExams()):
            return False
        return True
                    
    def hsGPA(self):
        grades=[]
        for c in self.hsCourses:
            grs = c.getGrades()
            if grs == None:
                pass
            else:
                grades.extend(grs)
        grades = list(filter(lambda x: x != None,grades))
        if len(grades) > 0:
            return sum(grades)/len(grades)
        else: 
            return None

#check the course sources 
    def check_all_hsCourses_from_LIST(hsCourseList):
        for e in hsCourseList:
            if e.course_source != 'LIST': return False
        return True

    def weighted_hs_Math_GPA(self):            
        w_grades = [] #[course.weightedGrade() for course in self.hsCourses]
        for course in self.hsCourses:
            if course.weightedGrade() != None:
                w_grades.append(course.weightedGrade())
        if len(w_grades)>0:
            return sum(w_grades)/len(w_grades)
        else:
            return None

    def firstMajor(self):
        if len(self.majors) > 0:
            self.majors.sort()
            return self.majors[0][1]
        else: return None
## for now
#   0 No
#   1 Yes
#   None no major or don't know
    def firstMajorSTEM(self):
        return None
    
    def max_hs_math_level(self,categories=Label_Maps.hs_label_categ):
        try:
            courses = []
            for e in self.hsCourses:
                courses.append(categories[e.course_label])
            return(max(map(lambda x: Label_Maps.hs_label_cat_ranked[x],courses)))
        except:
            print("error in took_math_beyon_alg2 "+self.sid)
            return None

## Unlike other elements of student this is meant to be modified.
#   The point of this class is to collect student application data
#   to use machine learning on.
    class HSCourse_FeatureVector:
        def __init__(self,studentData):
            self.coursesList = []

class HSCourse:
    def __init__(self,subject='Math',sid=None):
        self.sid=sid
        self.subject=subject
        self.hs_crs_nbr = None # not sure what this is
        self.hs_grade_level = None
        self.descr = None #the course name from the text file.
        self.fall_gr = None
        self.spr_gr = None
        self.summer_gr = None
        self.honors = None 
        self.sum2_gr = None
        self.High_School = None
        self.course_source =None # options seem to be "LIST" or "MANL"
        # this is the part where it actually gets alterred
        self.course_best_match=None
        self.course_label=None
        self.bestEditDist=None
       # self.weightedGrade=None

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

##
##
    def getGrades(self):
        try:
            if int(self.hs_grade_level) <9:
                return None
            grds = [self.fall_gr,
                    self.spr_gr,
                    self.summer_gr,
                    self.sum2_gr]
            actualGrades = []
            gradesmap = Label_Maps.gradesMap.copy()
            def gradeval(x):
                if x in gradesmap:
                    return gradesmap[x]
                else: 
                    return None
            grds = map(gradeval, grds)
            grds =  list(filter(lambda x: x != None, grds))
            if len(grds) == 0:
                return None
            else:
                return grds
        except:
            print(self.sid,"  getGrade failed")
            global get_grade_failed
            get_grade_failed.append(self.sid)
            return None

    def showAll(self):
        print(str(self.descr),str(self.hs_grade_level))

## Sets the course_label using the passed in function
#
    def set_course_label(self,matchfun):
        apparent_equivs = {'geometry' : 'geometry',
                'trigonometry' 'precalc' 'trig_and_precalc': 'precalc'}
        self.course_label = matchfun(self.descr)
        if self.course_label in apparent_equivs:
            self.course_label = apparent_equivs[self.course_label]

## Returns a course name. Should not be used with course match.
    def getCourseName(self):
        if self.course_label != None:
            return self.course_label
        else:
            return self.descr
## 
    def courseCategory(self,categoryDct = Label_Maps.hs_label_categ):
        return categoryDct[self.course_label]

# In general an AP course must be from a select list of courses and 
# have 'AP' somewhere in its name.
# For determining AP Calc, must have AB or BC in there.
    def isAPMath(self):
        if self.courseCategory() == 'Statistics':
            if (re.search("AP", self.descr, re.IGNORECASE) and
                self.course_label == 'stats'):
                return True
        elif self.courseCategory() == 'Calculus':
            if (re.search("AP", self.descr, re.IGNORECASE) and
                self.course_label == 'calculus' and 
                (re.search("AB",self.descr, re.IGNORECASE) or
                    re.search("BC",self.descr, re.IGNORECASE))):
                    return True
        else: 
            return False

    def weightedGrade(self):
        grades = self.getGrades()
        if (grades != None) and (len(grades)>0):
            if self.isAPMath():
                return (sum(grades)/len(grades))+1
            elif self.honors:
                return (sum(grades)/len(grades))+0.5
            else:
                return sum(grades)/len(grades)
        else:
            return None

## need a get grade func.

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
    def __init__(self,nam=None,sem=None,gra=None,un=None,sid='None'):
        gradesMap = Label_Maps.gradesMap 
        self.name = nam
        self.semester = sem # ???
        self.grade_letter = gra # str
        self.units = float(un) #??? 
        self.grade_val = None
        self.passed = 0
        self.repeat = gra == 'RP' # this course's grade got replaced
        if gra in gradesMap:
            self.grade_val = gradesMap[gra] 
            if gradesMap[gra] >= 2.0: self.passed = 1
        else:
            print("problem in course info:", sid, nam, sem, gra, un)
            self.grade_val = 0.0
            #self.units = 0

    def featureVector(self):
        return [int(self.semester), self.name, self.units, self.grade_letter]

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

