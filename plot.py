import readData as rd
import Student
import pickle
import pandas as pd
import courseMatcher as cm
from matplotlib import  pyplot as plt
#import set_operations as sop
from set_operations import *


#dataSet = sop.filter1(sop.readall())
#BIY = by incoming year
dataSet = load_data()

yrmap={ '204':'2004','205':'2005','206':'2006','207':'2007','208':'2008',
        '209':'2009','210':'2010','211':'2011','212':'2012','213':'2013',
        '214':'2014','215':'2015','216':'2016','217':'2017'}

def graduation_by_incoming_year():
    ret = partitionByRetention(dataSet)
    ret_sty=mapOverDct(ret,lambda x: startYear(x))
    d = mapOverDct(ret_sty, lambda x:mapOverDct(x,lambda y: len(y)))
    df = pd.DataFrame(d) 
    
    # need to get this sorted out. Basically need a nested dictionary to matrix
    # function that guarantees the out puts are correctly ordered. 

   # df = pd.DataFrame(col,columns=['current','dropout','grad'],index=yr)
    df = df.drop(['2016','2015','2014'])
    df['total'] = df.sum(axis=1)
    df['ret_rate'] = 100*(df['current']+df['grad'])/df['total']
    fig1 = df.plot(['ret_rate']).set_xticklabels(
            df.index.get_values())
    plt.show()
    #fig2 = df['ret_rate'].plot().set_ybound(0,100)
    #plt.show()
    return df 

def first_class_pass_rate_BIY():
    stydct = mapOverDct(startYear(dataSet),lambda x: stlstToDct(x))
    return


def gpa_freshmen_by_year_retention(data):
    d = partitionByRetention(data) 
    d2 = mapOverDct(d,lambda x: startYear(x))
    d3 = mapOverDct(d2,lambda x: mapOverDct(x,lambda y: stlstToDct(y)))
    d4 = mapOverDct(d3,groupGPA)
    df = pd.DataFrame(d4)
    df.plot().set_xticklabels(df.index.get_values())
    plt.show()
    return df

