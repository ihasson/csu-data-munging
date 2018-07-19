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
from fuzzywuzzy import StringMatcher as strmat

#note: precalc equivalencies may be subject to change.
apparent_equivs = {'geometry' : 'geometry',
        'trigonometry' 'precalc' 'trig_and_precalc': 'precalc'}

calculusReadiness = {'calculus' 'tigonometry' 'precalc' 'trig_and_precalc'
        'math_anal' :'calculus ready',
        'algebra2' 'algebra1' 'adv_math' 'geometry''adv_app_math' 
        'alg_trig' :'Not calculus ready',
        'bad' 'discrete_math' 'accounting' 'stats' 'bade' 'prob' 'geo_alg_trig' 
        'inter_alg' :'unknown',
        'no_math':'no_math'}

# this is probably no longer needed.
def levenshteinDist(stringA,stringB):
    try:
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
    except TypeError:
        print("stringA" + stringA)
        print("stringB" + "")

# This one should be deprecated now and probably needs to be removed.
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
                #print( cname +"\t" + closest )
    return dataset

## does some cleaning on text to reduce how much needs to be dealt with.
def justClean(string):
    try:
        cname = string
        cname = cname.replace('IV','4')
        cname = cname.replace('III','3')
        cname = cname.replace('II','2')
        cname = cname.replace('iii','3')
        cname = cname.replace('ii','2')
        cname = cname.lower()
        cname = re.sub("\(.*\)","",cname)
        cname = re.sub("common core","",cname)
        cname = re.sub("honors","",cname)
        cname = re.sub("ap ","",cname)
        cname = re.sub("h(\.)? ","",cname)
        cname = cname.strip()
        return cname
    except:
        print(string)

## need to define a normal form for english descriptions.
# Best idea so far:
#  (AP/Honors/IB) (bulk of name) (level i.e. number)
def cleanEnglish(string):
    cname = string
    cname = cname.lower()
    # roman numerals
    cname = re.sub(r"iv\W?([ab]$)",r"4 \1",cname)
    cname = re.sub(r"iii\W?([ab]$)",r"3 \1",cname)
    cname = re.sub(r"ii\W?([ab]$)",r"2 \1",cname)
    cname = re.sub(r"i\W?([ab]$)", r"1 \1",cname)

    cname = re.sub(r"\siv(\s|$|\W)",r" 4\1",cname)
    cname = re.sub(r"\siii(\s|$|\W)",r" 3\1",cname)
    cname = re.sub(r"\sii(\s|$|\W)",r" 2\1",cname)
    cname = re.sub(r"\si(\s|$|\W)", r" 1\1",cname)
    cname = re.sub("\(.*\)","",cname)
    cname = re.sub("common core","",cname)
    cname = re.sub("honors","",cname)
    cname = re.sub("ap ","",cname)
    cname = re.sub("a[\\\ +)(/,s-]b",r"ab",cname)
    cname = re.sub(r"([0-9])([a-zA-Z]{2})$",r"\1 \2",cname)

#    cname = re.sub("h(\.)? ","",cname)
    
    # The next part is to check for substrings definitely indicating "honors".
    # If any or maybe exactly one of these checks is true then remove the
    # indicating substring and then place '(honors)' at the front of the course 
    # name.

    #very few examples of ap courses where "AP" not in beginning.
    #cname = re.sub(r"ap (eng|lang|lit)(.*)",r"AP \1\2",cname)
    #maybe should rather capture the 

    cname = re.sub("\(.*\)$","",cname)
    cname = re.sub(r"^h ","",cname)
    cname = re.sub(r"([0-9])([a-zA-Z]{2})$",r"\1 \2",cname)
    cname = re.sub(r"\s\s+",r"\s",cname)
    cname = cname.strip() 
    return cname

## I think this is deprecated but not sure.
#   Takes a string and finds the closest match from a list of strings.
# Params: 
#    string : the thing you want to match to
#    maxDist    : the maximum allowable distance
#   cantFind    : the return string for when nothing is closer than maxDist
#   listOfNames : the list of course names
def findClosest(string, maxDist=7, cantFind="unknown", listOfNames=None):
    if listOfNames == None:
        knownclasses = ['algebra 1', 'algebra 2', 'geometry', 'calculus',
                    'pre-calculus', 'trigonometry', 'statistics',
                    'math analysis', 'trig/alg', 'alg/trig', 'algebra']
    else: knownclasses = listOfNames 
    bestMatch = cantFind
    bestdistance = maxDist
    for c in knownclasses:
        dist = levenshteinDist(c,string) 
        if dist < bestdistance :
            bestdistance = dist
            bestMatch = c
        if bestdistance == 0: break
    return bestMatch

## same as find closest but also returns distance
def findClosest_wd(string, maxDist=7, cantFind="unknown", listOfNames=None):
    if listOfNames == None:
        knownclasses = ['algebra 1', 'algebra 2', 'geometry', 'calculus',
                    'pre-calculus', 'trigonometry', 'statistics',
                    'math analysis', 'trig/alg', 'alg/trig', 'algebra']
    else: knownclasses = listOfNames 
    bestMatch = cantFind
    bestdistance = maxDist
    for c in knownclasses:
        dist = strmat.distance(c,string) 
        if dist < bestdistance :
            bestdistance = dist
            bestMatch = c
        if bestdistance == 0: break
    return bestMatch,bestdistance

def generate_overfit_map():
    verimap = {}
    with open('data/uniqNames.txt', 'r') as f:
        for line in f:
            categ,name = line.split(',')
            categ = categ.strip()
            name = name.strip()
            verimap[name] = categ
    verimap['unknown'] = 'unknown'
    return verimap

#if the proportion of the edit_distance is to large compared to the shorter of 
#the two words then we don't want it.
def satisfies_length_ratio_rule(word1,word2,edit_dist,ratio=1/4):
    def shorter(word1, word2):
        if len(word1) < len(word2): return word1
        else: return word2

    length_diff = abs(len(word1) - len(word2))
    shorter_word = shorter(word1,word2)
    
    return not(edit_dist >= len(shorter_word)*ratio)



#need to add some way to add per label rules more easily
def construct_matchfun():
    courseDct= generate_overfit_map()
    improvedCourseDct={}
    for oldcname in courseDct:
        newcname = justClean(oldcname)
        improvedCourseDct[newcname] = courseDct[oldcname]
    namelist=list(improvedCourseDct)
    print(namelist)
    def func(x): 
        if x in courseDct:
            return courseDct[x]
        modName = justClean(x)
        if modName == 'm': 
            return 'old_data'
        if modName in improvedCourseDct:
            return improvedCourseDct[modName]
        #print(bestMatch)
        bestMatch,distance = findClosest_wd(modName, 
                maxDist=6,listOfNames=namelist)

# check various rules for validity of bestMatch
        #new rule checking against length
        # removed because too late and too little impact.
        # i.e. the course matching was fine before.
        if not(satisfies_length_ratio_rule(modName,bestMatch,distance,1/4)):
            return 'unknown'
        # have to guard algebra2 against algrebra 1
        if improvedCourseDct[bestMatch] == 'algebra2':
            if (modName.find('1') > -1) or (modName.find('2') < 4):
                print("%s   is bad" % modName)
                improvedCourseDct[modName] = 'bad'
                return 'bad'
            else:
                return 'algebra2'
        elif distance < 3:
            improvedCourseDct[modName] = improvedCourseDct[bestMatch]
            #print(modName,bestMatch,str(distance))
            return improvedCourseDct[bestMatch]
        elif distance < 6:
            print("Best Match of    %s     is to    %s    with dist= %d" 
                    % (x, bestMatch, distance))
            return improvedCourseDct[bestMatch]
        print("No Match Found   %s" % x)
        return 'unknown'
    return func
