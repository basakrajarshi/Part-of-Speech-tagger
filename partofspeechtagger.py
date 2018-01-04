# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 01:52:54 2017

@author: rajar
"""

import collections
from collections import Counter
import operator
file = open("berp-POS-training.txt","r").readlines()
outputfile = open("outputthisset.txt", 'w')
inputfile = open("testthisset.txt","r").readlines()
inputfile.append("\n")
inputfile.append("\n")
iput=""
unsortedwordtags = []
sortedwordtags = []
splitlines = []
alltags = []
allwords = []
alltagbigrams = []
allwordtags = []
wordcount = []
tagcount = []
wordtagcount = []
tagbigramcount = []
wordtagcountdict = {}
tagbigramcountdict = {}
wordcountdict = {}
tagcountdict = {}
tagbigramcounter = []
totalcountsectag = {}
bigramprob = {}
totalcountfirstword = {}
wordtagprob = {}
probtagger = {}
probtag = {}
uniquetags = []
extrawordtagprobdict = {}
firstwords = []
occursonce = {}
sentendtag = []
smoothedprob = {}
wordandtagdict = {}
countlines = 0 

alltags.append('<s>')
allwords.append('<s>')
for line in file:
    s=line.strip().split("\t")
    if(line!="\n"):
        splitlines.append(s)
        alltags.append(s[2])
        allwords.append(s[1])
        wordandtagdict[s[1]] = s[2] 
    else:
        countlines += 1
        alltags.append('<es>')
        allwords.append('<es>')
        alltags.append('<s>')
        allwords.append('<s>')
alltags.append('<es>')
allwords.append('<es>')

for i in range(0,len(splitlines)):        
    unsortedwordtags.append(splitlines[i][1:3])
sortedwordtags = sorted(unsortedwordtags, key=lambda x: x[0])

wordcount = Counter(allwords)
for i in wordcount:
    wordcountdict[i] = wordcount[i]
    
tagcount = Counter(alltags)
for i in tagcount:
    tagcountdict[i] = tagcount[i]

for j in sortedwordtags:
    allwordtags.append(j[0] + "," + j[1])

allwordtags.append(str(".,<es>"))

wordtagcount = Counter(allwordtags)

for j in wordtagcount:
    wordtagcountdict[j] = wordtagcount[j]

for j in range (len(alltags)-1):
    if (alltags[j]!= "."):
        alltagbigrams.append(alltags[j] + "," + alltags[j+1])
        
tagbigramcount = Counter(alltagbigrams)

for k in tagbigramcount:
    tagbigramcountdict[k] = tagbigramcount[k]
    
for i in tagcount:
    totalcountsectag[i] = 0
    
for j in tagbigramcount:
    bigramprob[j] = 0
    
for each in tagcount:
    for every in tagbigramcountdict:
        p = every.strip().split(",")
        if each == p[1]:
            totalcountsectag[p[1]] += tagbigramcountdict[every]

for each in totalcountsectag:
    for every in tagbigramcountdict:
        r = every.strip().split(",")
        if each == r[1]:
            bigramprob[every] = tagbigramcountdict[every] / totalcountsectag[each]

for j in wordcount:
    totalcountfirstword[j] = 0
    
for j in wordtagcount:
    wordtagprob[j] = 0
    
for each in wordcount:
    for every in wordtagcountdict:
        q = every.strip().split(",")
        if each == q[0]:
            totalcountfirstword[q[0]] += wordtagcountdict[every]

for each in totalcountfirstword:
    for every in wordtagcountdict:
        s = every.strip().split(",")
        if each == s[0]:
            wordtagprob[every] = wordtagcountdict[every] / totalcountfirstword[each]
            
q = []

for i in range(0,len(file)):
    if(i==0):
        p = file[i].strip().split("\t")
        q.append(p[2])
    if(file[i]!="\n"):
        p = file[i].strip().split("\t")
    else:
        s = file[i+1].strip().split("\t")
        q.append(s[2])

sentstart = Counter(q)
startbigramprobdict = {}

for k in sentstart:
    startbigramprobdict["<s>"+","+k] = sentstart[k]/len(q)

r = []

for i in range(0,len(file)):
    if(file[i]!="\n"):
        continue
    else:
        if(file[i-2]!="\n"):
            s=file[i-2].strip().split("\t")
            r.append(s[2])
sentend = Counter(r)
endbigramprobdict={}
for f in sentend:
    endbigramprobdict[f+","+"<es>"] = sentend[f]/len(r)
    
extrawordtagprobdict["<s>,<s>"] = 1
extrawordtagprobdict["<es>,<es>"] = 1

bigramprob.update(startbigramprobdict)

bigramprob.update(endbigramprobdict)

for k in tagcountdict:
    uniquetags.append(k)
    
for i in wordcountdict:
    w = i+",<es>"
    extrawordtagprobdict[w] = 0
    
for i in wordcountdict:
    w = i+",<s>"
    extrawordtagprobdict[w] = 0
    
for i in wordcountdict:
    w = "<s>,"+i
    extrawordtagprobdict[w] = 0
    
for i in wordcountdict:
    w = "<es>,"+i
    extrawordtagprobdict[w] = 0
    
wordtagprob.update(extrawordtagprobdict)

for i in wordtagcount:
    if wordtagcount[i] == 1:
        occursonce[i] = wordtagcount[i]
for line in range(len(file)):
    if(file[line] == "\n"):
        t = file[line-1].strip().split("\t")
        k = t[2]+",<es>"
        sentendtag.append(k)
        
bigramprob[".,<es>"] = 1

wordtagcountdict[".,<es>"] = 1

unknown = [] #has all 87 uniquewords appearing once
udict={} #has all pairs of unique words and tags

for j in wordcount:
    if (wordcount[j] == 1):
        unknown.append(j)
for each in unknown:
    if each in wordandtagdict:
        udict[each]=wordandtagdict[each]
        
unkdict = Counter(udict.values())

val1 = 0
mostfrequnk = ""
for i in unkdict:
    if (val1 < unkdict[i]):
        mostfrequnk = i
        val1 = unkdict[i]

#-----------------------------------------------------------------------
#----------------------------Function for smoothing---------------------
#-----------------------------------------------------------------------
        
def probsmoother(word,tag):
    k = 0.05
    c = word+","+tag
    if c in wordtagprob:
        res = wordtagprob[c]*totalcountfirstword[word]
    else: 
        res = 0
    prob = (res + k)/(totalcountfirstword[word] + (k*len(wordcount)))    
    return prob

#-----------------------------------------------------------------------
#------Function that updates the first column of the Viterbi matrix-----
#-----------------------------------------------------------------------

def firstcol(word,tag):
    c = word+","+tag
    d = "<s>"+","+tag
    if c in wordtagprob:
        res =1*probsmoother(word,tag)
    elif(word not in allwords  and tag == mostfrequnk):
        res = 1
    else:
        res = 0
    if d in bigramprob:
        res2=bigramprob[d]
    else:
        res2=0
    return res*res2

#-----------------------------------------------------------------------
#-Function that updates all the subsequent columns of the Viterbi matrix
#-----------------------------------------------------------------------

def othercol(word,tag,s):
    e = word+","+tag
    d = []
    f = {}
    if e in wordtagprob:
        re =1*probsmoother(word,tag)
    elif(word not in allwords  and tag == mostfrequnk):
        re = 1
    else:
        re = 0
    for j in uniquetags:
        va = j+","+tag
        v = 0
        if va in bigramprob:
            v = re*bigramprob[va]*fortrell[uniquetags.index(j)][s-1][0] 
            f[va] = v 
        else:
            f[va] = 0
        d.append(v)
    
    g = max(f.items(), key=operator.itemgetter(1))[0]
    backPointer = d.index(f[g])
    
    back = g.split(",")
    bp = str(f[g])+","+back[1]
    return (bp,backPointer) 

#-----------------------------------------------------------------------
#-------------Function for Viterbi Algorithm----------------------------
#-----------------------------------------------------------------------

def viterbi(sent):
    for each in range(len(sent)):
        if each==0:
            for i in range(len(fortrell)):
                fortrell[i][each] = [firstcol(sent[each],uniquetags[i]), uniquetags[i], 0]
            
        else:
            for j in range(len(fortrell)):
                (ab,backpoint) = othercol(sent[each],uniquetags[j], each)
                cd = ab.split(",")
                maxim = float(cd[0])
                fortrell[j][each] = [maxim, cd[1], backpoint]
    
    maxvar = 0
    maxind = 0
    for j in range (len(fortrell)):
        if (maxvar < fortrell[j][len(sent)-1][0]):
            maxvar = fortrell[j][len(sent)-1][0]
            maxind = j
            
    sentword = []
    senttag = []
    backitr = maxind
    for i in range(len(sent)-1,-1,-1):
        finalthing = fortrell[backitr][i]
        finaltag = finalthing[1]
        sentword.append(sent[i])
        senttag.append(finaltag)
        backitr = fortrell[backitr][i][2]
        
    finalsentword = []
    finalsenttag = []
    for k in range(len(senttag)-1,-1,-1):
        finalsentword.append(sentword[k])
        finalsenttag.append(senttag[k])
    return (finalsentword,finalsenttag)

#-------------------------------------------------------------------
#------------Generating the output file from the input--------------
#-------------------------------------------------------------------

arrayofSent=[]
for a1 in inputfile:
    ip=a1.strip(" ").strip("\n").split("\t")
    if (a1 != "\n"):
        iput = iput + ip[1] + " "
    else:
        iput=iput.rstrip(" ")
        arrayofSent.append(iput)
        iput = ""
sent=[]    
for each in arrayofSent:
    wordout = []
    tagout = []
    words = each.split(" ")
    for j in words:
        sent.append(j)
    fortrell = [[0 for x in range(len(sent))] for y in range(len(uniquetags))]
    (wordout,tagout) = viterbi(sent)
    for count in range(len(wordout)):
        outputfile.write(str((count+1))+"\t"+wordout[count]+"\t"+tagout[count]+"\n")
    sent = []
    wordout = []
    tagout = []
    outputfile.write("\n")
    


  

