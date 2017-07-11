import readData as rd
import Student
import pickle
import pandas as pd
import courseMatcher as cm
from matplotlib import  pyplot as plt
import setOperations as sop

dataSet = anal.filter1(anal.readall())

def graduation_by_incoming_year():
    staryY = sop.startYear(dataSet)

    stydct=mapOverDct(startY,lambda x:stlstToDct(x)
    d = mapOverDct(stydct,lambda x: partitionByRetention(x))
    col=[]                                                           
    yr = []     
    for y in d:       
        print(y)                 
        yr.append(y)
        row = []
        for c in d[y]:
            row.append(len(d[y][c]))
            print(c,len(d[y][c]))
    df = pd.DataFrame(col,columns=['current','dropout','grad'],index=yr)
    df.plot()
    plt.show()

