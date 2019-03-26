# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 15:05:35 2019

Copies a folder in the same working directory as this script.

@author: John Hutcheson
"""

import shutil
import os
import time
from multiprocessing import Pool
from glob import glob


homeDir = r'C:\Users\pqb18127\OneDrive\PhD\Python\DEAP\multiprocessing\MP Workflow Abaqus'
copyDir = r'C:\Users\pqb18127\OneDrive\PhD\Python\DEAP\multiprocessing\MP Workflow Abaqus\original'
pasteDir = r'C:\Users\pqb18127\OneDrive\PhD\Python\DEAP\multiprocessing\MP Workflow Abaqus\analysis_'

noCores = 8
njobs = 8

def analysis(i):
    jobDir = shutil.copytree(copyDir,pasteDir + str(i)) # copy the original folder for use in this analysis.
    os.chdir(jobDir) # change working directory to new folder
    os.system('abaqus cae noGui=generateInp.py') # generate the input file in new folder
    os.system('abaqus job=Job-1 interactive ask_delete=OFF') # run the analysis
    os.system('abaqus viewer noGui=getDisps.py -- ' + str(i) ) # runs macro and passes i value to it # extract the data from the obd.
    os.chdir(homeDir) # change working directory to new folder
    
def main():
    #Ensure path is set to same directory as script
    abspath = os.path.abspath(__file__) 
    dname= os.path.dirname(abspath)
    os.chdir(dname)

    #Make sure no stray lock files mess up our runs
    for f in glob ('./*.lck'):
        os.unlink(f)
        
    #Generate List of tuples containing inputs to the analysis function.    
    args = [i for i in range (1,njobs+1) ] 
    
    #Parallise  
    Pool(noCores).map(analysis, args, chunksize = 1)

    
if __name__ == "__main__":
    t1 = time.time()
    main()
    t2 = time.time()
    print('Time to solve: ' + str(t2-t1) + ' s.') 
