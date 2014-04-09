'''
Created on 2014-02-26

@author: User
'''
import pygame
import parameters as p
import simulation
import kmui
import sys
from gridworld import GridWorld

class IntroPage():
    '''
    classdocs
    '''

    def __init__(self, mousepos):
        '''
        'mousepos' must be a function linked from the kmui module. it should return the current mouse position
        '''
        self.menu_w, self.menu_h = 250,300
        btnrect = pygame.Rect(int((p.resolution[0]-int(self.menu_w*0.8))/2),int((p.resolution[1]-32-int(self.menu_h*0.3))/2),int(self.menu_w*0.8),32)
        self.opt1_rect = pygame.Rect(btnrect)#pygame.Rect(int((p.resolution[0]-200)/2),int((p.resolution[1]-30)/2),200,30)
        self.opt2_rect = pygame.Rect(btnrect)
        self.opt2_rect.move_ip(0,50)
        self.opt3_rect = pygame.Rect(btnrect)
        self.opt3_rect.move_ip(0,150)
        self.btncolor = (190,130,130)
        hl = 20
        #self.currentmousepos = (0,0)
        self.highlight = (self.btncolor[0]+hl,self.btncolor[1]+hl,self.btncolor[2]+hl)
        self.btn1color = lambda: self.highlight if self.opt1_rect.collidepoint(mousepos()) else self.btncolor
        self.btn2color = lambda: self.highlight if self.opt2_rect.collidepoint(mousepos()) else self.btncolor
        self.btn3color = lambda: self.highlight if self.opt3_rect.collidepoint(mousepos()) else self.btncolor
        
    def generateSim(self, km_state, env_rect, gridunit, gridwidth, gridheight):        
        if km_state.m_left == kmui.Released:
            if self.btn1color() == self.highlight:
                # start the game with settings for user control
                grid = GridWorld(env_rect, gridunit, gridwidth, gridheight)
                return simulation.Simulation(env_rect, grid, mode=1)
            elif self.btn2color() == self.highlight:
                # start the game with settings for avoiding the obstacles
                grid = GridWorld(env_rect, gridunit, gridwidth, gridheight)
                return simulation.Simulation(env_rect, grid, mode=2)
            elif self.btn3color() == self.highlight:
                # exit the game
                pygame.quit()
                sys.exit()                
        
        return None
        
    def update(self, mpos):
        #self.currentmousepos = mpos
        '''
        if self.opt1_rect.collidepoint(mpos):
            self.opt1_highlight = 20
        else:
            self.opt1_highlight = 0
        '''

    def draw(self, screen):
        """
        display options for grid size, amount of food, odor intensity etc.
        """
        # menu background
        
        topleft = int((p.resolution[0]-self.menu_w)/2),int((p.resolution[1]-self.menu_h)/2)
        pygame.draw.rect(screen,(130,70,70),(topleft[0],topleft[1],self.menu_w,self.menu_h))
        pygame.draw.rect(screen,(0,0,0),(topleft[0]-p.border+1,topleft[1]-p.border+1,self.menu_w+p.border,self.menu_h+p.border),p.border)
        simulation.drawText("Simulation Type:", screen, (topleft[0]+int(self.menu_w*0.04),topleft[1]+int(self.menu_h*0.1)), 40)
        
        # basic button values
        
        # option one
        #(btncolor[0]+self.opt1_highlight,btncolor[1]+self.opt1_highlight,btncolor[2]+self.opt1_highlight)
        pygame.draw.rect(screen,self.btn1color(),self.opt1_rect)
        simulation.drawText("User Controlled", screen, (self.opt1_rect.center[0]-80,self.opt1_rect.center[1]-9), 30)
        
        # option two
        pygame.draw.rect(screen,self.btn2color(),self.opt2_rect)
        simulation.drawText("Automatic Avoid", screen, (self.opt2_rect.center[0]-80,self.opt2_rect.center[1]-9), 30)
        
        # option three
        pygame.draw.rect(screen,self.btn3color(),self.opt3_rect)
        simulation.drawText("Quit", screen, (self.opt3_rect.center[0]-80,self.opt3_rect.center[1]-9), 30)
        
