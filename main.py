'''
Created on 2014-02-18

@author: Matt Jorgensen

Run the program from this main file.
'''
import os, sys, pygame
from pygame.locals import *
import parameters as p
from simulation import Simulation
from basicFood import BasicFood
from introPage import IntroPage
from poisonFood import PoisonFood
import kmui

def imageSetup():
    """ 
    Should find another way to do this. But for now, 
    this allows the images to be set up after calling 'pygame.init()'
    rather than from within each class that has an image (where 
    'pygame.init()' is not called)
    """
    # regular green food
    BasicFood.image = BasicFood.image.convert_alpha()
    BasicFood.image.fill((0,0,0,0))
    pygame.draw.circle(BasicFood.image,p.basicFoodColour,BasicFood.image.get_rect().center,int(BasicFood.image.get_rect().width/2))
    
    # poison food
    PoisonFood.image = PoisonFood.image.convert_alpha()
    PoisonFood.image.fill((0,0,0,0))
    pygame.draw.circle(PoisonFood.image,PoisonFood.colour,PoisonFood.image.get_rect().center,int(PoisonFood.image.get_rect().width/2))
    
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
    
    # interface event handler
    km_state = kmui.KMState()
    
    # other housekeeping (some image setup needs to go after 'pygame.init()')
    imageSetup()
    
    #
    iPage = IntroPage()
    
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
            if e.type in (MOUSEBUTTONDOWN,MOUSEBUTTONUP,MOUSEMOTION,KEYDOWN,KEYUP):
                km_state.updateState(e)
#             if e.type == MOUSEBUTTONDOWN:
#                 p.leftMouse = True
#             if e.type == MOUSEBUTTONUP:
#                 p.leftMouse = False
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    if p.startup:
                        # safely exit the system
                        pygame.quit()
                        sys.exit()
                    else:
                        # back to menu
                        p.startup = True
                if e.key == K_o:
                    p.show_odors^=True # toggle true false

#                 if e.key == K_UP:
#                     p.up = True
#                 if e.key == K_DOWN:
#                     p.down = True
#                 if e.key == K_LEFT:
#                     p.left = True
#                 if e.key == K_RIGHT:
#                     p.right = True
#             if e.type == KEYUP:
#                 if e.key == K_UP:
#                     p.up = False
#                 if e.key == K_DOWN:
#                     p.down = False
#                 if e.key == K_LEFT:
#                     p.left = False
#                 if e.key == K_RIGHT:
#                     p.right = False

        # user controlled movement of protagonist
        '''
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
        '''
                
        if p.startup:
            #iPage.update(pygame.mouse.get_pos())
            # create a new simulation
            env_rect = env_screen.get_rect()
            sim = iPage.generateSim(km_state, env_rect, gridunit=30, gridwidth=26, gridheight=16)
            if sim != None:
                p.startup = False
                
            # draw the intro page
            iPage.draw(screen)
        else:
            # cover old screen with a healthy coat of [background colour]
            env_screen.fill(p.env_bgc)
            info_screen.fill(p.info_bgc)
            
            # run simulation
            sim.run(env_screen, km_state)
            
            # proliferate odors
            if p.show_odors: p.odorSources.update()
            #for i in p.odorSources:
            #    i.proliferate()
            
            # draw the environment
            sim.drawWorld(env_screen)
            p.allObjects.draw(env_screen)
            if p.show_odors: p.odorSources.draw(env_screen)
            
            # show the numbers and life bars
            sim.displayStats(info_screen)
            
            # flip the screen
            screen.blit(env_screen,(p.border,p.border))
            screen.blit(info_screen,(p.border,p.resolution[1]-p.info_size[1]-p.border))
        pygame.display.flip()
                
        # refresh mouse state at end of every loop
        km_state.refresh()
        
        # delay the simulation if it is running too fast
        clock.tick(p.fps)

    