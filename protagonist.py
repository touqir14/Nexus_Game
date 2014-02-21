'''
Created on 2014-02-19

@author: User
'''
from pygame.sprite import Sprite, GroupSingle
import parameters as p
import pygame
from movable import Movable
from odor import OdorSource

class Protagonist(Sprite, Movable):
    '''
    classdocs
    '''
    # give the protagonist an image
    image = pygame.Surface((p.protagonistDiameter,p.protagonistDiameter))
    image.fill(p.pro_colour)

    def __init__(self):
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
        # give this instance an odor so it has a smell in the environment
        OdorSource(__name__,GroupSingle(self))
        # give health and endurance
        self.health = p.pro_max_health
        #self.endurance = p.pro_max_endurance
        
    def update(self):
        """
        put AI stuff here
        """
        """
        # endurance
        self.endurance += p.endurance_increase
        if self.endurance > p.pro_max_endurance:
            self.endurance = p.pro_max_endurance
            
        endurancePercent = self.endurance / p.pro_max_endurance
        self.speed = p.pro_max_speed * endurancePercent
        """
    
    def move(self, direction=None):
        Movable.move(self, direction=direction)
        #self.endurance -= p.endurance_decrease
        #if self.endurance <= 0:
        #    self.endurance = 0.0
        
