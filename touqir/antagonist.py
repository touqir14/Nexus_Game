'''
Created on 2014-02-19

@author: User
'''
from pygame.sprite import Sprite, GroupSingle
import pygame
from movable import Movable
from odor import OdorSource
import math

class Antagonist(Sprite, Movable):
    '''
    classdocs
    '''
    # give the antagonist an image
    #image = pygame.Surface((parameters.ant_diameter,parameters.ant_diameter))
    #image.fill(parameters.ant_colour)

    def __init__(self, parameters):
        '''
        Constructor
        '''
        self.parameters=parameters
        self.image = pygame.Surface((parameters.ant_diameter,parameters.ant_diameter))
        self.image.fill(parameters.ant_colour)
        ## required by Sprite()
        # initialize Sprite() so this instance can be updated and drawn
        Sprite.__init__(self)
        # give antagonist a rect
        self.rect = self.image.get_rect()
        
        ## required by Movable()
        Movable.__init__(self, parameters.ant_max_speed)
        
        # add instance to simulation list groups and control group
        parameters.allObjects.add(self)
        parameters.antagonist.add(self)
        
        # give position
        self.rect.center = parameters.ant_starting_point
        self.pos = (float(self.rect.center[0]),float(self.rect.center[1]))
        
        # give this instance an odor so it has a smell in the environment
        OdorSource( parameters,__name__,GroupSingle(self),parameters.ant_odor_intensity,parameters.ant_colour)
        
        # give health and endurance
        self.health = parameters.ant_max_health
        #self.endurance = parameters.ant_max_endurance
        
        # a group to hold the closest food item
        #self.closest_food = GroupSingle()
        
    def update(self):
        """
        put AI stuff here
        """
        print("im here")
        # eat protagonist when close enough
        pro_list = self.parameters.protagonist.sprites()
        if pro_list:
            pro=pro_list[0]
            x = pro.rect.center[0] - self.rect.center[0]
            y = pro.rect.center[1] - self.rect.center[1]
            pro_radius = int(pro.rect.width/2)
            self_radius = int(self.rect.width/2)
            if (math.hypot(x, y) - pro_radius - self_radius) <= 0:
                pro.kill()
                self.health += self.parameters.food_value
                if self.health > self.parameters.ant_max_health:
                    self.health = self.parameters.ant_max_health

        
