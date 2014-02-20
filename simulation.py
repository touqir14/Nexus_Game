'''
Created on 2014-02-19

@author: User
'''
from basicFood import BasicFood
import parameters as p
from protagonist import Protagonist

class Simulation():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # zero time step
        p.timeStep = 0
        
        # create protagonist
        p.protagonist.add(Protagonist())
        
        # create food items
        for i in range(p.startingFood):
            BasicFood((p.rand.randint(int(p.basicFoodDiameter/2), p.env_size[0]-int(p.basicFoodDiameter/2)),
                       p.rand.randint(int(p.basicFoodDiameter/2), p.env_size[1]-int(p.basicFoodDiameter/2))))
            #to do: retry if food is close to previous food or object?

        # create antagonist

    def run(self, env_screen):
        
        # increment time step
        p.timeStep += 1
    
    