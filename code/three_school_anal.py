import Student
import courseMatcher as cm
import readData as rd
import pandas as pd

#Want to find the following:
#prob that student has "bad outcome" in college. need to define bad outcome
#Prob that student has "bad outcome" given that they took algebra 2 in last
#year of highschool.

#need to get total

#need summary stats of how many took each course.

failed_matches = []

hs_math_files = ['encrypted-grant-grades.txt',
                 'encrypted-poly-grades.txt',
                 'encrypted-taft-grades.txt']
hsCnameMap = cm.generate_overfit_map()

#hs_data = rd.extractHSCourseNames(filenames=hs_math_files)

#student_data = rd.constructDictionary()
student_data = rd.makeStList()

#bad students list
bad_student = []
algebra = []
#703 students both applied to csun and attended from the 3 schools

#replace the list of course names using overfitmap
for student in student_data:
    replacement_courses = []
    i = 0
    for name in student.hsOldCNames:
        oldhsc = student.hsCourses[i]
        cn = hsCnameMap[str.lower(name)]
        #print(cn)
        newhsc = (cn,oldhsc[1],oldhsc[2])
        replacement_courses.append(newhsc)
        if cn == 'unknown':
            bad_student.append(student)
        if cn == 'algebra1' or cn == 'algebra2' :
            algebra.append(student)
    student.hsCourses = replacement_courses


#Checks for which students gave all grades.
#Probably has lots of bugs but don't want to bother fixing it because most
#students never inputed their grades so it's not even worth counting seriously.
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

#Only one student at a time and returns pair where the first val is grades 
#submitted and second is how many classes.
#similar to gave_all_grades but actually worth implementing
#Still treats a blank as having submitted.
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

#already has deduplication.
def count_took_course(name,st_data_arr=student_data):
    count = 0
    for st in st_data_arr:
        took = 0
        for e in st.hsCourses:
            if e[0] == name:
                took = 1
        count += took
    return count

def dataForArman():
    lines = []

    for e in student_data:
        csunmath = e.first_math()
        for c in e.hsCourses: 
            numhscourses = len(e.hsCourses)
            hsmath = c[0]
            l = "%s,%s,%s,%s,%d\n" % (
                    e.sid,hsmath,csunmath[1],csunmath[3],numhscourses)
            lines.append(l)
    return lines


## Put all hscnames(old) into data frame along with number of occurences
#   and distance from all other strings.
def make_string_dist_table(student_dict):
    allnames={} #key = name, val = numb of occurences
    fun = lambda x: cm.justClean(x).strip()
    for student in student_dict:
        for hscn in student_dict[student].hsOldCNames:
            cname=hscn #the above didn't reduce unique list much.
            if cname in allnames:
                allnames[cname] = allnames[cname] +1
            else: 
                allnames[cname] = 1
    nameslst = list(allnames)
    distmatrix=[]
    columnhdr = ['freq']
    for r in nameslst:
        distrow = [allnames[r]]
        columnhdr.append(r)
        for c in nameslst:
            a = fun(r)
            b = fun(c)
            dist = cm.levenshteinDist(a,b)
            distrow.append(dist)
        distrow.append(hsCnameMap[str.lower(r)])
        distmatrix.append(distrow)
    columnhdr.append('label')
    return pd.DataFrame(columns=columnhdr,index=nameslst,data=distmatrix)

