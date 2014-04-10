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
import knn
import dijkstra
from target import Target
import sys

class Protagonist(Movable):
    '''
    classdocs
    '''
    # give the protagonist an image
    image = pygame.Surface((p.protagonistDiameter,p.protagonistDiameter))
    image.fill(p.pro_colour)

    # how much the hero will affect other objects
    effectvalue = 100


    def __init__(self, envirogrid, movestyle):
        '''
        Constructor
        '''
        super().__init__(p.pro_max_speed, envirogrid, Protagonist.image, (99,99))
        
        # add instance to simulation list groups and control group
        p.allObjects.add(self)
        p.protagonist.add(self)
        
        self._movestyle = movestyle
        
        # give this instance an odor so it has a smell in the environment
        OdorSource(__name__,GroupSingle(self),p.pro_odor_intensity,p.pro_colour)

        # adjust health from super class
        self.max_health = 100.0
        self.health = self.max_health
        
        # adjust rate of movement from Moveable class
        self.rateOfMovement = 3
        
        # knn memoization
        self.knnweights = None
        self.pathway = []
        self.k_of_KNN = 8
        self.approach_of_KNN = 0

    def update(self, km_state, grid):
        """
        
        """
        self.decreaseMoveCountdown(km_state)
        # put AI stuff here
        # mode 1: move first if mouse input
        if self._movestyle == 1:
            self.move(km_state)
        
        # mode 2: move by dykstra's with KNN as cost function
        elif self._movestyle == 2:
            # chase Target if exists
            # (target is placed on the grid using Simulation.placeObjectAt() within Simulation.run()
            if len(self.pathway) > 0:
                if self.movementCountdown <= 0:
                    target_coord = self.pathway.pop(0)
                    self.moveToward(target_coord)
                
            else:
                target = Target.g_targ.sprite
                if target:
                    targcoord = target.coord
                    
                    # first check if target has been reached
                    if self.coord == targcoord:
                        target.kill()
                    else:
                        # knn
                        self.knnweights = knn.k_nearest_neighbour_searcher(grid.value_dict, self.k_of_KNN, (grid.width-1, grid.height-1),.9,self.approach_of_KNN)
                        self.pathway = dijkstra.search(self.coord, targcoord, self.knnweights)
                
        # get affected by objects if they're on the same grid tile
        for o in p.allObjects.sprites():
            if o.coord == self.coord and o != self:
                o.affectHealth(self, grid.value_dict)
        
    def decreaseMoveCountdown(self, km_state):
        if kmui.Released in (km_state.left,km_state.right,km_state.up,km_state.down):
            self.movementCountdown = 0
        super().decreaseMoveCountdown()
    
    def move(self, km_state):
        """
        override Moveable.move() to let the movement be decided by the keyboard input
        """
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
        
    def affectHealth(self, env_obj, touqirs_value_dict):
        """
        overridden to not die while causing an effect to other screen objects
        """
        # hurt the hero a little bit
        env_obj.health += self.effectvalue
        # eat the hero a little bit
        #self.health += env_obj.effectvalue
        # regulate obj health. dead?
        env_obj.regulatehealth()

