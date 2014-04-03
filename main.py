'''
Created on 2014-02-18

@author: Matt Jorgensen

Run the program from this main file.
'''
import os, sys, pygame
from pygame.locals import *
import parameters as p
from pygame.colordict import THECOLORS
from simulation import Simulation
from basicFood import BasicFood
<<<<<<< HEAD
from introPage import IntroPage
from gridworld import GridWorld
=======
>>>>>>> parent of 3817c33... menu and border condition

def imageSetup():
    """ Should find another way to do this """
    BasicFood.image = BasicFood.image.convert_alpha()
    BasicFood.image.fill((0,0,0,0))
    pygame.draw.circle(BasicFood.image,p.basicFoodColour,BasicFood.image.get_rect().center,int(BasicFood.image.get_rect().width/2))
    
if __name__ == '__main__':
    # put the window in the centre of your monitor
    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
    
    # initialize pygame and the main drawing surface
    pygame.init()
    screen = pygame.display.set_mode(p.resolution)
    # environment drawing surface
    env_screen = pygame.Surface(p.env_size)
    # information display surface
    info_screen = pygame.Surface(p.info_size)
    
    # init components
    Gunit = 30
    Gwidth = 26
    Gheight = 16
    grid = pygame.sprite.GroupSingle()
    grid.add(GridWorld(Gunit, Gwidth, Gheight))
    
    # other housekeeping (some image setup needs to go after 'pygame.init()')
    imageSetup()
    
    # create a new simulation
    sim = Simulation()
    
    # create a clock to time the simulation
    clock = pygame.time.Clock()
    
    # main loop
    while True:
        # handle different events
        for e in pygame.event.get():
            if e.type == QUIT: 
                # safely exit the system
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    # safely exit the system
                    pygame.quit()
                    sys.exit()
                if e.key == K_o:
                    p.show_odors^=True # toggle true false
                if e.key == K_UP:
                    p.up = True
                if e.key == K_DOWN:
                    p.down = True
                if e.key == K_LEFT:
                    p.left = True
                if e.key == K_RIGHT:
                    p.right = True
            if e.type == KEYUP:
                if e.key == K_UP:
                    p.up = False
                if e.key == K_DOWN:
                    p.down = False
                if e.key == K_LEFT:
                    p.left = False
                if e.key == K_RIGHT:
                    p.right = False

        # user controlled movement of protagonist
        pro = p.protagonist.sprite
        grd = grid.sprite
        if pro and grd:
            if p.up == True:
                pro.move('up', grd.closestGridCoord, grd.getcenter)
            if p.down == True:
                pro.move('down', grd.closestGridCoord, grd.getcenter)
            if p.left == True:
                pro.move('left', grd.closestGridCoord, grd.getcenter)
            if p.right == True:
<<<<<<< HEAD
                pro.move('right', grd.closestGridCoord, grd.getcenter)
                
        if p.startup:
            #iPage.update(pygame.mouse.get_pos())
            # create a new simulation
            sim = iPage.generateSim(pygame.mouse.get_pos(), grid.sprite)
            if sim != None:
                p.startup = False
                
            # draw the intro page
            iPage.draw(screen)
        else:
            # cover old screen with a healthy coat of [background colour]
            env_screen.fill(p.env_bgc)
            info_screen.fill(p.info_bgc)
            grid.update()
            grid.draw(env_screen)
            
            # run simulation
            sim.run(env_screen, grid.sprite)
            
            # proliferate odors
            if p.show_odors: p.odorSources.update()
            #for i in p.odorSources:
            #    i.proliferate()
            
            # draw the environment
            p.allObjects.draw(env_screen)
            if p.show_odors: p.odorSources.draw(env_screen)
            
            # show the numbers and life bars
            sim.displayStats(info_screen)
            
            # flip the screen
            screen.blit(env_screen,(p.border,p.border))
            screen.blit(info_screen,(p.border,p.resolution[1]-p.info_size[1]-p.border))
=======
                pro.move('right')
        
        # cover old screen with a healthy coat of grey
        env_screen.fill(p.env_bgc)
        info_screen.fill(p.info_bgc)       # <--(might not want to erase this display every loop)
        
        # run simulation
        sim.run(env_screen)
        
        # proliferate odors
        if p.show_odors: p.odorSources.update()
        #for i in p.odorSources:
        #    i.proliferate()
        
        # draw the environment
        p.allObjects.draw(env_screen)
        if p.show_odors: p.odorSources.draw(env_screen)
        
        # show the numbers and life bars
        sim.displayStats(info_screen)
        
        # flip the screen
        screen.blit(env_screen,(1,1))
        screen.blit(info_screen,(1,p.resolution[1]-p.info_size[1]-1))
>>>>>>> parent of 3817c33... menu and border condition
        pygame.display.flip()
                
        # delay the simulation if it is running too fast
        clock.tick(p.fps)

    