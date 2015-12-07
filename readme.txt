Contributors:
Touqir Sajed, Matt Jorgensen   
 

CMPUT 275 B2
Final project

COLLABORATION
We asked Michael Bowling for advice which we used on many parts of our project 
including the class inheritance structure, and the A* algorithm.
We took one suggestion from a classmate about allowing the antagonist to die in 
Survival mode.
No other collaboration outside of the group.


THE GAME
Our project in a nutshell is a grid with objects that can move around on it and 
interact in various ways. 
There are two modes to choose from which provide different objectives and options: 
Survival mode, and KNN Path finding.


- MODE 1: SURVIVAL MODE
On the grid there are green dots to represent food, pink dots for poison, and a 
blue square antagonist which will chase and hurt you. The goal is to survive by eating 
only the green food pellets and avoiding the antagonist and the poison pellets. You can 
also guide the antagonist into poison pellets as he chases you in order to kill him.

Survival Mode Controls:
- Use the arrow keys to move around.
- Click with the left mouse button to place either food, poison, or another antagonist 
on the screen. (will delete item if you click on an occupied tile)
- Click with the right mouse button to choose which to place.


- MODE 2: KNN PATH FINDING
In this mode there are only food and poison pellets on the screen with your 
protagonist. You can click anywhere on the grid and the protagonist will use various 
path finding strategies to find a path to the target. He will avoid all pellets. 
The Controls and path finding strategies are shown at the bottom of the screen.
You can, again, place objects on the screen with mouse clicks like in survival mode.


EASTER EGG
In any mode you can press 'o' to see a visualization of the odor system that we decided 
not to use. It still looks cool though!


Note from Touqir:
To understand how the weighted KNN and the probabilistic KNN works, you can go to the 
documents folder and then read through the pdf pages serially that I have scanned. I 
have also included a Comments.pdf file that explains two functions of knn file. I 
strongly recommend to go through these things before touching the "knn" code. I have 
tried to make my code well commented.
