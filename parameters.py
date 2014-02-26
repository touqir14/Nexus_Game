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
env_size = (resolution[0]-2,500-2)
info_size = (resolution[0]-2,100-1)
fps = 30

# random object with seed
rand = Random()
rand.seed(12)

# colours
env_bgc = THECOLORS['grey']
info_bgc = THECOLORS['grey10']
pro_colour = THECOLORS['red3']
basicFoodColour = THECOLORS['forestgreen']

# sizes
basicFoodDiameter = 15
protagonistDiameter = 20

# simulation
history = []
pro_starting_point = (env_size[0]-int(protagonistDiameter/2),env_size[1]-int(protagonistDiameter/2))
pro_max_speed = 2.3
pro_max_health = 100.0
health_step_decrease = 0.07
pro_max_endurance = 100.0
endurance_decrease = 3.0
endurance_increase = 1.0

# Antagonist
antagonist = sprite.GroupSingle()
ant_diameter = 30
ant_starting_point = (int(ant_diameter/2),int(ant_diameter/2))
ant_max_speed = 2.1
ant_max_health = 100.0
ant_colour = THECOLORS['blue3']
ant_odor_intensity = 450

# food
startingFood = 10
food_value = 15

allObjects = sprite.Group()
protagonist = sprite.GroupSingle()
g_food = sprite.Group()

# each loop of the simulation will be tracked by timeStep
timeStep = 0

# odors
show_odors = False
odorSources = sprite.Group()
pro_odor_intensity = 450
basicFood_odor_intensity = 150

# keyboard input stuff
up = False
down = False
left = False
right = False
