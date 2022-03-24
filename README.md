# ordering_of_systems

This file contains the simple simulation of the behaviour of the flock of birds based on Reynolds model. 

Basis of the model is following:
1) Each bird finds its nearest neighbours;
2) Adjust the direction of motion to the average direction of neighbours
3) Birds are not computers; add some noise 

Adding a predator modifies the model:
1) Predator follows its nearest neighbour
2) All birds in some range run away from predator; their new direction is the same as the direction of the vector conecting predator to given bird
