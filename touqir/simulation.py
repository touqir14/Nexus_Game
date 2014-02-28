'''
Created on 2014-02-19

@author: User
'''
from basicFood import BasicFood
import parameters as pa
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
        self.p=pa.Parameters()
        # zero time step
        self.p.timeStep = 0
        # create protagonist

        self.init_images(self.p)
        
        #self.p.protagonist.add(self.x) touqir
        # create antagonist
        
        #self.p.antagonist.add(self.y) touqir
        self.p.PRO.append(Protagonist(self.p))
        self.p.ANT.append(Antagonist(self.p))
        # create food items
        for i in range(self.p.startingFood):
            self.p.FOOD.append(BasicFood(self.p,(self.p.rand.randint(int(self.p.basicFoodDiameter/2), self.p.env_size[0]-int(self.p.basicFoodDiameter/2)),
                       self.p.rand.randint(int(self.p.basicFoodDiameter/2), self.p.env_size[1]-int(self.p.basicFoodDiameter/2)))))
            #to do: retry if food is close to previous food or object?

    def init_images(self, parameters):
        BasicFood.image = pygame.Surface((parameters.basicFoodDiameter,parameters.basicFoodDiameter))
        BasicFood.image = BasicFood.image.convert_alpha()
        BasicFood.image.fill((0,0,0,0))
        pygame.draw.circle(BasicFood.image,parameters.basicFoodColour,BasicFood.image.get_rect().center,int(BasicFood.image.get_rect().width/2))

    def history_updater(self):
        """ records history of protagonist's game state, universal timestep, all the odour levels that the protagonist can smell, any rewards the protagonist gets"""
        child_history=[]
        child_history[0]=self.p.timeStep
        child_history[1]=self.pro_reward
        child_history[2]=self.pro_health
        child_history[3]=self.pro_location
        child_history[4]=self.odorlist
        #inorder to make sure that we keep recent history between index 0-999 of universal_history and remove far away past histories
        if len(self.p.universal_history)==1000:
            del self.p.universal_history[0]
            self.p.universal_history.append(child_history)
        else:
            self.p.universal_history.append(child_history)
    
    def run(self, env_screen):
        """
        calling this function represents one time step of the simulation
        """
        # increment time step
        self.p.timeStep += 1
        
        # update necessary things(updates protagonist, antagonist's, other objects's states)
        self.p.allObjects.update()
#        self.p.odors.update()

        # decrease health and check for death
        self.pro_list = self.p.protagonist.sprites() #returns a list of protagonist
        if self.pro_list:
            pro=self.pro_list[0]
        
            pro.health -= self.p.health_step_decrease
            if pro.health <= 0:
                pro.kill()

        

    def add_object(self, name, attribute=None):

        """
        adds any type of object to the simulation by creating them from their respective classes with the parameter "attribute" which is a lost containing multiple attributes like position, etc.
        It then stores the id of the instances so that the IDs can be used to call their functions or variables later
        """

        if name=='antagonist':
            self.p.ANT.append(Antagonist(self.p))

        if name=='protagonist':
            self.p.PRO.append(Protagonist(self.p))

        if name=='food':
            self.p.FOOD.append(BasicFood(self.p,()))



    def displayStats(self, screen):
        ## protagonist health bar
        drawText("Health:",screen,(10,1))
        # boarder of health bar for protagonist
        proHealthBar = pygame.Surface((self.p.info_size[0]-18,12))
        proHealthBar.fill(THECOLORS['black'])

        # back of health bar for protagonist
        back = pygame.Surface((proHealthBar.get_width()-2,proHealthBar.get_height()-2))
        back.fill(THECOLORS['red'])
        proHealthBar.blit(back,(1,1))

        # front of health bar for protagonist
        if self.pro_list:
            pro = self.pro_list[0]
        
            healthPercent = pro.health / self.p.pro_max_health
            front = pygame.Surface(((proHealthBar.get_width()-2)*healthPercent,proHealthBar.get_height()-2))
            front.fill(THECOLORS['green'])
            proHealthBar.blit(front,(1,1))

        screen.blit(proHealthBar,(9,9))

        '''
        ## protagonist endurance bar
        drawText("Endurance:", screen, (10,26))
        # boarder of endurance bar for protagonist
        proEnduranceBar = pygame.Surface((self.p.info_size[0]-18,12))
        proEnduranceBar.fill(THECOLORS['black'])

        # back of endurance bar for protagonist
        back = pygame.Surface((proEnduranceBar.get_width()-2,proEnduranceBar.get_height()-2))
        back.fill(THECOLORS['red'])
        proEnduranceBar.blit(back,(1,1))

        # front of endurance bar for protagonist
        pro = self.p.protagonist.sprite
        if pro:
            endurancePercent = pro.endurance / self.p.pro_max_endurance
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

