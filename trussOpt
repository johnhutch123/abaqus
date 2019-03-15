# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 11:28:41 2019

Optimisation of truss cross section using a GA.

to do:
    
    - Still need to consider both of the steps...

@author: pqb18127
"""
import os
import random
from deap import base
from deap import creator
from deap import tools
import numpy as np
from deap import algorithms
import time


# --- User inputs --- #

l1 = 0.254 # length of central member
l2 = 0.359 # length of side members

compStressLim = -1.89e8
tensStressLim = 1.379e8
dispLimUp = 0.00508
dispLimLow = 0

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


toolbox = base.Toolbox()
# Attribute generator 
toolbox.register("attr_bool", random.randint, 0, 1) # going to want to change this to a random number between small value and large value. (initial guess for matrix)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 2) # 2 is number of variables in the optimisation
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def fitFunc(individual,l1=l1,l2=l2): # fitness function is here, need to add constraint penalisation... 
    vol = individual[0]*l1 + individual[1]*l2*2 # calculate volume
    return vol,


def updateINP(desVar,fileName): # takes three cross sectional areas and updates the input file.
    
    a1 = desVar[0]
    a2 = desVar[1]
    
    # with is like your try .. finally block in this case
    with open(fileName, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        
        data[39] = str(a1) + ',\n'
        data[42] = str(a2) + ',\n'

     
    with open(fileName,'w') as file:
        file.writelines(data)


def runJob(fileName): # run abaqus using specified input file
    os.system('abaqus job=' + str(fileName) + ' interactive ask_delete=OFF')
    

def runMacro(macroFileName):
    os.system('abaqus cae noGui="' + str(macroFileName)+'"') # add command in here for running the macro.


def readResults(fileName):
    csv = np.genfromtxt(fileName,dtype=float,delimiter=',')
    csv[np.isnan(csv)]=0 # set nan values to 0. this shouldn' cause problems.
    stress = csv[np.argmax(abs(csv[:,12])),12]
    disp = csv[np.argmax(abs(csv[:,11])),11]
    return stress, disp


def analyseStructure(jobFile, macroFile,desVar): # runs abaqus analysis and returns the maximum stress and displacement
    updateINP(desVar,jobFile)
    runJob(jobFile)
    runMacro(macroFile) # need to prevent this from
    
    #while os.path.isfile(macroFile) == True:
    #time.sleep(15)
        
    stress, disp = readResults(simResults) # need to prevent this from running before the previous command has finished.
    return stress, disp


def feasible(individual):
    
    #global jobFile, macroFile
    
    """Feasibility function for the individual. Returns True if feasible False
    otherwise."""  
    stress, disp = analyseStructure(jobFile, macroFile,individual) # need to make this function

    if compStressLim < stress < tensStressLim and dispLimLow < disp < dispLimUp :
        return True
    return False


toolbox.register("evaluate", fitFunc)
toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, 10.0)) # applies penalty of 10 to result if it is unfeasible.
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


jobFile = 'Job-1.inp'
macroFile =  r'C:\Users\pqb18127\OneDrive\PhD\Training\NAFEMS Homework 1\dataOut.py'
simResults = 'data.csv'

def main():
    
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, 
                                   stats=stats, halloffame=hof, verbose=True)

if __name__ == "__main__":
    main()
