# ordering_of_systems

This file contains the simple simulation of the behaviour of the flock of birds based on Reynolds model. 

Basis of the model is following:
1) Each bird finds its nearest neighbours;
2) Adjust the direction of motion to the average direction of neighbours
3) Birds are not computers; add some noise 

Adding a predator modifies the model:
1) Predator follows its nearest neighbour
2) All birds in some range run away from predator; their new direction is the same as the direction of the vector conecting predator to given bird


# ants
#------------------------------#
#--WORKS ONLY FOR PYTHON 3.10--#
#------------------------------#

Simulation of the behaviour of ants based on two agents (pheromones). Coordinates are discreete; the position of ants are integers coresponding to the indices of 2d matrix. Each ant has also an orientation (integer from 0 to 7; 0 - corresponds to up direction, 2 - to left; 4 - down; 6 - right). Ants can move only to cells pointed by (orientation - 1), orientation or (orientation + 1). Pheromones decay with time. 
When ants look for food:
1) If there is no pheromone "to food" ants move randomly
2) Ant spreads pheromone "to home" marking the way back to the nest
3) If there is "to food" pheromone ant moves in the direction of the highest abundance of pheromones
4) If ant finds food it turns back

When ants look for nest:
1) If there is no pheromone "to home" ants move randomly however the choice of direction depends on the distance to the nest (ants use enviroment to navigate to nest)
2) If there is "to home" pheromone ants follow it (the choice of the direction also depends on the distance to the nest )
3) Ants leave "to food" pheromone
4) If an ant finds nest it restores the pheromones and goes back for food

Map contains four features: grass (green), nest (yellow), obstacles (brown) and food (red). After pressing key_1 or key_2 on keyboard the distribution of pheromones is shown.

KNOWN ISSUSES:
1) Sometimes ants can be stuck
2) Ants can form loops which eventually dissolve since ants have limited amount of pheromones   
3) Dissipation of pheromones is turned off since it confuses ants 
