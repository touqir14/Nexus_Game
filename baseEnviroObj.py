'''
Created on 2014-04-04

@author: User
'''
import pygame
import parameters as p

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
        self.coord = envirogrid.closestGridCoord(startcoord)
        #self.coord = startcoord
        self.rect.center = envirogrid.getcenter(self.coord)
        