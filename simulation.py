'''
Created on 2014-02-19

@author: User
'''
from pygame import sprite
from basicFood import BasicFood

class Simulation():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.food = sprite.Group(BasicFood())