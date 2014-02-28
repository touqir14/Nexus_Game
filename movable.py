'''
Created on 2014-02-19

@author: User
'''
import math
import pygame
import parameters as p

class Movable():
    '''
    This class adds motion capability to screen objects like the protagonist.
    object must have a float position called 'pos' and a pygame rect called 'rect'
    '''


    def __init__(self, speed):
        '''
        Call this init to give these variables to the new instance
        '''
        self.speed = speed
        self.direction = (0.0,1.0)
        
    def move(self, direction=None):
        """
        Please only use 1, 0, or -1 for 'x' and 'y' as they will later be 
        multiplied by the objects speed.
        """
        if (direction == 'up'):
            self.direction = (0.0,-1.0)
        elif (direction == 'down'):
            self.direction = (0.0,1.0)
        elif (direction == 'left'):
            self.direction = (-1.0,0.0)
        elif (direction == 'right'):
            self.direction = (1.0,0.0)
        else:
            self.direction = (0.0,0.0)
        self.moveForward()            
    
    def moveToward(self,pointB):
        self.direction = unitVec(self.pos, pointB)
        self.moveForward()

    def moveForward(self):
        oldpos = self.pos
        self.pos = ( self.pos[0]+self.direction[0]*self.speed, 
                     self.pos[1]+self.direction[1]*self.speed )
        self.rect.center = self.pos
        
        # stay on the screen
        if not pygame.Rect(0,0,p.env_size[0],p.env_size[1]).contains(self.rect):
            self.pos = oldpos
            self.rect.center = self.pos

def unitVec(pointA, pointB):
    """
    Some vector math to find the ratio of x,y change on a unit triangle (hypotenuse == 1).
    x and y can later be multiplied by the objects 'speed' to ensure that 
    the hypotenuse between its old and new positions will be exactly equal to 'speed'.
    """
    side_a = pointB[0]-pointA[0]
    side_b = pointB[1]-pointA[1]
    hyp = math.hypot(side_a, side_b)
    if hyp == 0: return (0.0,0.0)
    return ((side_a / hyp),(side_b / hyp))

