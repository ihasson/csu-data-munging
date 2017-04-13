# This script reads data and strips some of the irrelevant crap from
# the the second field. Also finds best match from a list. 
#
#    Copyright (C) 2017 Izzy Hasson <izzy.hasson.925@my.csun.edu>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 


#from fuzzywuzzy import StringMatcher as strM
import re
import sys

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
   
    #print matrix 
    a = matrix[len(stringA)][len(stringB)]
    #print a
    return a

# read data and also find what appears to be the closest match for the 
# course name.
def readAndClean(fileList):
    dataset = []
    for fname in fileList:
        with open(fname,'r') as f:
            for line in f:
                vals = line.split('|')
                cname = vals[1]
                cname = cname.replace('II','2')
                cname = cname.lower()
                cname = re.sub("\(.*\)","",cname)
                cname = re.sub("common core","",cname)
                cname = re.sub("honors","",cname)
                cname = re.sub("ap ","",cname)
                cname = re.sub("h(\.)? ","",cname)
                cname.strip()
                closest = findClosest(cname)
                dataset.append((vals,cname,closest))
                print( cname +"\t" + closest )
    return dataset

def justClean(string):
    cname = string
    cname = cname.replace('II','2')
    cname = cname.lower()
    cname = re.sub("\(.*\)","",cname)
    cname = re.sub("common core","",cname)
    cname = re.sub("honors","",cname)
    cname = re.sub("ap ","",cname)
    cname = re.sub("h(\.)? ","",cname)
    cname.strip()
    return cname

## 
#   Takes a string and finds the closest match from a list of strings.
#   Bounds on what is too distant can be set by changing the starting value
#   of bestdistance.
#
# The knownclasses, bestMatch, and bestdistance variables should all
# be changed to fit the needs of the user.
def findClosest(string):
    knownclasses = ['algebra 1', 'algebra 2', 'geometry', 'calculus',
                    'pre-calculus', 'trigenometry', 'statistics',
                    'math analysis', 'trig/alg', 'alg/trig', 'algebra']
    bestMatch = "unknown"
    bestdistance = levenshteinDist(bestMatch,string)
    for c in knownclasses:
        dist = levenshteinDist(c,string) 
        if dist < bestdistance :
            bestdistance = dist
            bestMatch = c
    return bestMatch

