from pygame.sprite import GroupSingle
import parameters as p
import pygame
from movable import Movable
from odor import OdorSource
import search_algorithms

class Antagonist(Movable):
    """
    RAWRRR!!!! all i want to do is eat the protagonist!! i will chase it forever!
    """
    # give the antagonist an image
    image = pygame.Surface((p.ant_diameter,p.ant_diameter))
    image.fill(p.ant_colour)
    
    # how much the hero (or any environment object?) will be affected by this type of game object
    effectvalue = -20

    # a value is given to all environment object classes that tell them if the hero likes them or not
    # for KNN functions.
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
            targcoord = search_algorithms.A_star_chaser(self.coord, pro.coord, grid.value_dict)
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

        if self.value in touqirs_value_dict[self.coord]:
            touqirs_value_dict[self.coord].remove(self.value)

        # regulate obj health. dead?
        env_obj.regulatehealth()
