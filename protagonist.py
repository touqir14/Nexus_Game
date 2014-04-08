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
import kmui

class Protagonist(Movable):
    '''
    classdocs
    '''
    # give the protagonist an image
    image = pygame.Surface((p.protagonistDiameter,p.protagonistDiameter))
    image.fill(p.pro_colour)

    def __init__(self, envirogrid):
        '''
        Constructor
        '''
        super().__init__(p.pro_max_speed, envirogrid, Protagonist.image, (99,99))
        ## required by Sprite()
        # initialize Sprite() so this instance can be updated and drawn
        #Sprite.__init__(self)
        # give protagonist a rect
        #self.rect = Protagonist.image.get_rect()
        
        ## required by Movable()
        #Movable.__init__(self, p.pro_max_speed)
        
        # add instance to simulation list groups and control group
        p.allObjects.add(self)
        p.protagonist.add(self)
        
        
        #self.coord = (float(self.rect.center[0]),float(self.rect.center[1]))

        
        # give this instance an odor so it has a smell in the environment
        OdorSource(__name__,GroupSingle(self),p.pro_odor_intensity,p.pro_colour)
        # give health
        self.max_health = 100.0
        self.health = self.max_health
        #self.endurance = p.pro_max_endurance
        
        # a group to hold the closest food item
        #self.closest_food = GroupSingle()
        
    def update(self, km_state):
        """
        
        """
        # put AI stuff here
        # mode 1: move first if mouse input
        self.move(km_state)
        
        # mode 2: move by dykstra's with KNN as cost function
        #
        
        #=======================================================================
        # # eat food when close enough
        # for i in p.g_food.sprites():
        #     x = i.rect.center[0] - self.rect.center[0]
        #     y = i.rect.center[1] - self.rect.center[1]
        #     food_radius = int(i.rect.width/2)
        #     self_radius = int(self.rect.width/2)
        #     if (math.hypot(x, y) - food_radius - self_radius) <= 0:
        #         i.kill()
        #         self.health += p.food_value
        #         if self.health > p.pro_max_health:
        #             self.health = p.pro_max_health
        #=======================================================================
                    
        # get affected by objects if they're on the same grid tile
        for o in p.allObjects.sprites():
            if o.coord == self.coord and o != self:
                o.affectHealth(self)
        
        
        """
        # endurance
        self.endurance += p.endurance_increase
        if self.endurance > p.pro_max_endurance:
            self.endurance = p.pro_max_endurance
            
        endurancePercent = self.endurance / p.pro_max_endurance
        self.speed = p.pro_max_speed * endurancePercent
        """
    
    def move(self, km_state):
        if km_state.left == kmui.Down:
            super().move('left')
        if km_state.right == kmui.Down:
            super().move('right')
        if km_state.up == kmui.Down:
            super().move('up')
        if km_state.down == kmui.Down:
            super().move('down')
#        Movable.move(self, direction=direction)
        #self.endurance -= p.endurance_decrease
        #if self.endurance <= 0:
        #    self.endurance = 0.0
        
