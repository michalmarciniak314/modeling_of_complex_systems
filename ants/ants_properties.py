# from tabnanny import check
import numpy as np

from ants_simulation import PHEROMONE

class ant:
    def __init__(self, X, Y, orientation, image, task = 0):
        self.X = X           
        self.Y = Y            
        self.orientation = orientation #direction of motion; 0 = up; 2 = left; 4 = down; 6 = right
        self.task = task   #0 = searchiing _______ 1= returning 
        self.PHEROMONE_0 = 1000        #initial pheromones on ant
        self.PHEROMONE_1 = 1000        #initial pheromones on ant
        self.image = image
        self.home = (X, Y)

    def movement(self, orientation, MAP ):  #make a move according to orientation

        match orientation:
            case 0:
                
                self.X = self.X - 1

            case 1: 
                
                self.X = self.X - 1
                self.Y = self.Y - 1

            case 2:
                
                self.Y = self.Y - 1
                
            case 3:
               
                self.X = self.X + 1
                self.Y = self.Y - 1
    
            case 4:
           
                self.X = self.X + 1
            
            case 5:
       
                self.X = self.X + 1
                self.Y = self.Y + 1
        
            case 6:
           
                self.Y = self.Y + 1
            
            case 7:
 
                self.X = self.X - 1
                self.Y = self.Y + 1
    
    def pheromone_detect(self, MAP, PHEROMONE):  #detect pheromones
        
        A0 = [ check_move(self.X, self.Y, (self.orientation - 1 + i)%8, MAP)   for i in range(3)] #get an array of possible new coordinates
        
        A = np.array( [ PHEROMONE[x,  y][self.task]   for x, y in A0] )   # get pheromones of type self.task on the map at those positions

        dist = np.array( [ (self.home[0]-x)**2+(self.home[1]-y)**2   for x, y in A0] )   # get find distances to nest
        # dist = np.where(dist == 0, 0.01, dist)

        # print(dist, self.X, self.Y, self.check(2, MAP), MAP[check_move(self.X, self.Y, self.orientation - 1, MAP)]==2 , MAP[check_move(self.X, self.Y, ( self.orientation )%8, MAP )]==2, MAP[check_move(self.X, self.Y, (self.orientation + 1%8), MAP)]==2)
        # print(A0, self.orientation)
        # print(check_move(self.X, self.Y, (self.orientation - 1)%8, MAP) , check_move(self.X, self.Y, ( self.orientation )%8, MAP ), check_move(self.X, self.Y, (self.orientation + 1)%8, MAP))
        if max(A) >= 1 : # if ant detects pheromones go in the direction of the largest concentration 
            if self.task == 0:
                A = np.where(A == A[np.argmax(A)], 1, 0) 
            else: 
                A = np.where(A >= 1 , A, 0)/dist**2 
                A = np.where(A == A[np.argmax(A)], 1, 0)/dist**2 
                # print(A)
        else: 
            if self.task == 0:
                A = np.ones(3) # if there are no pheromones go in the random direction
                
            else:
                A = np.ones(3)/dist**2 

        A = A/np.sum(A)     #make probabilities 
        C = np.arange(3)    
        
        self.orientation = ( self.orientation - 1 + np.random.choice(C, p = A) )%8 #update direction
    

    def antidetect(self, GOAL, MAP, PHEROMONE):   # go in the direction where there is no GOAL

        A0 = [ check_move(self.X, self.Y, (self.orientation - 1 + i)%8, MAP)   for i in range(3)] #get an array of possible new coordinates
        
        A = np.array([MAP[x, y] for x, y in A0])                                                  # get objects on the map at those positions
        
        B = np.array([PHEROMONE[x, y][0] for x, y in A0])                                         # get pheromones on map at those positions
        
        
        if sum(A) == 3*GOAL:                                                                           # if only possible moves are to GOAL then turn back
            self.orientation = ( self.orientation - 4) % 8
            

        else:

            A = np.where(A == GOAL, 0, 1)                                                         #exchange 1<->0
            
            if all(A * B) != 0:                                                                    # if there are pheromones follow them if not go in random direction where ther is no GOAL
                A = A * B
            
            A = A/np.sum(A)                                                                       # get probabilities

            B = np.arange(3)
            self.orientation = ( self.orientation - 1 + np.random.choice(B, p = A)) % 8           # update orientation
            

    def detect(self, GOAL, MAP): #detect GOAL = nest or food 

        A0 = [ check_move(self.X, self.Y, (self.orientation - 1 + i)%8, MAP)   for i in range(3)]   #get an array of possible new coordinates
        A = np.array([MAP[x, y] for x, y in A0])                                                    # objects on map at those positions

        # if ant can reach GOAL in the next step go there with corresponding probabilities;
        A = np.where(A == GOAL, 1, 0) 
        A = A/np.sum(A)
        B = np.arange(3)
        self.orientation = ( self.orientation - 1 + np.random.choice(B, p = A)) % 8
    
    def check(self, GOAL, MAP):
        # check if in the foward cells is TYPE = food, nest, border
        if MAP[check_move(self.X, self.Y, (self.orientation - 1)%8, MAP)]==GOAL or MAP[check_move(self.X, self.Y, ( self.orientation )%8, MAP )]==GOAL or MAP[check_move(self.X, self.Y, (self.orientation + 1)%8, MAP)]==GOAL:
            return True
        else:
            return False

        
def spread_pheromone(X, Y, orientation, MAP, PHEROMONE, TYPE, SPREADING_COEFFICIENT, PHEROMONE_QUANTITY ):
    
    PHEROMONE[X, Y][TYPE] += PHEROMONE_QUANTITY      # at current position leave basic amount of pheromone
    
    #leave behind smaller amount of pheromone 
    if MAP[check_move(X, Y, (orientation-4-1)%8 ,MAP)] == 0: PHEROMONE[check_move(X, Y, (orientation-4-1)%8 ,MAP)][TYPE] += SPREADING_COEFFICIENT * PHEROMONE_QUANTITY
    if MAP[check_move(X, Y, (orientation-4)%8 ,MAP)] == 0: PHEROMONE[check_move(X, Y, (orientation-4)%8 ,MAP)][TYPE] += SPREADING_COEFFICIENT * PHEROMONE_QUANTITY
    if MAP[check_move(X, Y, (orientation-4+1)%8 ,MAP)] == 0: PHEROMONE[check_move(X, Y, (orientation-4+1)%8 ,MAP)][TYPE] += SPREADING_COEFFICIENT * PHEROMONE_QUANTITY
    

def check_move(X, Y, orientation, MAP ):    #do a 'trial' step; similar to ant.movement();     
    match orientation:
        case 0:
            X = X - 1

        case 1: 
            X = X - 1
            Y = Y - 1

        case 2:
            Y = Y - 1
            
        case 3:
            X = X + 1
            Y = Y - 1
    
        case 4:
            X = X + 1
        
        case 5:
            X = X + 1
            Y = Y + 1

        case 6:
            Y = Y + 1
        
        case 7:
            X = X - 1
            Y = Y + 1

    return X, Y

def pheromone_decay(PHEROMONE,  DECAY_CONSTANT_0, DECAY_CONSTANT_1):  # the decay function
    return PHEROMONE * np.array([(1- DECAY_CONSTANT_0), (1-DECAY_CONSTANT_1)])
