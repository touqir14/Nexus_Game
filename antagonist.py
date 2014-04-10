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
import dijkstra

class Antagonist(Movable):
    '''
    classdocs
    '''
    # give the antagonist an image
    image = pygame.Surface((p.ant_diameter,p.ant_diameter))
    image.fill(p.ant_colour)
    
    # how much the hero (or any environment object?) will be affected by this type of game object
    effectvalue = -20

    # a value is given to all environment object classes that tell them if the hero likes them or not
    # 0 means not...
    value = 0

    def __init__(self, envirogrid, startcoord, mode):
        '''
        Constructor
        '''
        self.mode = mode
        super().__init__(p.pro_max_speed, envirogrid, Antagonist.image, startcoord)

        # add instance to simulation list groups and control group
        p.allObjects.add(self)
        p.antagonist.add(self)
        
        # give this instance an odor so it has a smell in the environment
        OdorSource(__name__,GroupSingle(self),p.ant_odor_intensity,p.ant_colour)
        
        # adjust health from super class
        self.max_health = 100.0
        self.health = self.max_health
                
        # track self on grid
        envirogrid.trackObj(self, self.coord)
        
    def update(self, mouse, grid):
        """
        put AI stuff here
        """
        self.decreaseMoveCountdown()
        pro = p.protagonist.sprite
        if pro:
            targcoord = dijkstra.chaser(self.coord, pro.coord, grid.value_dict)
#             print(targcoord)
            self.moveToward(targcoord)
            
        # get affected by objects if they're on the same grid tile
        for o in p.allObjects.sprites():
            if o.coord == self.coord and o != self:
                o.affectHealth(self, grid.value_dict)
        
    def affectHealth(self, env_obj, touqirs_value_dict):
        """
        overridden to not die but instead gain health from the hero
        """
        # hurt the hero a little bit
        env_obj.health += self.effectvalue
        # eat the hero a little bit
        #self.health += env_obj.effectvalue
        if self.value in touqirs_value_dict[self.coord]:
            touqirs_value_dict[self.coord].remove(self.value)
        # regulate obj health. dead?
        env_obj.regulatehealth()
