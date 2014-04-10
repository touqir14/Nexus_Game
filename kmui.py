"""
kmui stands for [K]eyboard, [M]ouse [U]ser [I]nterface
it's for handling/redirecting events from the user
"""

from pygame.locals import *
import pygame

"""
these are the 6 available states
Ready Clicked, Down Released are unique button states for mouse buttons;
Ready Down Up are unique mouse wheel states
Ready, Hit, Down, Released are unique states for keys
"""
Ready, Hit, Clicked, Down, Released, Up = range(6)

class KMState(object):
    '''
    Basically just track the state of the mouse and keys.
    Also, I started to implement a way to handle events in this class with eHandle() method.
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
        self.v = Ready
        # add new keys as necessary
        #self. = Ready
        
        # these events can be handled by going through the set
        self.links = set()
        
    def eHandle(self):
        """
        the links list is iterated ove and each function in it is called
        """
        for insource, instate, f, vars in self.links:
            #print(insource(),instate)
            if insource() == instate:
                if vars==None:
                    f()
                #else:
                #    f(*vars)
        
    def addEvent(self, insource, instate, f, vars=None):
        """
        links is a list of tuples that hold (the input source,required state,function to call, variables)
        """
        self.links.add((insource, instate, f, vars))
    
    def updateState(self, e):
        """
        based on input from the mouse and keyboard, update the variables of this instance
        so they can be used later by any object with access to this instance
        """
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
                'print("middle")'
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
            if e.key == K_v:
                self.v = Hit
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
            if e.key == K_v:
                self.v = Released

    def refresh(self):
        """
        this method is necessary to ensure that any key is only in certain 
        states for at most one loop. to do this, please call this method at 
        the end of main loop so it can run every time and reset these variables.
        
        eg: you may need to know the moment the mouse button is pressed, but 
        you don't care anymore if it's still held down. so, when it's pressed
        it's state is changed to 'Clicked' then at the end of the main loop 
        this method will run to change it from 'Clicked' to 'Down' ensuring 
        that it was only in the 'Clicked' state for one loop.
        """
        # mouse
        if self.m_left == Clicked: self.m_left = Down
        elif self.m_left == Released: self.m_left = Ready
        if self.m_right == Clicked: self.m_right = Down
        elif self.m_right == Released: self.m_right = Ready
        self.m_wheel = Ready

        # keys
        if self.left == Hit: self.left = Down
        elif self.left == Released: self.left = Ready
        if self.right == Hit: self.right = Down
        elif self.right == Released: self.right = Ready
        if self.up == Hit: self.up = Down
        elif self.up == Released: self.up = Ready
        if self.down == Hit: self.down = Down
        elif self.down == Released: self.down = Ready
        if self.k == Hit: self.k = Down
        elif self.k == Released: self.k = Ready
        if self.v == Hit: self.v = Down
        elif self.v == Released: self.v = Ready

    def _checkkey(self, k):
        """
        ignore
        """
        if k == Hit:
            return Down
        elif k == Released:
            return Ready
        return k