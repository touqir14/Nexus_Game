import pygame
import math
import kmui


class Block(pygame.sprite.Sprite):
    def __init__(self, size, pos, boarderColour):
        # sprite needs: init, image, rect
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect()
        # update image
        self.boarderColour = boarderColour
        pygame.draw.rect(self.image,boarderColour,self.rect.inflate(0,0),1)
        self.rect.topleft = pos
        
        self._bgc = (20,20,20)
        self.other = False
        highlight = 50
        self.bgc = [self._bgc,(self._bgc[0]+highlight,self._bgc[1]+highlight,self._bgc[2]+highlight),(0,0,0)]
        
    def update(self, mpos):
        # get rect at (0,0) for drawing to the block's .image
        #drawrect = pygame.Rect((0,0),self.rect.size)
        zerorect = pygame.Rect((0,0),self.rect.size)
        self.image.fill(self.bgc[self.rect.collidepoint(mpos) if not self.other else 2])
        pygame.draw.rect(self.image,self.boarderColour,zerorect.inflate(0,0),1)

def floorCoord(coordfunc):
    """
    to be used as a wrapper.
    *** anytime the grid's dict needs to be accessed ***
    since screen objects can store their coordinates as float due to
    differences in movement speed, this wrapper will make sure that
    any function that takes coords will receive the INT coords.
    lambda(self,coord):...
    """
    return lambda s,co: coordfunc(s,(math.floor(co[0]),math.floor(co[1])))

class GridWorld(pygame.sprite.Sprite):
    #g_Grid = pygame.sprite.GroupSingle()
    g_Blocks = pygame.sprite.Group()

    def __init__(self, env_rect, Gunit, Gwidth, Gheight, km_state):
        '''
        Create a new grid where Gunit is the width and height of each tile ie. the unit size,
        Gwidth and G height are the number of tiles across and dorwn respectively.
        '''
        self.gunit = Gunit
        self.width = Gwidth
        self.height = Gheight
        
        # sprite needs: init, image, rect
        super().__init__()
        self.image = pygame.Surface((int(Gunit*Gwidth)+1,int(Gunit*Gheight)+1))
        self.rect = self.image.get_rect()
        #GridWorld.g_Grid.add(self)
        
        # outside grid boarder
        boarderColour = (50,50,30)
        pygame.draw.rect(self.image,boarderColour,self.rect,1)
        
        # clear old blocks (do this somewhere else please)
        for b in GridWorld.g_Blocks.sprites():
            b.kill()
        
        # create blocks
        self.value_dict = {}
        self.blockdict = {}
        self.itemsdict = {}
        for y in range(self.height):
            for x in range(self.width):
                self.value_dict[(x,y)] = []
                self.itemsdict[(x,y)] = pygame.sprite.Group()
                self.blockdict[(x,y)] = pygame.sprite.GroupSingle()
                self.blockdict[(x,y)].add(Block(Gunit, (x*self.gunit,y*self.gunit), boarderColour))
                GridWorld.g_Blocks.add(self.blockdict[(x,y)].sprite)
        
        GridWorld.g_Blocks.draw(self.image)

        # move rects by offset amount (grid is centered on screen)
        xoffset = (env_rect.width - self.rect.width)//2
        yoffset = (env_rect.height - self.rect.height)//2
        #self.rect.topleft = (xoffset, yoffset)
        #for s in GridWorld.g_Blocks.sprites():
        #    s.rect.left += xoffset
        #    s.rect.bottom += yoffset
    
    @floorCoord
    def istile(self, coord):
        """
        check if tile exists.
        """
        return coord in self.itemsdict.keys()
    
    def emptytiles(self):
        """
        return a list of the tiles that have nothing on them
        """
        return [k for k,v in self.itemsdict.items() if len(v.sprites()) == 0]
        
    def update(self, mpos):
        # update / draw blocks
        GridWorld.g_Blocks.update(mpos)
        GridWorld.g_Blocks.draw(self.image)
        '''
        u = self.gunit
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(self.image,(200,10,10),((x*u,y*u),(u+1,u+1)),1)
        '''
    
    def trackObj(self, env_obj, coord):
        """
        remember that there is an object at this position so other objects can query the grid
        """
        self.itemsdict[coord].add(env_obj)
        
    def getItemAt(self, coord):
        tilegroup = self.itemsdict.get(coord)
        if tilegroup and len(tilegroup) > 0:
            return tilegroup.sprites()[0]
        return None            
        
    def removeItemAt(self, item, coord):
        tilegroup = self.itemsdict.get(coord)
        if tilegroup and len(tilegroup) > 0:
            if tilegroup.has(item):
                # kill from all groups
                item.kill()
                # also remove from toquir's knn value dict
                if item.value in self.value_dict[coord]:
                    self.value_dict[coord].remove(item.value)
        
    def kill(self):
        """
        override kill method to kill grid block sprites as well
        """
        blocks = list(GridWorld.g_Blocks.sprites())
        for b in blocks:
            b.kill()
        super().kill()
        
    @floorCoord
    def getcenter(self, coord):
        """
        return the x,y position of the center of the tile at 'coord'
        return None if not a tile (can be used for edge of world 
        detection but there's a better way to do that)
        """
        #floorcoord = (math.floor(coord[0]),math.floor(coord[1]))
        if self.istile(coord):
            return self.blockdict[coord].sprite.rect.center
        return None
    
    def convPosToCoord(self, screenpos):
        return (math.floor(screenpos[0]/self.gunit), math.floor(screenpos[1]/self.gunit))
    
    @floorCoord
    def convCoordToPos(self, gridcoord):
        return (math.floor(gridcoord[0])*self.gunit, math.floor(gridcoord[1])*self.gunit)
    
    def closestGridCoord(self, gridcoord):
        x,y = gridcoord
        if x < 0:
            x = 0
        elif x >= self.width:
            x = self.width - 1
        if y < 0:
            y = 0
        elif y >= self.height:
            y = self.height - 1
        return (x,y)
    
    def edgecondition(self, coord):
        """
        game objects moving around on the screen can use this function to 
        make sure they stay on the grid. 
        - takes a grid coordinate to check
        - returns a valid coordinate (possibly the same)
        """
        return self.closestGridCoord(coord)
