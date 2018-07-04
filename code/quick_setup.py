import pandas as pd
from matplotlib import pyplot as plt
import re
import csv
from stuff_for_prof import *

def desiredterm(x): 
    return( (int(x.term) >= 2040) and (str.endswith(str(x.term),'7')))

gpas = pd.read_csv("data/hsgpa.csv",quoting=csv.QUOTE_NONE)
gpas.set_index('sid',inplace=True)
cohorts = pd.read_csv("data/cohorts.txt",sep='|',quoting=csv.QUOTE_NONE)
ftf = cohorts[cohorts['cohort']=='FTF']
ftf.set_index("studentid",inplace=True)
ftf = ftf.join(gpas)
df = pd.DataFrame(big_table(DATASET))

