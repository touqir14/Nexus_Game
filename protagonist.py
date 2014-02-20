'''
Created on 2014-02-19

@author: User
'''
from pygame.sprite import Sprite
import parameters as p
import pygame
from movable import Movable

class Protagonist(Sprite, Movable):
    '''
    classdocs
    '''
    # add this class to the odors list so it has a smell in the environment
    p.odors.append(__name__)
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
        Movable.__init__(self, p.pro_speed)
        
        # add instance to simulation list groups and control group
        p.allObjects.add(self)
        p.protagonist.add(self)
        # give position
        self.rect.center = p.pro_starting_point
        self.pos = (float(self.rect.center[0]),float(self.rect.center[1]))
        
        