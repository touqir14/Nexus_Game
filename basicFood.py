'''
Created on 2014-02-19

@author: User
'''
from pygame import sprite
import parameters as p

class BasicFood(sprite.Sprite):
    '''
    classdocs
    '''
    # add this class to the odors list so it has a smell in the environment
    p.odors.append(__name__)

    def __init__(self):
        '''
        Constructor
        '''
        pass