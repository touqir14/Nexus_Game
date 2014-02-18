AI simmulation.
Grid based environment with food items.
Protagonist must survive by finding food and avoiding antagonist.
Antagonist must survive by finding protagonist.

Protagonist will be given a certain amount of time in between moves(time steps) to simulate for itself what would happen if it took various paths. This is its ability to plan for the future. It will choose the best option out of the paths that it has thought through.

1 Time step
2 Health level
3 Box position and number
4 Odor intensity
5 Health value of food
6 Speed of agents (dependant on health and exhaustion)
7 Exhaustion level
8 History

History will be a list of lists. Each sub-list will contain all the information that the protaganist has seen for one time step:
- time step
- box x, y coordinates / number
- list of odor levels in that box
- 


Each object has a unique ID
Each object gets an odor
Each odor type has a unique ID but more than one object can have the same odor type

hello