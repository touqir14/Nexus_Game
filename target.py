import pygame
from baseEnviroObj import BaseEnviroObj

class Target(BaseEnviroObj):
    '''
    this object gives the hero something to chase after.
    there should only be one at a time on the board
    '''
    g_targ = pygame.sprite.GroupSingle()
    unit = 24 #for adjusting the size of the target ie: unit size
    image = pygame.Surface((unit,unit))
    colour = (250,100,100)

    value = 0


    def __init__(self, envirogrid, startcoord):
        '''
        Constructor
        '''
        super().__init__(Target.image, envirogrid, startcoord)
        
        Target.g_targ.add(self)

