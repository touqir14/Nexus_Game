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
                if e.key == K_UP:
                    p.up = True
                    print("{}".format(p.odors))
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
        if pro:
            if p.up == True:
                pro.move('up')
            if p.down == True:
                pro.move('down')
            if p.left == True:
                pro.move('left')
            if p.right == True:
                pro.move('right')
        
        # cover old screen with a healthy coat of grey
        env_screen.fill(THECOLORS['grey'])
        info_screen.fill(THECOLORS['grey10'])       # <--(might not want to erase this display every loop)
        
        # run simulation
        sim.run(env_screen)
        
        # proliferate odors
        for i in p.odorSources:
            i.proliferate()
        
        # draw the environment
        p.allObjects.draw(env_screen)
        
        # show the numbers and life bars
        sim.displayStats(info_screen)
        
        # flip the screen
        screen.blit(env_screen,(0,0))
        screen.blit(info_screen,(0,p.resolution[1]-p.info_size[1]))
        pygame.display.flip()
                
        # delay the simulation if it is running too fast
        clock.tick(p.fps)

    