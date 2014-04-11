import math
from baseEnviroObj import BaseEnviroObj

class Movable(BaseEnviroObj):
    '''
    This class adds motion capability to screen objects like the protagonist.
    object must have a float position called 'pos' and a pygame rect called 'rect'
    
    some of the methods were targeted for diagonal movement but they work on a grid anyway.
    '''

    def __init__(self, speed, envirogrid, image, startcoord=(0,0)):
        '''
        Call this init to give these variables to the new instance
        '''
        super().__init__(image, envirogrid, startcoord)
        self.speed = speed
        self.direction = (0.0,1.0)
        self.edgecheck = envirogrid.edgecondition
        self.pos = envirogrid.getcenter #convCoordToPos
        
        # limit the rate of movement with a frame countdown
        self.rateOfMovement = 6 
        self.movementCountdown = 0
        
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
    
    def moveToward(self,coord):
        self.direction = unitVec(self.coord, coord)
        self.moveForward()

    def moveForward(self):
        if self.movementCountdown <= 0:
            self.resetMoveCountdown()

    #        oldcoord = self.coord
            newcoord = ( self.coord[0]+self.direction[0]*self.speed, 
                         self.coord[1]+self.direction[1]*self.speed )
    
            # stay on the screen
            self.coord = self.edgecheck(newcoord)
            
            # place rect on correct tile position
            newpos = self.pos(self.coord)
            if newpos:
                self.rect.center = newpos
            else:
                print("invalid position for protagonist")
            
            # stay on the screen
            #if not pygame.Rect(0,0,p.env_size[0],p.env_size[1]).contains(self.rect):
            #    self.coord = oldcoord
            #    self.rect.center = self.place(self.coord)
        
    def decreaseMoveCountdown(self):
        self.movementCountdown -= 1
        if self.movementCountdown < 0:
            self.movementCountdown = 0
            
    def resetMoveCountdown(self):
        self.movementCountdown = self.rateOfMovement

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

