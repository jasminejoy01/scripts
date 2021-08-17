'''
Batch export of all arcGIS maps
Additional File: Textfile with filepath to all mxd
'''

import os, glob, fnmatch, re, arcpy

# Functions
def pdf(input_path):
    mxd = arcpy.mapping.MapDocument(input_path)
    for lyr in arcpy.mapping.ListLayers(mxd):
        if lyr.visible == True:
            #print lyr.name                                 
            outputPDF = input_path.split('.')[0] + ".pdf"
            return arcpy.mapping.ExportToPDF(mxd,outputPDF)
        else:
            pass

def file_search(folder):
    for dirpath, dirs, files in os.walk(folder):
        for filename in fnmatch.filter(files, filetype):     
            with open(os.path.join(dirpath, filename)) as f:
                os.path.dirname(os.path.realpath(filetype))
                inFile.append(os.path.realpath(filetype))

####################
inFile = []              
directory = 'C:'
filetype = 'BatchPDF.txt'
file_search(directory)

for i in inFile:
    inHandler = open(i, 'r')
    for line in inHandler:
        line = line.replace('\n', '')
        pdf(line)
        print 'Completed:', i
     
inHandler.close()
