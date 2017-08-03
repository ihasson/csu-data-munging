# a script to make start up more convenient
import Student
import readData as rd
#from readData import save, load_data
import courseMatcher
#import pandas as pd
import set_operations as s_op
#import analysis as an
import pickle
#import importlib

def loadFTF():
    """ Loads the first time freshmen data set.
        Depends on the first time freshmen data set having already been built.
    """
    f = open("FTFpickle","rb")
    data = pickle.load(f)
    f.close()
    return data

def buildFTFDataSet():
    """ a nice function to construct the FTF data set"""
    matchFun = courseMatcher.construct_matchfun()
    data = rd.read_Large_HS()

    data = rd.read_College_Courses(dct=data)
    data = rd.read_Progress(dct=data)
    data = rd.read_Math_SAT(dct=data)
    data = rd.read_Cohorts(dct=data)
    #filtering
    data = s_op.filter_has_hs_and_college(data)
    data = s_op.and_filter(data,[lambda x: x.cohort_type == 'FTF'])
    for k,s in data.items():
        s.set_hs_course_labels(matchFun)
    # filter out students who never took a course
    dataSet1 = {}
    num_no_course =0
    for key,e in data.items():
        if e.gpa_raw() < 0:
            num_no_course += 1
        else:
            dataSet1[key] = e
    print(num_no_course," students dropped for having no gpa")
    data = dataSet1
    f = open("FTFpickle","wb")
    pickle.dump(data,f)
    f.close()
    return data


def build_BIG_DataSet():
    data = rd.readall()
    mf = courseMatcher.construct_matchfun()
    for k,s in data.items():
        if len(s.hsCourses) > 0:
            s.set_hs_course_labels(mf)
    return data
