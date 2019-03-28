# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:17:22 2019

Shared list test.

This is an example of how to set up multiprocessing to work with a shared list.

@author: pqb18127
"""

#from multiprocessing import Pool, Manager
#
#x = list(range(10,21))
#
#man = Manager()
#sharedList = man.list(range(10))
#
#def process(x,sharedList):
#    item = sharedList
#    del item[0]
#    sharedList = item
#    print(item,x)
#    
#
#args = (x,sharedList)    
#
#p = Pool().starmap(process,args)    

# This is an example of multiprocessing using the manager function. 

from multiprocessing import Pool, Manager

num = 1000

def f(x,sharedList): 
    item = sharedList
    del item[0]
    sharedList = item
    print(item,x)

if __name__ == '__main__':
    manager = Manager()
    x = list(range(num))
    sharedList = manager.list(range(num))
    print(sharedList)
    sharedListList = [sharedList for i in range(num)]
    args = [(x[i],sharedListList[i]) for i in range(num)]
    p = Pool(4).starmap(f,args)
    print(sharedList)
