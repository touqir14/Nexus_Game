'''
Created on 2014-02-18

@author: Matt Jorgensen

Run the program from this main file.
'''
import os, sys, pygame
from pygame.locals import *
import parameters as p
from pygame.colordict import THECOLORS

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
                    print("{}".format(p.odors))
        
        # cover old screen with a healthy coat of grey
        env_screen.fill(THECOLORS['grey'])
        info_screen.fill(THECOLORS['purple'])       # <--(might not erase this display every loop)
        
        # run simulation
        
        # flip the screen
        screen.blit(env_screen,(0,0))
        screen.blit(info_screen,(0,p.resolution[1]-p.info_size[1]))
        pygame.display.flip()
                
        # delay the simulation if it is running too fast
        clock.tick(p.fps)
        
        # advance timeStep
        p.timeStep += 1
        