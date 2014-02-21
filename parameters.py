'''
Created on 2014-02-19

@author: Matthew Jorgensen

The global values of the simulation.
Stored here for easy access.
'''
from pygame import sprite
from pygame.colordict import THECOLORS
from random import Random

# setup
resolution = (800,600)
env_size = (resolution[0],500)
info_size = (resolution[0],100)
fps = 30

# random object with seed
rand = Random()
rand.seed(12)

# colours
pro_colour = THECOLORS['red3']
basicFoodColour = THECOLORS['forestgreen']

# sizes
basicFoodDiameter = 20
protagonistDiameter = 20

# simulation
history = []
pro_starting_point = (env_size[0]-int(protagonistDiameter/2),env_size[1]-int(protagonistDiameter/2))
pro_max_speed = 22.0
pro_max_health = 100.0
health_step_decrease = 0.1
pro_max_endurance = 100.0
endurance_decrease = 3.0
endurance_increase = 1.0

startingFood = 10
allObjects = sprite.Group()
protagonist = sprite.GroupSingle()
#food = sprite.Group()

# each loop of the simulation will be tracked by timeStep
timeStep = 0

# a dictionary of the different odors in the environment
# the keys are the class types
odors = sprite.Group()
odorSources = sprite.Group()

# keyboard input stuff
up = False
down = False
left = False
right = False
