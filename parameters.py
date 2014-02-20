'''
Created on 2014-02-19

@author: Matthew Jorgensen

The global values of the simulation.
Stored here for easy access.
'''

# setup
resolution = (800,600)
env_size = (resolution[0],500)
info_size = (resolution[0],100)
fps = 30

# each loop in 'main.py' will be tracked by timeStep
timeStep = 0

# a dictionary of the different odors in the environment
# the keys are the class types
odors = []