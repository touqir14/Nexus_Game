'''
Created on 2014-02-19

@author: User
'''
from pygame.sprite import Sprite, GroupSingle
import pygame
from movable import Movable
from odor import OdorSource
import math

class Protagonist(Sprite, Movable): 
    '''
    classdocs
    '''
    # give the protagonist an image
    #image = pygame.Surface((parameters.protagonistDiameter,parameters.protagonistDiameter))
    #image.fill(parameters.pro_colour)

    def __init__(self, parameters):
        '''
        Constructor
        '''
        self.parameters=parameters
        self.image = pygame.Surface((parameters.protagonistDiameter,parameters.protagonistDiameter))
        self.image.fill(parameters.pro_colour)

        ## required by Sprite()
        # initialize Sprite() so this instance can be updated and drawn
        Sprite.__init__(self)
        # give protagonist a rect
        self.rect = self.image.get_rect()
        
        ## required by Movable()
        Movable.__init__(self, parameters.pro_max_speed)
        
        # add instance to simulation list groups and control group
        parameters.allObjects.add(self)
        parameters.protagonist.add(self)
        # give position
        self.rect.center = parameters.pro_starting_point
        self.pos = (float(self.rect.center[0]),float(self.rect.center[1]))
        # give this instance an odor so it has a smell in the environment
        OdorSource(parameters,__name__,GroupSingle(self),parameters.pro_odor_intensity,parameters.pro_colour)
        # give health and endurance
        self.health = parameters.pro_max_health
        #self.endurance = parameters.pro_max_endurance
        
        # a group to hold the closest food item
        #self.closest_food = GroupSingle()
        
    def update(self):
        """
        put AI stuff here
        """
        # eat food when close enough
        for i in self.parameters.g_food.sprites():
            x = i.rect.center[0] - self.rect.center[0]
            y = i.rect.center[1] - self.rect.center[1]
            food_radius = int(i.rect.width/2)
            self_radius = int(self.rect.width/2)
            if (math.hypot(x, y) - food_radius - self_radius) <= 0:
                i.kill()
                self.health += self.parameters.food_value
                if self.health > self.parameters.pro_max_health:
                    self.health = self.parameters.pro_max_health
        
        """
        # endurance
        self.endurance += parameters.endurance_increase
        if self.endurance > parameters.pro_max_endurance:
            self.endurance = parameters.pro_max_endurance
            
        endurancePercent = self.endurance / parameters.pro_max_endurance
        self.speed = parameters.pro_max_speed * endurancePercent
        """

    def reward(self):
        """will produce rewards based on health changes"""

        
    def intrinsic_reward(self):
        """ it will give the protagonist reward for exploration(curiosity in other words)"""

    
    def move(self, direction=None):
        Movable.move(self, direction=direction)
        #self.endurance -= parameters.endurance_decrease
        #if self.endurance <= 0:
        #    self.endurance = 0.0
        
