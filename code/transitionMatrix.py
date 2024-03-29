import Student
import readData as rd
#import analysis as an
import pandas as pd
#import numpy as np
# I merged everything from here into printData.py so you guys can just ignore
# this.

#def add_student_to_transitMatrix(student,term1,term2,tt=term_transition):
#    for cname1 in term1:
#        if not(cname1 in tm): tt[cname1] = {}
#        for cname2 in term2:
#            if cname2 in tm[cname1]: tt[cname1][cname2] +=1
#            else: tt[cname1][cname2] = 0
#    return tt


def termTransitionSeries(numTerms):
    term = 'term'
    terms=[]
    transitions = []
    for e in range(1,numTerms+1):
        terms.append(term+str(e))
    for i in range(numTerms-1):
        transitions.append([terms[i],terms[i+1]])
    return transitions

def transitionMat(dataSet):
    
    def addToTM(t_c,term1,term2,transition):
        if not(term1 in t_c) or not(term2 in t_c):
            return transition

        t1_courses = t_c[term1]
        t2_courses = t_c[term2]
        for course1 in t1_courses:
            if not(course1 in transition): transition[course1] = {}
            for course2 in t2_courses:
                if course2 in transition[course1]:
                    transition[course1][course2] += 1
                else:
                    transition[course1][course2] = 1
        return transition

    transitions = {}
    maxterms = 0
    student_term_courses = {}
    termTrans = []
    for s in dataSet:
        if dataSet[s].number_of_terms() > maxterms: 
            maxterms = dataSet[s].number_of_terms()
        student_term_courses[s] = dataSet[s].courses_by_term()
    
    termTrans = termTransitionSeries(maxterms)

    for tpre,tnext in termTrans:
        transName = tpre+'_to_'+tnext
        transitions[transName] = {}
        transit = transitions[transName]
        for stdnt,terms_courses in student_term_courses.items():
            transit = addToTM(terms_courses,tpre,tnext,transit)
    return transitions

def transitionsList(transmat):
    lines = []
    transitions = []
    for k1,vct in transmat.items():
        for k2,val in vct.items():
            transitions.append([val,k1,k2])
    transitions.sort()
    for e in transitions:
        lines.append(e[1]+'['+str(e[0])+']_'+e[2]+'\n')
    f = open('transitions.txt','w')
    f.writelines(lines)
    f.close()

def merge10Terms(transmat):
    mergedTrans = {}
    for term,termTrans in transmat.items():
        for start_course,to_courses in termTrans.items():
            if not(start_course in mergedTrans):
                mergedTrans[start_course] = {}
            for end_course,num in to_courses.items():
                if end_course in mergedTrans[start_course]:
                    mergedTrans[start_course][end_course] += num
                else: 
                    mergedTrans[start_course][end_course] = num
    return mergedTrans
