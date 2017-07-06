import pandas as pd
import three_school_anal as tsa
import readData as rd
import courseMatcher as cm
import Student

data = tsa.make_string_dist_table(rd.constructDictionary())

def look_at_calc(datafram):
    calc = datafram.loc[lambda x: x.label == 'calculus',:]
    c = list(calc.index)
    c.append('freq')
    return calc.loc[:,c]


def compare_to_not_calc(datafram):
    calc = datafram.loc[lambda x: x.label == 'calculus',:]
    notCalc = datafram.loc[lambda x: x.label != 'calculus',:]
    nc = list(notCalc)
    return calc.loc[:,nc]

#def avg_dist(datafram):
#    it

# need to compute weighted avg distance.
