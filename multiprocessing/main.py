# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 10:09:41 2019

Modified code from reddit:
https://www.reddit.com/r/learnpython/comments/4j4x20/python_multiprocessing_critique/

Can increase the pool size to speed up the analysis however this uses more abaqus licences, shouldnt use more than number of cpus I am using. 

@author: John Hutcheson
"""

from multiprocessing import Pool
import os
from glob import glob
import time

njobs = 12

#Abaqus Caller
def analysis (filename,i):
    os.system('abaqus job=' + filename + ' interactive ask_delete=OFF')
    os.system('abaqus viewer noGui=getDisps.py -- ' + str(i) ) # runs macro and passes i value to it 


def main():
    #Ensure path is set to same directory as script
    abspath = os.path.abspath(__file__) 
    dname= os.path.dirname(abspath)
    os.chdir(dname)

    #Make sure no stray lock files mess up our runs
    for f in glob ('./*.lck'):
        os.unlink(f)

    #Set filename structure here    
    basename = "mp"

    #Generate List of tuples containing inputs to the analysis function.    
    args = [(basename + str(i),i) for i in range (1,njobs+1) ] 
    
    #Parallise  
    Pool().starmap(analysis, args, chunksize = 1)

    
if __name__ == "__main__":
    t1 = time.time()
    main()
    t2 = time.time()
    print('Time to solve: ' + str(t2-t1) + ' s.')
