'''
Created on 2014-02-26

@author: User
'''
import pygame
import parameters as p
import simulation
import kmui

class IntroPage():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.opt1_rect = pygame.Rect(int((p.resolution[0]-200)/2),int((p.resolution[1]-30)/2),200,30)
        self.opt1_highlight = 0
        
    def generateSim(self, km_state, env_rect, gridunit, gridwidth, gridheight):
        if self.opt1_rect.collidepoint(km_state.mpos):
            self.opt1_highlight = 20
            if km_state.m_left == kmui.Released:
                return simulation.Simulation(env_rect, gridunit, gridwidth, gridheight)
        else:
            self.opt1_highlight = 0
        
        return None
        
    def update(self, mpos):
        if self.opt1_rect.collidepoint(mpos):
            self.opt1_highlight = 20
        else:
            self.opt1_highlight = 0
        
    def draw(self, screen):
        """
        display options for grid size, amount of food, odor intensity etc.
        """
        # menu background
        w,h = 250,300
        topleft = int((p.resolution[0]-w)/2),int((p.resolution[1]-h)/2)
        pygame.draw.rect(screen,(130,70,70),(topleft[0],topleft[1],w,h))
        pygame.draw.rect(screen,(0,0,0),(topleft[0]-p.border+1,topleft[1]-p.border+1,w+p.border,h+p.border),p.border)
        simulation.drawText("Simulation Type:", screen, (topleft[0]+int(w*0.04),topleft[1]+int(h*0.1)), 40)
        
        # option one
        self.opt1_rect = pygame.Rect(int((p.resolution[0]-int(w*0.8))/2),int((p.resolution[1]-32-int(h*0.3))/2),int(w*0.8),32)
        pygame.draw.rect(screen,(190+self.opt1_highlight,130+self.opt1_highlight,130+self.opt1_highlight),self.opt1_rect)
        simulation.drawText("User Controlled", screen, (self.opt1_rect.center[0]-80,self.opt1_rect.center[1]-9), 30)