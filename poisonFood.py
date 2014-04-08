'''
Created on 2014-02-19

@author: User
'''
from pygame import sprite
import parameters as p
import pygame
from odor import OdorSource
from pygame.sprite import GroupSingle
from baseEnviroObj import BaseEnviroObj

class PoisonFood(BaseEnviroObj):
    '''
    classdocs
    '''
    # add this class to the odors list so it has a smell in the environment
    #p.odors.append(__name__)
    # one image for all the food instances
    image = pygame.Surface((15,15))
    colour = (200,50,250)
    
    # how much the hero (or any environment object) will be affected by this type of game object
    effectvalue = -25

    # set food value to positive
    value = 0
        
    def __init__(self, envirogrid, startcoord=(0,0)):
        '''
        Constructor
        '''
        super().__init__(PoisonFood.image, envirogrid, startcoord)
        # initialize Sprite() so this instance can be updated and drawn
        #sprite.Sprite.__init__(self)
        
        # add instance to simulation list groups
        p.allObjects.add(self)
        #p.g_food.add(self)
        
        # give this instance a rect
        #self.rect = PoisonFood.image.get_rect()
        #self.rect.center = coord
        #self.coord = (float(self.rect.center[0]),float(self.rect.center[1]))

        # give this instance an odor so it has a smell in the environment
        OdorSource(__name__,GroupSingle(self),p.basicFood_odor_intensity,PoisonFood.colour)
        
    def affect(self, env_obj):
        env_obj.health += self.effectvalue
        self.kill()
        