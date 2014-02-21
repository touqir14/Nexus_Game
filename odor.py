'''
Created on 2014-02-20

@author: User
'''
from pygame.sprite import Sprite, Group
import parameters as p
import pygame
from pygame.colordict import THECOLORS
once = 0
tid = 0
class OdorSource(Sprite):
    '''
    Special extension of Sprite that will not have a rect or an image. 
    ie. will never be drawn to the screen
    '''

    def __init__(self, type, sourceSprite, intensity=100):
        '''
        Constructor
        '''
        Sprite.__init__(self)
        p.odorSources.add(self)
        self.sourceSprite = sourceSprite    # must be a Group containing the sprite that the odor comes from
        self.type = type
        self.intensity = intensity
        
    def proliferate(self):
        """
        call this function on the update() of any object with a smell.
        """
        # if no source sprite then die
        if self.sourceSprite.sprite == None: 
            self.kill(self)
            return
        
        # find and odor of this type on the same position, or create one there
        found = False
        for i in p.odors.sprites():
            if i.type == self.type:
                if i.pos == (self.sourceSprite.sprite.pos[0],self.sourceSprite.sprite.pos[1]):
                    i.smellAmount = self.intensity
                    found = True
                    break
        if not found:
            # create new odor
            Odor(self.type, self.sourceSprite.sprite.pos, self.intensity)

    def __str__(self):
        return "type:{}".format(self.type)

'''
print(id(OdorSource("socks")))
print(id(OdorSource("watermelon")))
print(OdorSource("orange"))
print(OdorSource("dirt"))
print(OdorSource("watermelon"))
'''

class Odor(Sprite):
    def __init__(self, otype, pos, smellAmount):
        # required by Sprite
        Sprite.__init__(self)
        self.image = pygame.Surface((1,1))
        self.image.fill(THECOLORS['yellow'])
        self.rect = self.image.get_rect()
        self.add(p.allObjects, p.odors)
        self.pos = (int(pos[0]), int(pos[1]))   # pos must be an int for the odors since they are positioned one per pixel
        self.rect.center = self.pos
        self.type = otype
        self.smellAmount = smellAmount
        self.surroundingOdors = Group()
        # check if you have neighbours
        for i in p.odors.sprites():
            if i.type == self.type:
                if (i.pos[0] >= self.pos[0]-1 and i.pos[0] <= self.pos[0]+1) and (i.pos[1] >= self.pos[1]-1 and i.pos[1] <= self.pos[1]+1):
                    self.surroundingOdors.add(i)
                    i.surroundingOdors.add(self)
        
    def update(self):
        # proliferate smell to surrounding Odors
        if len(self.surroundingOdors.sprites()) >= 8:
            return
        self.smellAmount -= 0#int(self.smellAmount/2)
        if self.smellAmount > 0:
            #for i in self.surroundingOdors.sprites():
            #    i.smellAmount += self.smellAmount-1
            
            found = [False for i in range(9)]
            found[4] = True     # this is where self is sitting
            addAmount = self.smellAmount-1
            global once, tid
            if once == 0: 
                tid = id(self)
                once +=1
            if True:
                once +=1
                for i in self.surroundingOdors.sprites()[:]:
                    j = ((i.pos[0]-self.pos[0]+1)+int((i.pos[1]-self.pos[1]+1)*3))
                    found[j] = True
                    i.smellAmount += addAmount
                    print("pos: j{} i{} {}".format(j, i.pos, self.pos))
                    '''
                    if i.pos == (self.pos[0]-1,self.pos[1]-1):
                        found[0] = True
                        i.smellAmount += addAmount
                    elif i.pos == (self.pos[0],self.pos[1]-1):
                        found[1] = True
                        print("True")
                        i.smellAmount += addAmount
                    elif i.pos == (self.pos[0]+1,self.pos[1]-1):
                        found[2] = True
                        i.smellAmount += addAmount
                    elif i.pos == (self.pos[0]-1,self.pos[1]):
                        found[3] = True
                        i.smellAmount += addAmount
                    elif i.pos == (self.pos[0]+1,self.pos[1]):
                        found[5] = True
                        i.smellAmount += addAmount
                    elif i.pos == (self.pos[0]-1,self.pos[1]+1):
                        found[6] = True
                        i.smellAmount += addAmount
                    elif i.pos == (self.pos[0],self.pos[1]+1):
                        found[7] = True
                        i.smellAmount += addAmount
                    elif i.pos == (self.pos[0]+1,self.pos[1]+1):
                        found[8] = True
                        i.smellAmount += addAmount
                    '''

                print("actual pos {}".format(self.pos))
                for i in range(9):
                    if found[i] == False:
                        # create new odor
                        newpos = (self.pos[0]+(i%3-1),self.pos[1]+(int(i/3)-1))
                        print("{}: found[{}]:{} newpos:{} {} {}".format(id(self),i,found[i],newpos,(i%3-1),(int(i/3)-1)))
                        Odor(self.type, newpos, addAmount)
        else:
            self.kill(self)
