import parameters as p
import pygame
from odor import OdorSource
from pygame.sprite import GroupSingle
from baseEnviroObj import BaseEnviroObj

class PoisonFood(BaseEnviroObj):
    '''
    a pink pellet on the screen that will hurt the protagonist if touched.
    '''
    # one image for all the poison instances
    image = pygame.Surface((15,15))
    colour = (200,50,250)
    
    # how much the hero (or any environment object?) will be affected by this type of game object
    effectvalue = -25

    # set food value to positive for KNN functions
    value = 0
        
    def __init__(self, envirogrid, startcoord=(0,0)):
        '''
        Constructor
        '''
        super().__init__(PoisonFood.image, envirogrid, startcoord)
        
        # add instance to simulation list groups
        p.allObjects.add(self)
        p.g_poison.add(self)
        
        # give this instance an odor so it has a smell in the environment
        OdorSource(__name__,GroupSingle(self),p.basicFood_odor_intensity,PoisonFood.colour)
        
        