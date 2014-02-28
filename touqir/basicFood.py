'''
Created on 2014-02-19

@author: User
'''
from pygame import sprite
import pygame
from odor import OdorSource
from pygame.sprite import GroupSingle

class BasicFood(sprite.Sprite):
    '''
    classdocs
    '''
    # add this class to the odors list so it has a smell in the environment
    #parameters.odors.append(__name__)
    # one image for all the food instances
    #image = pygame.Surface((parameters.basicFoodDiameter,parameters.basicFoodDiameter))

    def __init__(self, parameters, pos):
        '''
        Constructor
        '''
        self.parameters=parameters
        self.image = pygame.Surface((parameters.basicFoodDiameter,parameters.basicFoodDiameter))
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        pygame.draw.circle(self.image,parameters.basicFoodColour,self.image.get_rect().center,int(self.image.get_rect().width/2))

        # initialize Sprite() so this instance can be updated and drawn
        sprite.Sprite.__init__(self)
        
        # add instance to simulation list groups
        parameters.allObjects.add(self)
        parameters.g_food.add(self)
        
        # give this instance a rect
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = (float(self.rect.center[0]),float(self.rect.center[1]))

        # give this instance an odor so it has a smell in the environment
        OdorSource(parameters,__name__,GroupSingle(self),parameters.basicFood_odor_intensity,parameters.basicFoodColour)
        
