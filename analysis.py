from set_operations import *
import pickle

def gpa_freshmen_by_year_retention(data):
    d = partitionByRetention(data) 
    d2 = mapOverDct(d,lambda x: startYear(x))
    d3 = mapOverDct(d2,lambda x: mapOverDct(x,lambda y: stlstToDct(y)))
    d4 = mapOverDct(d3,groupGPA)
    return pd.DataFrame(d4)

# the explanation for why my data had more people was that it did not filter out
# transfer students?
def graduation_by_incoming_year(dataSet) -> "could be freshmen or transfer":
    ret = partitionByRetention(dataSet)
    ret_sty=mapOverDct(ret,lambda x: startYear(x))
    d = mapOverDct(ret_sty, lambda x:mapOverDct(x,lambda y: len(y)))
    df = pd.DataFrame(d) 
    
   # df = pd.DataFrame(col,columns=['current','dropout','grad'],index=yr)
    #df = df.drop(['2016','2015','2014'])
    df['total'] = df.sum(axis=1)
    df['ret_rate'] = 100*(df['current']+df['grad'])/df['total']
    df['grad_rate'] = 100*df['grad']/df['total']
    df['drop_rate'] = 100*df['drop']/df['total']
    df['current_rate'] = 100*df['current']/df['total']
    return df

# figure out why cohort term differs from start term

def weird_start(dataSet):
    d = and_filter(dataSet,[lambda x: int(x.cohort_term) - int(x.first_term)>10])
    return d
