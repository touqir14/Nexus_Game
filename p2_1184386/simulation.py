from basicFood import BasicFood
import parameters as p
from protagonist import Protagonist
import pygame
from pygame.colordict import THECOLORS
from antagonist import Antagonist
from poisonFood import PoisonFood
import kmui
from target import Target

class Simulation():
    """
    chose a game mode and this class will set the board and display 
    with the appropriate components.  
    """

    def __init__(self, env_rect, envirogrid, km_state, mode=1):
        '''
        Constructor
        '''
        self.mode = mode
        
        # destroy previous simulation
        for i in p.allObjects.sprites():
            i.kill()
        km_state.links = set()
        
        # zero time step (counts the number of loops)
        p.timeStep = 0
        
        # create environment
        self.g_grid = pygame.sprite.GroupSingle()
        self.g_grid.add(envirogrid)
        
        # create protagonist
        p.protagonist.add(Protagonist(envirogrid, km_state, mode))
        
        # index of object placement with the mouse
        self.placing = 0
        
        # mode specific preparation
        if mode == 1:
            # create Antagonist
            ant_coord = (0,0)
            p.antagonist.add(Antagonist(envirogrid, ant_coord, self.mode))
            # adjust valuedict to include antagonist
            envirogrid.value_dict[ant_coord].append(Antagonist.value)
            # place objects with mouse. placeable classes must take (grid, coord) as 
            # variables ie: BasicFood(grid, coord)
            self.placeable = [BasicFood, PoisonFood, Antagonist]
        
        if mode == 2:
            self.placeable = [Target, BasicFood, PoisonFood]
            # create food items
            self.placeObjects(BasicFood, 30, envirogrid)
            # generate poison item
            self.placeObjects(PoisonFood, 15, envirogrid)
            
        # button to clear the grid of food
        self.clrbtnrect = pygame.Rect(705,5,80,25)
        r,g,b,h = (100,100,100,30)
        m = lambda: (km_state.mpos[0],km_state.mpos[1]-p.env_size[1])
        self.clrbtnhighlight = (r+h,g+h,b+h)
        self.clrbtncolor = lambda: (r+h,g+h,b+h) if self.clrbtnrect.collidepoint(m()) else (r,g,b)
        
    def run(self, env_screen, km_state):
        """
        calling this function represents one time step of the simulation
        it will update all the game objects on the board here.
        """
        # centre grid on screen
        #self.g_grid.sprite.rect.center = env_screen.get_rect().center
        
        # graphically show the KNN wieghts for path finding
        if p.weightvisual:
            self.overlayweights()
        
        #update background grid
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
            if len(p.g_food) < 10:
                self.placeObjects(BasicFood, 1, self.g_grid.sprite)
            if len(p.g_poison) < 5:
                self.placeObjects(PoisonFood, 1, self.g_grid.sprite)
        
        # never empty the screen completely. (it's not a glitch, it's a feature)
        if self.mode == 2:
            if len(p.g_poison) < 1:
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
        
        # clear the food and poison from the screen
        if self.mode == 2 and self.clrbtncolor() == self.clrbtnhighlight and km_state.m_left == kmui.Released:
            for pellet in p.g_food.sprites()+p.g_poison.sprites():
                pellet.kill()
                grid = self.g_grid.sprite
                if grid:
                    grid.value_dict[pellet.coord].remove(pellet.value)
        
        # increment time step
        p.timeStep += 1
    
    def drawWorld(self, screen):
        self.g_grid.draw(screen)
        
    def overlayweights(self):
        """
        this is a newer method so it may be unrefined, but it's meant to 
        show the calculated weights from the KNN algorithm.
        
        At this point it's only showing the weights of the tiles that have 
        the pink 'poisonFood' neighbours.
        """
        grid = self.g_grid.sprite
        # reset tiles
        for k,v in grid.blockdict.items():
            grid.blockdict[k].sprite.other = False
        pro = p.protagonist.sprite
        if pro:
            # leave if KNN aproach is not 'Weighted'
            if pro.approach_of_KNN != 1:
                return
            weights = pro.knnweights
        if weights:
            heaviest = {}
            for k,v in weights.items():
                d,win = v
                #print(win)
                # only get the values for poison neighbours! (where key == 0)
                h = d.get(0)
                if h:
                    heaviest[k] = h[-1]
             
            low = min(heaviest, key=lambda x: heaviest[x])
            high = max(heaviest, key=lambda x: heaviest[x])
            #print(heaviest[low], heaviest[high])
            
            new = {}
            for k,v in heaviest.items():
                new[k] = self.map255(v, heaviest[low], heaviest[high])
            #print(new)
             
            for k,v in new.items():
                grid.blockdict[k].sprite.other = True
                # set the background colour of the grid tiles based on the weight
                grid.blockdict[k].sprite.bgc[2] = (v,40,0)
    
    def map255(self, val, in_min, in_max, out_min=50.0, out_max=250.0):
        # taken from www.arduino.cc
        if (in_max - in_min) + out_min > 0.000000001:
            return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        else:
            return 0

    def displayStats(self, screen):
        """
        This method makes the display area at the bottom of the screen.
        """
        ## protagonist health bar
        hbsize = (p.info_size[0]//2-10,12)#-(110 if self.mode==2 else 20),12)
        drawText("Protagonist Health",screen,(10,1))
        # boarder of health bar for protagonist
        proHealthBar = pygame.Surface(hbsize)
        proHealthBar.fill(THECOLORS['black'])

        # back of health bar for protagonist
        back = pygame.Surface((hbsize[0]-2,hbsize[1]-2))
        back.fill(THECOLORS['red'])
        proHealthBar.blit(back,(1,1))

        # front of health bar for protagonist
        pro = p.protagonist.sprite
        if pro:
            healthPercent = pro.health / pro.max_health
            front = pygame.Surface(((hbsize[0]-2)*healthPercent,hbsize[1]-2))
            front.fill(THECOLORS['green'])
            proHealthBar.blit(front,(1,1))

        screen.blit(proHealthBar,(9,19))
        
        # mode specific display
        if self.mode == 1:
            ## antagonist health bar
            drawText("Antagonist Health",screen,(p.info_size[0]//2+225,1))
            # boarder of health bar for antagonist
            antHealthBar = pygame.Surface(hbsize)
            antHealthBar.fill(THECOLORS['black'])
    
            # back of health bar for antagonist
            back = pygame.Surface((hbsize[0]-2,hbsize[1]-2))
            back.fill(THECOLORS['red'])
            antHealthBar.blit(back,(1,1))
    
            # front of health bar for antagonist
            ant = p.antagonist.sprite
            if ant:
                
                healthPercent = ant.health / ant.max_health
                front = pygame.Surface(((hbsize[0]-2)*healthPercent,hbsize[1]-2))
                front.fill(THECOLORS['blue'])
                antHealthBar.blit(front,(1,1))
    
            screen.blit(antHealthBar,(p.info_size[0]//2,19))
            
            # timer for user control mode
            txt = "Survival time: {}.{}".format(p.timeStep//p.fps,int(p.timeStep%p.fps*3.3))
            drawText(txt,screen,(10,50))
            
            x,y = (295,50)
            txt = "Use arrow keys to move."
            drawText(txt,screen,(x,y))
            txt = "[ESCAPE] for the menu."
            drawText(txt,screen,(x,y+20))

        # knn stuff for mode 2
        elif self.mode == 2:
            pro = p.protagonist.sprite
            if pro:
                x,y = (325,38)
                txt = "k neighbours: {}".format(pro.k_of_KNN)
                drawText(txt,screen,(x,y))
                txt = '[mouse wheel] to change'
                drawText(txt,screen,(x,y+22),20)

                x = 10
                txt = "KNN approach: {}".format('Weighted' if pro.approach_of_KNN else 'Prababilistic')
                drawText(txt,screen,(x,y))
                txt = '[k] toggle approach'
                drawText(txt,screen,(x,y+22),20)
                if pro.approach_of_KNN == 1:
                    txt = '[v] toggle weight visualization {}'.format('(on)' if p.weightvisual else '(off)')
                    drawText(txt,screen,(x,y+40),20)
                    
                pygame.draw.rect(screen,self.clrbtncolor(),self.clrbtnrect)
                drawText('Clear*',screen,(self.clrbtnrect.center[0]-25,self.clrbtnrect.center[1]-9),25)
        
        # what are I placing with the mouse clicks?
        pos = (600,38)
        drawText("Placing:",screen,pos)
        drawText("[left mouse] to place",screen,(pos[0],pos[1]+22),20)
        drawText("[right mouse] to change",screen,(pos[0],pos[1]+40),20)
        imgOfPlacing = self.placeable[self.placing].image
        prect = imgOfPlacing.get_rect()
        screen.blit(imgOfPlacing,((pos[0]+87)-prect.center[0],(pos[1]+8)-prect.center[1]))

    def generatefood(self, amount, grid):
        """
        place a lot of food on environment grid in such a way that no more 
        than one food is placed per tile
        (better to use the new method below> 'placeObjects()'
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
        place a single object on environment grid at a specified tile if tile is empty.
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
    helper function to simplify drawing text to the screen
    """
    f = pygame.font.Font(None,size)
    t = f.render(text,1,colour)
    screen.blit(t,pos)

        