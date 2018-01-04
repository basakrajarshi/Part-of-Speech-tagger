# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 23:53:16 2017

@author: rajar
"""

import collections
from collections import Counter
import operator

file = open("berp-POS-training.txt","r").readlines()
thefile = open('test99.txt', 'w')

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

appear = ""
temp = 0
freq = 0
tag = ""
temptag =""


for line in file:
    s=line.strip().split("\t")
    if(line!="\n"):
        splitlines.append(s)
        alltags.append(s[2])
        allwords.append(s[1])
        
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

wordtagcount = Counter(allwordtags)

for j in wordtagcount:
    wordtagcountdict[j] = wordtagcount[j]
    
def probt(word):
    probtagger = {}
    newwordtag = ""
    for each in wordtagcountdict:
        t = each.strip().split(",")
        if(t[0]==word):
            probtagger[each] = wordtagcount[each]
        else:
            newwordtag = word+","+"NN"
            probtagger[newwordtag] = 1 
    tag = max(probtagger, key=probtagger.get)
    u = tag.split(",")
    probtagger = {}
    return(u[1])

for each in file:
    s=each.strip().split("\t")
    if(each!="\n"):
        thefile.write(s[0]+"\t"+s[1]+"\t"+probt(str(s[1]))+"\n")
    else:
        thefile.write("\n")