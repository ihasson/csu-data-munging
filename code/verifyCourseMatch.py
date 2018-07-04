import courseMatcher as cm
import re
import numpy as np
import pandas

cmDefaults = ['algebra 1', 'algebra 2', 'geometry', 'calculus',
            'pre-calculus', 'trigonometry', 'statistics',
            'math analysis', 'trig/alg', 'alg/trig', 'algebra']

verimap = {}
with open('uniqNames.txt', 'r') as f:
    for line in f:
        categ,name = line.split(',')
        categ = categ.strip()
        name = name.strip()
        verimap[name] = categ

categories = ['adv_app_math', 'unknown', 'algebra1', 'algebra2', 'calculus', 
        'stats', 'geometry', 'data_science', 'discrete_math', 'geo_alg_trig', 
        'precalc', 'math_anal']
cmDefaultsMap = {'algebra 1':'algebra1', 'algebra 2':'algebra2', 
                 'geometry':'geometry', 'calculus':'calculus',
                 'pre-calculus':'precalc', 'trigonometry':"trigonometry", 
                 'statistics':'stats','math analysis':'math_anal', 
                 'trig/alg':'geo_alg_trig', 'alg/trig':'geo_alg_trig', 
                 'algebra':'unknown'}

#need to find the number of correctly labeled and incorrectly labeled
filesList = ['encrypted-grant-grades.txt','encrypted-poly-grades.txt',
                'encrypted-taft-grades.txt']

approximated = cm.readAndClean(filesList)

sample = []
correct = 0
incorrect = 0
unknowns = 0
correctUnknowns = 0
for a in approximated:
    sample.append((a[1],a[2]))
    c = a[0][1].lower()

    try:
        b1 = verimap[c]
        if b1=="unknown":
            correctUnknowns +=1
    except: 
        b1 = "unknown"
        correctUnknowns +=1
    try:
        b2 = cmDefaultsMap[a[2]]
    except: 
        b2 = "unknown"
        unknowns += 1
    if b1==b2:
        correct += 1
    else: 
        incorrect +=1
        #print(c+" :     "+b1+"  "+b2+"  "+a[1]+" "+a[2])
        if  b2 != "unknown":
            print(c+" :     "+b1+"  "+b2+"  "+a[1]+" "+a[2])
            
