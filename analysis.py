import readData as rd
import Student

def readall():
    data = {}
    data = rd.read_Large_HS(dictionary=data)
    data = rd.read_College_Seq(dictionary=data)
    data = rd.read_Persistance_Data(dictionary=data)
    data = rd.read_zip(dictionary=data)
    return data

def readall2():
    data = {}
    rd.read_Large_HS(dictionary=data)
    rd.read_College_Seq(dictionary=data)
    rd.read_Persistance_Data(dictionary=data)
    rd.read_zip(dictionary=data)
    return data

def filter(data):
    filtered_data = {}
    for s in data:
        st = data[s]
        #if ((len(st.hsCourses)>0) and (len(st.collegeSeq)>0) and
        #        st.is_californian() and (st.first_term != None)
        #        and (st.last_term != None) and (st.grad_term != None)):
        if (len(st.hsCourses)>0 and len(st.collegeSeq)>0 and                
                st.is_californian()):
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


