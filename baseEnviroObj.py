'''
Created on 2014-04-04

@author: User
'''
import pygame
import parameters as p
import math

class BaseEnviroObj(pygame.sprite.Sprite):
    '''
    a base environment object has coordinates and inits properly to the environment grid
    '''


    def __init__(self, image, envirogrid, startcoord):
        '''
        Constructor
        '''
        super().__init__()
        self.rect = image.get_rect()
        # give position
        #startcoord = envirogrid.convPosToCoord(startpos)
        # be sure that coord is on map
        self._coord = envirogrid.closestGridCoord(startcoord)
        #self.coord = startcoord
        self.rect.center = envirogrid.getcenter(self.coord)
        
        # give health
        self.max_health = 1.0
        self.health = self.max_health
        
    @property
    def coord(self):
        return math.floor(self._coord[0]),math.floor(self._coord[1])
    
    @coord.setter
    def coord(self, twotuple):
        self._coord = twotuple
        
    def affectHealth(self, env_obj):
        """
        This method can be overridden by inheriting classes to allow 
        them to affectHealth other objects in the environment.
        
        primarily used against the hero as most objects should only affect the hero.
        """
        env_obj.health += self.effectvalue
        self.kill()
        # regulate obj health
        if env_obj.health <= 0:
            env_obj.kill()
        elif env_obj.health > env_obj.max_health:
            env_obj.health = env_obj.max_health
    