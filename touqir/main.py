'''
Created on 2014-02-18

@author: Matt Jorgensen

Run the program from this main file.
'''
import os, sys, pygame
from pygame.locals import *
from pygame.colordict import THECOLORS
from simulation import Simulation
from basicFood import BasicFood
import parameters as p

#Global variable
mode1=True
mode2=False
show_odors=False

def game_mode1():
    # user controlled movement of protagonist
    # other housekeeping (some image setup needs to go after 'pygame.init()')
    
    pro_list=sim1.p.protagonist.sprites()
    if pro_list:
        pro=pro_list[0]
        pro_id = sim1.p.PRO[0]
        if pro_id==pro:
            if p.up == True:
                pro.move('up')
            if p.down == True:
                pro.move('down')
            if p.left == True:
                pro.move('left')
            if p.right == True:
                pro.move('right')

    env_screen.fill(sim1.p.env_bgc)
    info_screen.fill(sim1.p.info_bgc)       # <--(might not want to erase this display every loop)
    
    # run simulation(in other words, update the game states and increase timestep by 1)
    sim1.run(env_screen)
    
    # proliferate odors
    if sim1.p.show_odors: sim1.p.odorSources.update()
    #for i in sim1.p.odorSources:
    #    i.proliferate()
    
    # draw the environment(it draws sprites to the surface)
    sim1.p.allObjects.draw(env_screen)
    if sim1.p.show_odors: sim1.p.odorSources.draw(env_screen)
    
    # show the numbers and life bars
    sim1.displayStats(info_screen)
    
    # flip the screen(draws the surface every loop)
    screen.blit(env_screen,(1,1))
    screen.blit(info_screen,(1,sim1.p.resolution[1]-sim1.p.info_size[1]-1))
    pygame.display.flip()
            
    # limit framerate to 30fps as sim1.p.fps=30
    clock.tick(p.fps)

#def game_mode2():
    #AI controlled movement of protagonist
    
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

    # create simulations, sim1 for mode1 and sim2 for mode2
    sim1 = Simulation()
    sim2 = Simulation()
    
    # create a clock to time the simulation
    clock = pygame.time.Clock()
    
    # main Game loop
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
                    show_odors^=True # toggle true false
                if e.key == K_UP:
                    p.up = True
                if e.key == K_DOWN:
                    p.down = True
                if e.key == K_LEFT:
                    p.left = True
                if e.key == K_RIGHT:
                    p.right = True
                if e.key == K_1:
                    mode1 = True
                    mode2 = False
                if e.key == K_2:
                    mode1 = False
                    mode2 = True
            if e.type == KEYUP:
                if e.key == K_UP:
                    p.up = False
                if e.key == K_DOWN:
                    p.down = False
                if e.key == K_LEFT:
                    p.left = False
                if e.key == K_RIGHT:
                    p.right = False

        if mode1:
            if show_odors==True:sim1.p.show_odors=True
            else: sim1.p.show_odors=False
            game_mode1()
            
        else :
            if show_odors==True:sim2.p.show_odors=True
            else: sim2.p.show_odors=False
            game_mode2()
            
        
        
        
    
