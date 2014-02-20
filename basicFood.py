'''
Created on 2014-02-19

@author: User
'''
from pygame import sprite
import parameters as p
import pygame

class BasicFood(sprite.Sprite):
    '''
    classdocs
    '''
    # add this class to the odors list so it has a smell in the environment
    p.odors.append(__name__)
    # one image for all the food instances
    image = pygame.Surface((p.basicFoodDiameter,p.basicFoodDiameter))

    def __init__(self, pos):
        '''
        Constructor
        '''
        # initialize Sprite() so this instance can be updated and drawn
        sprite.Sprite.__init__(self)
        # add instance to simulation list groups
        p.allObjects.add(self)
        # give this instance a rect
        self.rect = BasicFood.image.get_rect()
        self.rect.center = pos
        self.pos = (float(self.rect.center[0]),float(self.rect.center[1]))