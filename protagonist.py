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

class Protagonist(Sprite, Movable):
    '''
    classdocs
    '''
    # give the protagonist an image
    image = pygame.Surface((p.protagonistDiameter,p.protagonistDiameter))
    image.fill(p.pro_colour)

    def __init__(self, grid):
        '''
        Constructor
        '''
        ## required by Sprite()
        # initialize Sprite() so this instance can be updated and drawn
        Sprite.__init__(self)
        # give protagonist a rect
        self.rect = Protagonist.image.get_rect()
        
        ## required by Movable()
        Movable.__init__(self, p.pro_max_speed)
        
        # add instance to simulation list groups and control group
        p.allObjects.add(self)
        p.protagonist.add(self)
        # give position
        self.rect.center = p.pro_starting_point
        self.pos = (float(self.rect.center[0]),float(self.rect.center[1]))
        
        # make sure that position is on grid world
        self.pos = grid.closestGridCoord(self.pos)
        
        # centre rect over grid coord
        self.rect.center = grid.blockdict[self.pos].sprite.rect.center
        
        # give this instance an odor so it has a smell in the environment
        OdorSource(__name__,GroupSingle(self),p.pro_odor_intensity,p.pro_colour)
        # give health and endurance
        self.health = p.pro_max_health
        #self.endurance = p.pro_max_endurance
        
        # a group to hold the closest food item
        #self.closest_food = GroupSingle()
        
    def update(self, grid):
        """
        """
        # eat food when close enough
        for i in p.g_food.sprites():
            x = i.rect.center[0] - self.rect.center[0]
            y = i.rect.center[1] - self.rect.center[1]
            food_radius = int(i.rect.width/2)
            self_radius = int(self.rect.width/2)
            if (math.hypot(x, y) - food_radius - self_radius) <= 0:
                i.kill()
                self.health += p.food_value
                if self.health > p.pro_max_health:
                    self.health = p.pro_max_health
        
        # put AI stuff here
        
        
        """
        # endurance
        self.endurance += p.endurance_increase
        if self.endurance > p.pro_max_endurance:
            self.endurance = p.pro_max_endurance
            
        endurancePercent = self.endurance / p.pro_max_endurance
        self.speed = p.pro_max_speed * endurancePercent
        """
    
        
