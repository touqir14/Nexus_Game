"""
kmui = keyboard, mouse user interface
it's for handling/redirecting events from the user
"""

from pygame.locals import *
import pygame

# Ready Clicked, Down Released are unique button states for mouse buttons;
# Ready Down Up are unique mouse wheel states
# Ready, Hit, Down, Released are unique states for keys
Ready, Hit, Clicked, Down, Released, Up = range(6)

class KMState(object):
    '''
    Basically just track the state of the mouse
    '''

    def __init__(self):
        # mouse
        self.mpos = (0,0)
        self.m_left = Ready       # Ready, Clicked, Down, Released
        self.m_right = Ready      # Ready, Clicked, Down, Released
        self.m_wheel = Ready      # Ready, Down, Up
        
        # keys
        self.left = Ready           # Ready, Hit, Down, Released
        self.right = Ready
        self.up = Ready
        self.down = Ready
        self.k = Ready
        #self. = Ready
        
    def updateState(self, e):
        if e.type == MOUSEMOTION:
            self.mpos = pygame.mouse.get_pos()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                #print("left")
                self.m_left = Clicked
            elif e.button == 3:
                #print("right")
                self.m_right = Clicked
            elif e.button == 2:
                print("middle")
            elif e.button == 4:
                #print("up")
                self.m_wheel = Up
            elif e.button == 5:
                #print("down")
                self.m_wheel = Down
        elif e.type == MOUSEBUTTONUP:
            # left
            if e.button == 1:
                self.m_left = Released
            # right
            elif e.button == 3:
                self.m_right = Released
                
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                self.up = Hit
            if e.key == K_DOWN:
                self.down = Hit
            if e.key == K_LEFT:
                self.left = Hit
            if e.key == K_RIGHT:
                self.right = Hit
            if e.key == K_k:
                self.k = Hit
        elif e.type == KEYUP:
            if e.key == K_UP:
                self.up = Released
            if e.key == K_DOWN:
                self.down = Released
            if e.key == K_LEFT:
                self.left = Released
            if e.key == K_RIGHT:
                self.right = Released
            if e.key == K_k:
                self.k = Released

    
    def refresh(self):
        # mouse
        if self.m_left == Clicked: self.m_left = Down
        if self.m_right == Clicked: self.m_right = Down
        if self.m_left == Released: self.m_left = Ready
        if self.m_right == Released: self.m_right = Ready
        self.m_wheel = Ready

        # keys
#        keys = (self.left, self.right, self.down, self.up)
#        for k in keys:
#            k = self._checkkey(k)
#        self.left = self.checkkey(self.left)
        if self.left == Hit: self.left = Down
        if self.left == Released: self.left = Ready
        if self.right == Hit: self.right = Down
        if self.right == Released: self.right = Ready
        if self.up == Hit: self.up = Down
        if self.up == Released: self.up = Ready
        if self.down == Hit: self.down = Down
        if self.down == Released: self.down = Ready
        if self.k == Hit: self.k = Down
        if self.k == Released: self.k = Ready

    def _checkkey(self, k):
        if k == Hit:
            return Down
        elif k == Released:
            return Ready
        return k