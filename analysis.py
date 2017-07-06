import readData as rd
import Student
import pickle
import pandas as pd

def readall():
    data = {}
    data = rd.read_Large_HS(dictionary=data)
    data = rd.read_College_Seq(dct=data)
    data = rd.read_Progress(dct=data)
    return data


def filter(data):
    filtered_data = {}
    for s in data:
        st = data[s]
        #if ((len(st.hsCourses)>0) and (len(st.collegeSeq)>0) and
        #        st.is_californian() and (st.first_term != None)
        #        and (st.last_term != None) and (st.grad_term != None)):
        if (len(st.hsCourses)>0 and len(st.collegeSeq)>0 and                
                (st.first_term != None)):
            filtered_data[s] = st
    return filtered_data

def filter2(data):
    l = {}
    for s in data:
        st = data[s]
        if len(st.hsCourses) > 0:
            if len(st.collegeSeq) > 0:
                l[s] = st
    return l

def save(dct):
    with open("datafile.txt","wb") as f:
        pickle.dump(dct, f)

def load_data():
    with open("datafile.txt","rb") as f:
        return pickle.load(f)


## take N from dictionary and return as list.
def TakeN(dct,num=100):
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

