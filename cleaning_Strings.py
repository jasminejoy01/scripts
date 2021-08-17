# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:10:23 2018
@author: jjoy

First attempt at cleaning data that were entered by users in the form of strings.
Data collected: Proper Nouns (places, companies, user names) and hence contained large variations in typos.
"""

import pandas as pd
import glob, time
import numpy as np
import string, os
from fuzzywuzzy import fuzz

start_time = time.time()
path = "C:/Users/jjoy/Desktop/ListofNames"
os.chdir(path)

## Collection Array
collection =   [
    "accommodate",
"accomodation",
"achieve",
"across",
"aggressive",
"aggression",
"apparently",
"appearance",
"argument",
"assassination",
"basically",
"beginning",
"believe",
"bizarre",
"business",
"calendar",
"Caribbean",
"cemetery",
"chauffeur",
"colleague",
"coming",
"committee",
"completely",
"conscious",
"curiosity",
"definitely",
"dilemma",
"disappear",
"disappoint",
"ecstasy",
"embarrass",
"environment",
"existence",
"Fahrenheit",
"familiar",
"finally",
"fluorescent",
"foreign",
"foreseeable",
"forty",
"forward",
"friend",
"further",
"gist",
"glamorous",
"government",
"guard",
"happened",
"harass, harassment",
"honorary",
"humorous",
"idiosyncrasy",
"immediately",
"incidentally",
"independent",
"interrupt",
"irresistible",
"knowledge",
"liaise, liaison",
"lollipop",
"millennium, millennia",
"Neanderthal",
"necessary",
"noticeable",
"occasion",
"occurred, occurring",
"occurrence",
"pavilion",
"persistent",
"pharaoh",
"piece",
"politician",
"Portuguese",
"possession",
"preferred, preferring",
"propaganda",
"publicly",
"really",
"receive",
"referred, referring",
"religious",
"remember",
"resistance",
"sense",
"separate",
"siege",
"successful",
"supersede",
"surprise",
"tattoo",
"tendency",
"therefore",
"threshold",
"tomorrow",
"tongue",
"truly",
"unforeseen",
"unfortunately",
"until",
"weird",
"wherever",
"which",
    ]

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in xrange(size_x):
        matrix [x, 0] = x
    for y in xrange(size_y):
        matrix [0, y] = y

    for x in xrange(1, size_x):
        for y in xrange(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])

def stringSplit(stringIn):
    stringIn = stringIn.replace(".","")
    replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
    stringIn = stringIn.translate(replace_punctuation)
    stringIn = stringIn.lower()
    stringIn = (stringIn.rstrip()).lstrip()
    return stringIn

def levenshteinAvg(array1, collection):
    lenCheckList = []
    array1 = (array1.rstrip()).lstrip()
    array1 = stringSplit(array1)
    array1 = ' '.join(array1)
    for each in collection:
        eachSplit = stringSplit(each)
        eachSplit = ' '.join(eachSplit)
        lenCheck = levenshtein(eachSplit, array1)
        lenCheckList.append(lenCheck)
    minVal = np.nanmin(lenCheckList)
    Index = lenCheckList.index(minVal)
    replaceVal = collection[Index]
    return array1, Index, minVal, replaceVal

def clean(column, data):
    f = open("temporary.txt", "w+")
    threshold = 2
    masterList = data[column]
    masterList = list(set(masterList))

    for each in masterList:
        each = str(each)

        if each == 'nan':
            data[column]= data[column].str.replace(each, "None Found" , case = "True") 
        else:
            levenshtein_ = levenshteinAvg(each, collection)
            str1 = str(levenshtein_[0]) 
            str2 = str(levenshtein_[3])
            levenstein_index = (levenshtein_[2]) 
            
            #fuzzy match stats
            Ratio = fuzz.ratio(str1.lower(),str2.lower())
            Partial_Ratio = fuzz.partial_ratio(str1,str2.lower())
            Token_Sort_Ratio = fuzz.token_sort_ratio(str1,str2)
            Partial_Ratio2 = fuzz.partial_ratio(each.lower(),str2.lower())
            average = (Ratio+Partial_Ratio+Token_Sort_Ratio+Partial_Ratio2)/4

            #output stats
            statement = str(each) + "\t" + str1 + "\t" + str(levenshtein_[1]) + '\t' + str(levenstein_index) + '\t' + str2 + '\t' + str(Ratio) + '\t' + str(Partial_Ratio) + '\t' + str(Token_Sort_Ratio) + '\t' + str(Partial_Ratio2) + '\n'            

            #Match Adjustment
            if levenstein_index <= threshold:
                data[column]= data[column].str.replace(each, str2 , case = "True") 
            elif Ratio >= 90:
                data[column]= data[column].str.replace(each, str2 , case = "True") 
            elif Partial_Ratio2 > 95 and Ratio >= 85:
                data[column]= data[column].str.replace(each, str2 , case = "True") 
            elif Partial_Ratio2 > 85 and Ratio >= 95:
                data[column]= data[column].str.replace(each, str2 , case = "True") 
            elif average > 85 or (Ratio >= 85 and Token_Sort_Ratio >= 85):
                data[column]= data[column].str.replace(each, str2 , case = "True") 
            elif average > 85 or Ratio >= 85 or Token_Sort_Ratio >= 85 or Partial_Ratio >= 85 or Partial_Ratio2 >= 85:
                data[column]= data[column].str.replace(each, str2 , case = "True") 
            else:
                f.write(statement)       # catch those oustside the list     
    f.close()
    return data


#### Main ###
files = find_csv()[0] 
newname = files.replace(".csv", "")
data = pd.read_csv(files)
df = pd.DataFrame(data) 

columnNum = 2
df = clean(df.columns[entries], df)

# delete Temporary file if empty 
if os.stat("temporary.txt").st_size == 0:
    os.remove("temporary.txt")
else:
    print "Check Temporary File for excluded records"

#data = segment(df)
print str((time.time()-start_time)/60.) + " minutes"

data.to_csv(r'DataFrame.csv')


