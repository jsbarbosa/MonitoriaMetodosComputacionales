# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 20:47:39 2016

@author: juan
"""

import numpy as np
import glob
import time
import zipfile
import imp
import os
import re
#import sys
import csv
import fileinput

# gets zip files in current working directory
def getFiles(extention):
    return glob.glob(extention)
    
# unzips the files on paths
def unzip(paths):
    folder_names = []
    for path in paths:
        with zipfile.ZipFile(path, "r") as zip_ref:
            print("Extracting " + path + "...")
            temp = path.split(".zip", 1)[0]            
            zip_ref.extractall(temp)
            folder_names.append(temp)
    print("===============================================")
    return folder_names

# gets students names            
def nameSplitter(path):
    temp = path.split("_", 1)[0] 
    name = re.findall('[A-Z][^A-Z]*', temp)
    
    return name
        
# imports .py file
def moduleImport(code, name):
    try:
        return imp.load_source(name, code)
    except:
        return None
    
def analize(extention):
    paths = getFiles(extention)
    folder_names = unzip(paths)
    student_names = nameSplitter(folder_names)
    return student_names
    
def countLines(file):
    count = 0
    with open(file) as f:
        for line in f:
            count += 1
    return count
        
def file_checker(directory, files_list):
    found = []
    for file in files_list:
        if os.path.exists(directory + "/" + file):
            found.append(file)
    return found
    
def saveResults(name, row):
    writer = csv.writer(open(name, 'a'))
    writer.writerow(row)

def replace(file, search_for, replace_for):
    for line in fileinput.input(file, inplace = 1):
        print(line.replace(search_for, replace_for).rstrip())