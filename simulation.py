'''
Created on 2014-02-19

@author: User
'''
from basicFood import BasicFood
import parameters as p
from protagonist import Protagonist
import pygame
from pygame.colordict import THECOLORS
from antagonist import Antagonist

class Simulation():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # destroy previous simulation
        for i in p.allObjects.sprites():
            i.kill()
        
        # zero time step
        p.timeStep = 0
        
        # create protagonist
        p.protagonist.add(Protagonist())
        p.antagonist.add(Antagonist())
        
        # create food items
        for i in range(p.startingFood):
            BasicFood((p.rand.randint(int(p.basicFoodDiameter/2), p.env_size[0]-int(p.basicFoodDiameter/2)),
                       p.rand.randint(int(p.basicFoodDiameter/2), p.env_size[1]-int(p.basicFoodDiameter/2))))
            #to do: retry if food is close to previous food or object?

        # create antagonist

    def run(self, env_screen):
        """
        calling this function represents one time step of the simulation
        """
        # update necessary things
        p.allObjects.update()
#        p.odors.update()
        
        # decrease health and check for death
        pro = p.protagonist.sprite
        if pro:
            pro.health -= p.health_step_decrease
            if pro.health <= 0:
                pro.kill()
        else:
            # back to menu
            p.startup = True
        
        # increment time step
        p.timeStep += 1
    
    def displayStats(self, screen):
        ## protagonist health bar
        drawText("Health:",screen,(10,1))
        # boarder of health bar for protagonist
        proHealthBar = pygame.Surface((p.info_size[0]-18,12))
        proHealthBar.fill(THECOLORS['black'])

        # back of health bar for protagonist
        back = pygame.Surface((proHealthBar.get_width()-2,proHealthBar.get_height()-2))
        back.fill(THECOLORS['red'])
        proHealthBar.blit(back,(1,1))

        # front of health bar for protagonist
        pro = p.protagonist.sprite
        if pro:
            healthPercent = pro.health / p.pro_max_health
            front = pygame.Surface(((proHealthBar.get_width()-2)*healthPercent,proHealthBar.get_height()-2))
            front.fill(THECOLORS['green'])
            proHealthBar.blit(front,(1,1))

        screen.blit(proHealthBar,(9,9))

        '''
        ## protagonist endurance bar
        drawText("Endurance:", screen, (10,26))
        # boarder of endurance bar for protagonist
        proEnduranceBar = pygame.Surface((p.info_size[0]-18,12))
        proEnduranceBar.fill(THECOLORS['black'])

        # back of endurance bar for protagonist
        back = pygame.Surface((proEnduranceBar.get_width()-2,proEnduranceBar.get_height()-2))
        back.fill(THECOLORS['red'])
        proEnduranceBar.blit(back,(1,1))

        # front of endurance bar for protagonist
        pro = p.protagonist.sprite
        if pro:
            endurancePercent = pro.endurance / p.pro_max_endurance
            front = pygame.Surface(((proEnduranceBar.get_width()-2)*endurancePercent,proEnduranceBar.get_height()-2))
            front.fill(THECOLORS['deepskyblue'])
            proEnduranceBar.blit(front,(1,1))

        screen.blit(proEnduranceBar,(9,34))
        '''

def drawText(text, screen, pos, size=15, colour=(200,255,200)):
    """
    helper function to simplify text to screen
    """
    f = pygame.font.Font(None,size)
    t = f.render(text,1,colour)
    screen.blit(t,pos)

        