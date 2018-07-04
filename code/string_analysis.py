import matplotlib.pyplot as plt
from fuzzywuzzy import StringMatcher as strmat
import re
import difflib as dl
from fuzzywuzzy import process
import sys
#this takes two list of strings and returns a list of nearest points
# and returns the array of initialpositions.
# The initialposition array lines up with the dataset array.

filelist1 = ["Taft-12thgrade-mathcourses.txt",
        "Grant-12thgrade-mathcourses.txt",
        "Poly-12thgrade-mathcourses.txt"]
centroids1 = ["algebra 1", "algebra 2", "calculus", "precalculus",
        "trigenometry","geometry", "statistics", "adv app math ab",
        "geo & alg/tr ab", "discrete math","english lit", "history",
        "not math"]
filelist2 = ["tmp.txt"]

# need to eliminate Elt because it is cancer.
class Elt:
    pass

#need to better structure data set and standardize usinig objects
# 
class Element :
    def __init__(self, string):
        #print( string)
        self.string = string

    def setNum(self, num):
        self.num = num

    def getString(self):
        return self.string

    def getNum(self) :
        return self.num 

class Cluster :

# for this implementation the centroid isn't considered an element
# so when computing a new centroid the element that becomes the new 
# centroid must 
    def __init__(self, centroid):
        self.centroid = str(centroid)
        self.elts = []
    
  #  def add_element(self, newElement, distance):
    #     self.elts.append((newElement,distance))
    
    def add_element(self, newString):
        newelt = Element(newString)
        newelt.setNum(self.editDist(newelt.string))
        self.elts.append(newelt)

    def editDist(self, string):
        a = self.centroid
        return strmat.distance(a, string)
    
    def avgDist(self):
        sumOfDistances = 0
        for e in self.elts :
            sumOfDistances += e.getNum()
        return float(sumOfDistances) / float(len(self.elts))
    
    def find_medoid(self) :
        bestCentroid = None
        avgDistForCentroid = 9001
        for x in self.elts :
            currentCentroid = Cluster(x.getString())
            for y in self.elts :
                currentCentroid.add_element(y.getString())
            curAvgD = currentCentroid.avgDist()
            if avgDistForCentroid >= curAvgD :
                bestCentroid = x.getString()
                avgDistForCentroid = curAvgD
        return bestCentroid
            


def kluster(dataset, initialPositions):
    clusters = []
    for item in dataset :
        bestCenter = None
        for centroid in initialPositions :
            cent = dl.SequenceMatcher()
            cent.set_seqs(centroid,item)
            distance = cent.ratio()
            distance = strmat.distance(centroid,item)*(1 - distance)
            if bestCenter == None :                
               bestCenter = (distance,centroid)
            else: 
               if bestCenter[0] >= distance :
                   bestCenter = (distance, centroid)
        clusters.append(bestCenter)
    return clusters

        

#def levenshteinDistance(stringA, stringB):
def levenshteinDist(stringA,stringB):
    matrix = [[None for col in range(0,len(stringB)+1)] 
                for row in range(0,len(stringA)+1)]
    for col in range(0,len(stringB)+1,1) :
        matrix[0][col] = col
    for row in range(0,len(stringA)+1,1) :
        matrix[row][0] = row

    for col in range(1,len(stringB)+1) :
        for row in range(1,len(stringA)+1):
            l = 1 if stringB[col-1] != stringA[row-1] else 0
            up = matrix[row][col-1] +1
            left = matrix[row-1][col] +1
            upleft = matrix[row-1][col-1] + l
            matrix[row][col] = min((upleft,up,left))
   
    #print(matrix) 
    a = matrix[len(stringA)][len(stringB)]
    #print( a)
    return a

def getData(filelist):
    dataset = []
    for fname in filelist :
        with open(fname, 'r') as f:
            for line in f:
                #format
                line = line.rstrip()
                vals = line.split(',')
                #course = Elt()
                #course.name = str.lower(vals[0])
                #course.numStudents = vals[1]
                #course.school = fname
                #course.centroid = ""
                #dataset.append(course)
                dataset.append(str.lower(vals[0]))
    return dataset

#takes a
def getDistances(medians,dataset):
    l = len(dataset)
    distanceMatrix = []
    for m in medians:
        column = []
        for row in range(l):
            column.append(strmat.distance(m,dataset[row]))
        distanceMatrix.append((m,column))
    return distanceMatrix        
#bug is because dictionary deduplicates
#takes dictionary of integer arrays
def avgDistances(data):
    avgs = []
    n = len(data)
    print(n)
    for e in data:
        avgs.append((float(sum(e[1]))/n , e[0]))
    return avgs

def cluster1(): 
    filelist = filelist2
    centroids = centroids1

    data = getData(filelist)
    names = []
    for elt in data :
        names.append(elt.name)
    nearestList = kluster(names, centroids)
    for num in range(0,len(data)) :
        a = data[num]
        a.centroid = nearestList[num]
    
    return data

def findWorst():
    results = cluster1()
    ls = []
    for e in results:
        ls.append((e.centroid[0],e))
    ls.sort()
    newresults=[]
    for e in ls :
        newresults.append(e[1])
    for e in newresults :
        print( e.name +"      "+e.centroid[1] +" "+ str(e.centroid[0]))

# find most common by 5 nearest neighbors
def cluster2():
    filelist = filelist2
    data = getData(filelist)
    names = []
    for elt in data :
        names.append(elt.name)
    
    results=[]
    for n in names:
        results.append(process.extract(n,names,limit=5))
    results = [e[0] for sublist in results for e in sublist]
    results.sort()
    tail = [i for i in results]
    head = tail.pop()
    count = 1
    newlist = []
    for t in tail :
        if t == head :
            count = count + 1
        else :
            newlist.append((count,head))
            head = t
            count = 1

    return newlist

def runKMedoids():
    filelist = filelist2
    stringlist = getData(filelist)
    return kmedoids(stringlist, centroids1, 25)

def kmedoids(list_of_strings,starting_centroids, iterations):
    print( starting_centroids)
    if iterations == 0:

        return starting_centroids
    else :
        resultMedoids = []
        centroids = [] 
        for s in starting_centroids :
            centroids.append(Cluster(s))
        for s in list_of_strings :
            bestCent = None
            bestDist = sys.maxsize
            for c in centroids :
                distance = c.editDist(s.name)
                if distance < bestDist:
                    bestCent = c
                    bestDist = distance
            bestCent.add_element(s.name) 
            #print( str(bestDist) +"  " + bestCent.centroid)
        for c in centroids :
            resultMedoids.append(c.find_medoid())
        return kmedoids(list_of_strings, resultMedoids, iterations-1)
    

def tokenize(cnames):
    tokenized = [] # should pick better names
    for c in cnames:
        c = c.replace("II","2")
        c = c.lower()
        tokens = c.split(" ")
        tokenized.append(tokens)
    return tokenized 

def uniquetokens(tokenMatrix):
    ls = []
    for a in tokenMatrix:
        for t in a:
            ls.append(t)
    #ls = ls.sort()

    features={}
    result = []
    c = ls[0]
    features[c] = ls[0]
    dummyVar = 0
    for b in ls:
        if b in features.keys():
            dummyVar += 1
        else: 
            features[b] = b
            result.append(b)
    return result

def tabulateTokenIntersection():
    cnames= tokenize(extractHSCourseNames())
    tokenlist = uniquetokens(cnames)
    tab = np.tile(0,(len(tokenlist),len(tokenlist)))
    for i in range(len(tokenlist)):
        for j in range(len(tokenlist)):
            for e in cnames:
                imatch = False
                jmatch = False
                for f in e:
                    if f == tokenlist[i] and f == tokenlist[j]:
                        print(f)
                    if f == tokenlist[j]:
                        jmatch = True
                    if f == tokenlist[i]:
                        imatch = True
                if imatch and jmatch:
                    tab[i,j] = tab[i,j] + 1
    return tab,tokenlist
