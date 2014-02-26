'''
Created on 2014-02-19

@author: User
'''
from pygame.sprite import Sprite, GroupSingle
import parameters as p
import pygame
from movable import Movable
from odor import OdorSource
import math

class Antagonist(Sprite, Movable):
    '''
    classdocs
    '''
    # give the antagonist an image
    image = pygame.Surface((p.ant_diameter,p.ant_diameter))
    image.fill(p.ant_colour)

    def __init__(self):
        '''
        Constructor
        '''
        ## required by Sprite()
        # initialize Sprite() so this instance can be updated and drawn
        Sprite.__init__(self)
        # give antagonist a rect
        self.rect = Antagonist.image.get_rect()
        
        ## required by Movable()
        Movable.__init__(self, p.ant_max_speed)
        
        # add instance to simulation list groups and control group
        p.allObjects.add(self)
        p.antagonist.add(self)
        
        # give position
        self.rect.center = p.ant_starting_point
        self.pos = (float(self.rect.center[0]),float(self.rect.center[1]))
        
        # give this instance an odor so it has a smell in the environment
        OdorSource(__name__,GroupSingle(self),p.ant_odor_intensity,p.ant_colour)
        
        # give health and endurance
        self.health = p.ant_max_health
        #self.endurance = p.ant_max_endurance
        
        # a group to hold the closest food item
        #self.closest_food = GroupSingle()
        
    def update(self):
        """
        put AI stuff here
        """
        print("im here")
        # eat protagonist when close enough
        pro = p.protagonist.sprite
        x = pro.rect.center[0] - self.rect.center[0]
        y = pro.rect.center[1] - self.rect.center[1]
        pro_radius = int(pro.rect.width/2)
        self_radius = int(self.rect.width/2)
        if (math.hypot(x, y) - pro_radius - self_radius) <= 0:
            pro.kill()
            self.health += p.food_value
            if self.health > p.ant_max_health:
                self.health = p.ant_max_health

        
