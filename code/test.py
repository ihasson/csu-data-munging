def check_mergeable():
    f = open('data/good-hs-math.csv','r')
    dict1 = {}
    for l in f.readlines():
        l = l.split(",")
        if not(l[0] in dict1):
            dict1[l[0]] = l[0]
    f2 = open('data/terms-codes-graddates.txt','r')
    dict2 = {}
    for l in f2.readlines():
        l = l.split("|")
        if not(l[0] in dict2):
            dict2[l[0]] = l[0]
    dict3 ={}
    for e in dict2:
        if e in dict1:
            dict3[e] = e
    return dict1,dict2,dict3

from analysis import *

a = big_table(DATASET)
