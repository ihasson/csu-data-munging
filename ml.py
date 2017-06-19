# taken off from readData.py
#
#From here on everything is in trying to machine-learn to read course names
#
#Note this should be useful
def extractHSCourseNames(filenames=['encrypted-poly-grades.txt']):
    cnames = []
    for fname in filenames:
        with open(fname,'r') as f:
            for line in f.readlines():
                head,vals = line.split("==|")
                vals = vals.split("|")
                # remove the first part so that position mod4=0
                for i in range(int(len(vals)/4)):
                    cnames.append(vals[4*i])
    return cnames

def tokenizeMultiple(cnames):
    tokenized = [] # should pick better names
    for c in cnames:
        c = c.replace("II","2")
        c = c.lower()
        tokens = c.split(" ")
        tokenized.append(tokens)
    return tokenized

def tokenize(cname):
    c = cname.replace("II","2")
    c = c.lower()
    tokens = c.split(" ")
    return tokens

def uniqueTokens(tokenMatrix):
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
    cnames= tokenizeMultiple(extractHSCourseNames())
    tokenlist = uniqueTokens(cnames)
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

def tokenDict(inList):
    tokens = uniqueTokens(inList)
    d = {}
    for k in tokens:
        d[k] = 0
    return d

# Takes the course names from some files and creates a matrix 
# (currently some nested dictionaries) consisting of the count of each 
# lexeme to each course
def token_cmatch(
                filenames=['encrypted-poly-grades.txt'],
                cnameDict=hsClassesDict
                 ): 
    #get the strings from the files
    uncleanCNames = []
    for fname in filenames:
        with open(fname,'r') as f:
            for line in f.readlines():
                head,vals = line.split("==|")
                vals = vals.split("|")
                # remove the first part so that position mod4=0
                for i in range(int(len(vals)/4)):
                    uncleanCNames.append(vals[4*i])

    print(uncleanCNames[0])
    tkMat = tokenizeMultiple(uncleanCNames)
    uniq_tks = uniqueTokens(tkMat)
    tkdict = tokenDict(uniq_tks)
    
    # take the dictionary of coursenames which countains non-unique
    # courses and construct a list of unique courses 
    # e.g. make a course name equivalency map and initialize 
    # courseToken dictionary
    cTDict = {} #dict w/ the counts I want to be converted to matrix later 
    eqMap = {} # map coursenames to coursenames of equivalentcourses
    seenInt = {}
    for cnKey in cnameDict.keys():
        cnumb = cnameDict[cnKey] #the identifying number to find uniqueness
        if cnumb in seenInt: 
            eqMap[cnKey] = seenInt[cnumb]
        else: # haven't seen anything equivalent yet
            seenInt[cnumb] = cnKey
            cTDict[cnKey] = tokenDict(uniq_tks)
    lsOCnames = list(cnameDict.keys()) 
    for cn in uncleanCNames:
        #need to break down and fix this line
        currentCourse = cTDict[eqMap[courseMatcher.findClosest(courseMatcher.justClean(cn),listOfNames=lsOCnames)]]
        t_arr = tokenize([cn])
        for t in t_arr: 
            currentCourse[t] = currentCourse[t] + 1
    
    return cTDict
