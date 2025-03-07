'''
Created on 2014-02-19

@author: Matthew Jorgensen

The global values of the simulation.
Stored here for easy access.

decided to stop using this global module but still working on the conversion.
'''
from pygame import sprite
from pygame.colordict import THECOLORS
from random import Random

# setup
border = 2
resolution = (30*27+border*2,30*17+border*2+100)
env_size = (resolution[0]-border*2,30*17)
info_size = (resolution[0]-border*2,100-border)
fps = 30
startup = True

# random object with seed
rand = Random()
rand.seed(12)

# screen colours
env_bgc = THECOLORS['grey']
info_bgc = THECOLORS['grey10']

# simulation
allObjects = sprite.Group()
history = []
startingFood = 100
health_step_decrease = 0.07
endurance_decrease = 3.0
endurance_increase = 1.0
weightvisual = True

# Protagonist
protagonist = sprite.GroupSingle()
protagonistDiameter = 20
pro_starting_point = (env_size[0]-int(protagonistDiameter/2),env_size[1]-int(protagonistDiameter/2))
pro_max_speed = 1
pro_max_endurance = 100.0
pro_colour = THECOLORS['red3']
pro_odor_intensity = 450

# Antagonist
antagonist = sprite.GroupSingle()
ant_diameter = 30
ant_starting_point = (int(ant_diameter/2),int(ant_diameter/2))
ant_max_speed = 1
ant_max_health = 100.0
ant_colour = THECOLORS['blue3']
ant_odor_intensity = 450

# food
g_food = sprite.Group()
g_poison = sprite.Group()
basicFoodDiameter = 15
basicFood_odor_intensity = 150

# each loop of the simulation will be tracked by timeStep
timeStep = 0

# odors
show_odors = False
odorSources = sprite.Group()
