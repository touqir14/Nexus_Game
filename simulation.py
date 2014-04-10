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
from gridworld import GridWorld
import knn
from poisonFood import PoisonFood
import kmui
from dijkstra import search
from target import Target

class Simulation():
    '''
    classdocs
    '''

    def __init__(self, env_rect, envirogrid, mode=1):
        '''
        Constructor
        '''
        self.mode = mode
        heromovestyle = mode        # mode 1 = user control    2 = follow the clicks
        
        
        # destroy previous simulation
        for i in p.allObjects.sprites():
            i.kill()
        
        # zero time step
        p.timeStep = 0
        
        # create environment
        self.g_grid = pygame.sprite.GroupSingle()
        self.g_grid.add(envirogrid)
        
        # create protagonist
        p.protagonist.add(Protagonist(envirogrid, heromovestyle))
        
        self.placing = 0
        if mode == 1:
            ant_coord = (0,0)
            p.antagonist.add(Antagonist(envirogrid, ant_coord, self.mode))
            #adjust valuedict for antagonist
            envirogrid.value_dict[ant_coord].append(Antagonist.value)

            # place objects with mouse. placeable classes must take (grid, coord) as 
            # variables ie: BasicFood(grid, coord)
            
            self.placeable = [BasicFood, PoisonFood, Antagonist]
            
            # create food items, or do it later?
            #self.placeObjects(BasicFood, 20, envirogrid)
            # generate poison item
            #self.placeObjects(PoisonFood, 5, envirogrid)
        
        if mode == 2:
            self.placeable = [Target, BasicFood, PoisonFood]
            
            # create food items
            self.placeObjects(BasicFood, 30, envirogrid)
            # generate poison item
            self.placeObjects(PoisonFood, 15, envirogrid)        
        
        #for i in range(p.startingFood):
        #    BasicFood((p.rand.randint(int(p.basicFoodDiameter/2), p.env_size[0]-int(p.basicFoodDiameter/2)),
        #               p.rand.randint(int(p.basicFoodDiameter/2), p.env_size[1]-int(p.basicFoodDiameter/2))))
            #to do: retry if food is close to previous food or object?

        #self.knndict = knn.k_nearest_neighbour(envirogrid.value_dict, 4, (envirogrid.width-1,envirogrid.height-1))
        
    def run(self, env_screen, km_state):
        """
        calling this function represents one time step of the simulation
        """
        # centre grid on screen
        #self.g_grid.sprite.rect.center = env_screen.get_rect().center
        
        #update background grid
        #self.overlayweights()
        self.g_grid.update(km_state.mpos)
        
        
        # place new objects or delete them, based on mouse input
        if km_state.m_right == kmui.Clicked:
            self.placing = (self.placing+1)%len(self.placeable)
        if km_state.m_left == kmui.Clicked:
            mcoord = self.g_grid.sprite.convPosToCoord(km_state.mpos)
            item = self.g_grid.sprite.getItemAt(mcoord)
            if item:
                self.g_grid.sprite.removeItemAt(item,mcoord)
            else:
                self.placeObjectAt(self.placeable[self.placing], self.g_grid.sprite, mcoord)
                
        # maintain a certain number of objects on the screen
        if self.mode == 1:
            if len(p.g_food) < 20:
                self.placeObjects(BasicFood, 1, self.g_grid.sprite)
            if len(p.g_poison) < 5:
                self.placeObjects(PoisonFood, 1, self.g_grid.sprite)
        
        # update necessary things
        p.allObjects.update(km_state, self.g_grid.sprite)
#        p.odors.update()
        
        # decrease health and check for death
        pro = p.protagonist.sprite
        if pro:
            pro.health -= p.health_step_decrease if self.mode != 2 else 0
            if pro.health <= 0:
                pro.kill()
        else:
            # back to menu
            p.startup = True
        
        
        # increment time step
        p.timeStep += 1
    
    def drawWorld(self, screen):
        self.g_grid.draw(screen)
        
    def overlayweights(self):
        pro = p.protagonist.sprite
        if pro:
            weights = pro.knnweights
        if weights:
            heaviest = {}
            for k,v in weights.items():
                d,win = v
                print('')
                heaviest[k] = d[win][-1]
                
            print('#####')
            for i in heaviest.values():
                print(i)
            print('#####')
             
            low = min(heaviest, key=lambda x: heaviest[x])
            high = max(heaviest, key=lambda x: heaviest[x])
             
            new = {}
            for k,v in heaviest.items():
                new[k] = self.map255(v, heaviest[low], heaviest[high])
            print(new)
             
            grid = self.g_grid.sprite
            for k,v in new.items():
                grid.blockdict[k].sprite.other = True
                #print(v)
                grid.blockdict[k].sprite.bgc[2] = (v,v,v)
                 
#             print('#####')
#             l = set(heaviest.values())
#             for i in l:
#                 print(i)
    
    def map255(self, val, in_min, in_max, out_min=50, out_max=200):
        # taken from arduino.cc
        if (in_max - in_min) + out_min < 0.000000001:
            return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        else:
            return 0

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
            healthPercent = pro.health / pro.max_health
            front = pygame.Surface(((proHealthBar.get_width()-2)*healthPercent,proHealthBar.get_height()-2))
            front.fill(THECOLORS['green'])
            proHealthBar.blit(front,(1,1))

        screen.blit(proHealthBar,(9,19))
        
        # mode specific display
        # timer for user control mode
        if self.mode == 1:
            txt = "Survival time: {}.{}".format(p.timeStep//p.fps,int(p.timeStep%p.fps*3.3))
            drawText(txt,screen,(10,50))
            
        # knn stuff for mode 2
        elif self.mode == 2:
            pro = p.protagonist.sprite
            if pro:
                txt = "k neighbours: {}".format(pro.k_of_KNN)
                drawText(txt,screen,(325,45))
                txt = '[mouse wheel] to change'
                drawText(txt,screen,(325,67),20)

                txt = "KNN approach: {}".format('Weighted' if pro.approach_of_KNN else 'Prababilistic')
                drawText(txt,screen,(10,45))
                txt = '[k] to change'
                drawText(txt,screen,(10,67),20)
        
        # what are I placing with the mouse clicks?
        pos = (600,45)
        drawText("Placing:",screen,pos)
        drawText("[left mouse] to place",screen,(pos[0],pos[1]+22),20)
        drawText("[right mouse] to change",screen,(pos[0],pos[1]+40),20)
        imgOfPlacing = self.placeable[self.placing].image
        prect = imgOfPlacing.get_rect()
        screen.blit(imgOfPlacing,((pos[0]+87)-prect.center[0],(pos[1]+8)-prect.center[1]))

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
    
    def generatefood(self, amount, grid):
        """
        place food on environment grid in such a way that no more than one food is placed per tile
        """
        possiblecoords = grid.emptytiles()#[(x,y) for x in range(grid.width) for y in range(grid.height)]
        # at this point the hero's coordinate should be removed from the list
        #possiblecoords = possiblecoords[:-1]
        for n in range(amount):
            if len(possiblecoords) <= 0: break # no more room for foods
            coord = p.rand.choice(possiblecoords)
            grid.value_dict[coord].append(BasicFood.value)
            BasicFood(grid, coord)#(p.rand.randint(0, gridwidth-1),p.rand.randint(0, gridwidth-1)))
            possiblecoords.remove(coord)

    def placeObjects(self, objclass, amount, grid):
        """
        place objects on environment grid in such a way that no more than one is placed per tile
        """
        possiblecoords = grid.emptytiles()
        for n in range(amount):
            if len(possiblecoords) <= 0: break # no more room for objects
            coord = p.rand.choice(possiblecoords)
            grid.value_dict[coord].append(objclass.value)
            grid.trackObj(objclass(grid, coord), coord)
            possiblecoords.remove(coord)

    def placeObjectAt(self, objclass, grid, coord):
        """
        place object on environment grid at a specified tile if tile is empty
        """
        possiblecoords = grid.emptytiles()
        if coord in possiblecoords:
            if objclass != Target: grid.value_dict[coord].append(objclass.value)
            if objclass == Antagonist:
                grid.trackObj(objclass(grid, coord, self.mode), coord)
            else:
                grid.trackObj(objclass(grid, coord), coord)

def drawText(text, screen, pos, size=25, colour=(200,255,200)):
    """
    helper function to simplify text to screen
    """
    f = pygame.font.Font(None,size)
    t = f.render(text,1,colour)
    screen.blit(t,pos)

        