import parameters as p
import pygame
from odor import OdorSource
from pygame.sprite import GroupSingle
from baseEnviroObj import BaseEnviroObj
from pygame.colordict import THECOLORS

class BasicFood(BaseEnviroObj):
    """
    The green food pellets on the grid. the hero can travel to the same 
    tile as one of these items to gain some health points
    """

    # one image for all the food instances
    image = pygame.Surface((p.basicFoodDiameter,p.basicFoodDiameter))
    colour = THECOLORS['forestgreen']

    # how much the hero (or any environment object?) will be affected by this type of game object
    effectvalue = 15

    # set food value to positive for KNN functions
    value = 1
        
    def __init__(self, envirogrid, startcoord=(0,0)):
        '''
        Constructor
        '''
        super().__init__(BasicFood.image, envirogrid, startcoord)
        
        # add instance to simulation list groups
        p.allObjects.add(self)
        p.g_food.add(self)
        
        # give this instance an odor so it has a smell in the environment
        OdorSource(__name__,GroupSingle(self),p.basicFood_odor_intensity,BasicFood.colour)
        
