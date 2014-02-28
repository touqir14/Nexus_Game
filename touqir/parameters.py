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

class Parameters:
    
    def __init__(self):

        #setup
        self.resolution = (800,600)
        self.env_size = (resolution[0]-2,500-2)
        self.info_size = (resolution[0]-2,100-1)
        self.fps = 30
        
        # random object with seed
        self.rand = Random()
        self.rand.seed(12)

        
        # colours
        self.env_bgc = THECOLORS['grey']
        self.info_bgc = THECOLORS['grey10']
        self.pro_colour = THECOLORS['red3']
        self.basicFoodColour = THECOLORS['forestgreen']

        # sizes
        self.basicFoodDiameter = 15
        self.protagonistDiameter = 20

        # simulation
        self.universal_history = []
        self.pro_starting_point = (env_size[0]-int(self.protagonistDiameter/2),env_size[1]-int(self.protagonistDiameter/2))
        self.pro_max_speed = 2.3
        self.pro_max_health = 100.0
        self.health_step_decrease = 0.07
        self.pro_max_endurance = 100.0
        self.endurance_decrease = 3.0
        self.endurance_increase = 1.0

        # Antagonist
        # I changed antagonist from sprite.GroupSingle to Group touqir
        self.antagonist = sprite.Group()
        self.ant_diameter = 30
        self.ant_starting_point = (int(self.ant_diameter/2),int(self.ant_diameter/2))
        self.ant_max_speed = 2.1
        self.ant_max_health = 100.0
        self.ant_colour = THECOLORS['blue3']
        self.ant_odor_intensity = 450

        # food
        self.startingFood = 10
        self.food_value = 15

        #List and groups of the gameworld objects
        # I added the last four lists and i changed protagonist from sprite.GroupSingle to Group  touqir
        self.allObjects = sprite.Group()
        self.protagonist = sprite.Group()
        self.g_food = sprite.Group()
        self.PRO=[]
        self.ANT=[]
        self.FOOD=[]
        self.ALLOBJ=[]

        # each loop of the simulation will be tracked by timeStep
        self.timeStep = 0

        # odors
        self.show_odors = False
        self.odorSources = sprite.Group()
        self.pro_odor_intensity = 450
        self.basicFood_odor_intensity = 150

# keyboard input stuff
up = False
down = False
left = False
right = False
