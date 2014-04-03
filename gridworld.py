'''
Created on 2014-03-28

@author: User
'''
import pygame
import math


class Block(pygame.sprite.Sprite):
    def __init__(self, size, pos, boarderColour):
        # sprite needs: init, image, rect
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect()
        # update image
        pygame.draw.rect(self.image,boarderColour,self.rect.inflate(0,0),1)
        self.rect.topleft = pos
        
    def update(self):
        # get rect at (0,0) for drawing to the block's .image
        #drawrect = pygame.Rect((0,0),self.rect.size)
        pass



class GridWorld(pygame.sprite.Sprite):
    #g_Grid = pygame.sprite.GroupSingle()
    g_Blocks = pygame.sprite.Group()

    def __init__(self, Gunit, Gwidth, Gheight):
        '''
        Constructor
        '''
        self.gunit = Gunit
        self.gwidth = Gwidth
        self.gheight = Gheight
        
        # sprite needs: init, image, rect
        super().__init__()
        self.image = pygame.Surface((int(Gunit*Gwidth)+1,int(Gunit*Gheight)+1))
        self.rect = self.image.get_rect()
        #GridWorld.g_Grid.add(self)
        
        # outside grid boarder
        boarderColour = (200,200,30)
        pygame.draw.rect(self.image,boarderColour,self.rect,1)
        
        # create blocks
        self.blockdict = {}
        for y in range(Gheight):
            for x in range(Gwidth):
                self.blockdict[(x,y)] = pygame.sprite.GroupSingle()
                self.blockdict[(x,y)].add(Block(Gunit, (x*self.gunit,y*self.gunit), boarderColour))
                GridWorld.g_Blocks.add(self.blockdict[(x,y)].sprite)
        
    def update(self):
        # update / draw blocks
        #GridWorld.g_Blocks.update()
        GridWorld.g_Blocks.draw(self.image)
        '''
        u = self.gunit
        for y in range(self.gheight):
            for x in range(self.gwidth):
                pygame.draw.rect(self.image,(200,10,10),((x*u,y*u),(u+1,u+1)),1)
        '''
        
    def kill(self):
        """
        override kill method to kill grid block sprites as well
        """
        blocks = GridWorld.g_Blocks.sprites()
        for b in blocks:
            b.kill()
        pygame.sprite.Sprite.kill(self)
        
    def getcenter(self, coord):
        return self.blockdict[coord].sprite.rect.center
    
    def convScreenToGrid(self, screenpos):
        return (screenpos[0]/self.gunit, screenpos[1]/self.gunit)
    
    def convGridToScreen(self, gridcoord):
        return (math.floor(gridcoord[0])*self.gunit, math.floor(gridcoord[1])*self.gunit)
    
    def closestGridCoord(self, gridcoord):
        x,y = gridcoord
        if x < 0:
            x = 0
        elif x >= self.gwidth:
            x = self.gwidth - 1
        if y < 0:
            y = 0
        elif y >= self.gheight:
            y = self.gheight - 1
        return (x,y)
