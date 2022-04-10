import pygame
import numpy as np

import ants_properties as ap



WIDTH, HEIGHT = 500, 500                  # size of the window
CELL_WIDTH, CELL_HEIGHT = 10, 10          # size of one grid cell of a map


# some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN =(69,120,0)
RED = (255, 0, 0)
BORDER_COLOR = (138,54,15)
NEST_COLOR = (255,185,15)
FOOD_COLOR = (255,48,48)



ANT_SIZE = (20, 20)      # size of the ants
NUMBER_OF_ANTS = 100     # number of the ants
FPS = 20               # frames per second


WIN=pygame.display.set_mode((WIDTH, HEIGHT))        # set display window

# -------- map creation -------
MAP_SIZE = 50                                 #size of the map

MAP=np.zeros(( MAP_SIZE, MAP_SIZE ))   #generate map

PHEROMONE = np.zeros((MAP_SIZE, MAP_SIZE, 2))  #pheromone array, for each index x, y one has two values of two types of pheromones

PHEROMONE_QUANTITY = 5                # amount of pheromone droped by ants
SPREADING_COEFFICIENT = 0.           # how much pheromone will be drop to neighbouring cells
DECAY_CONSTANT_0 = 0.0005              # how fast first pheromone vanishes 0 - never; 1 - instantaneously 
DECAY_CONSTANT_1 = 0.0005              # how fast second pheromone vanishes 0 - never; 1 - instantaneously 


MAP[:,0]=-1                         # boundary conditions; at the end of map there are obstacles 
MAP[:,MAP_SIZE-1]=-1
MAP[0,:]=-1
MAP[MAP_SIZE-1,:]=-1


#--------------------- nest and big food source

start = [10, 10] #nest position

# MAP[start[0],start[1]]=2    # we use numberr 2 to mark nest


# for i in range(40, 48):
#     for j in range(5,48):
#         MAP[i][j]=1   


# --------------------- nest between food -------

# start = [MAP_SIZE//2,MAP_SIZE//2] #nest is in the middle

# MAP[start[0],start[1]]=2    # we use numberr 2 to mark nest

# for i in range(10,30):
#     for j in range(2,10):
#         MAP[i][j]=1

# for i in range(20, 40):
#     for j in range(41,49):
#         MAP[i][j]=1   

#--------------------- nest in the middle and four sources of food -------

start = [MAP_SIZE//2,MAP_SIZE//2] #nest is in the middle

MAP[start[0],start[1]]=2    # we use numberr 2 to mark nest

for i in range(2,10):
    for j in range(2,10):
        MAP[i][j]=1

for i in range(40, 48):
    for j in range(41, 49):
        MAP[i][j]=1   

for i in range(2,10):
    for j in range(41, 49):
        MAP[i][j]=1

for i in range(40, 48):
    for j in range(2, 10):
        MAP[i][j]=1

#-------------------------------


#  images of ants
ANT_FINDER = pygame.transform.scale(pygame.image.load("ant_seeker.png"), ANT_SIZE)       
ANT_RETURNER = pygame.transform.scale(pygame.image.load("ant_returner.png"), ANT_SIZE)


def draw_map(PHEROMONE_CONTROL):
    # draw map
    for row in range(MAP_SIZE):
        for column in range(MAP_SIZE):
            # draw food, nest, boundaries
            color = GREEN

            if MAP[row][column] == -1:  
                color = BORDER_COLOR
            elif MAP[row][column] == 1:
                color = FOOD_COLOR
            elif MAP[row][column] == 2:
                color = NEST_COLOR
            else:
                color = GREEN

            pygame.draw.rect(WIN, tuple(color), [ CELL_WIDTH * column, CELL_HEIGHT * row, CELL_WIDTH, CELL_HEIGHT])


            # check if keyboards 1 or 2 are pressed and if true draw corresponding 'heat map' of the given type of pheromone

            if int(PHEROMONE_CONTROL)  > -1 and PHEROMONE[row][column][int(PHEROMONE_CONTROL)]>= 1: #ants detect pheromone if pheromone bigger than 1
                if PHEROMONE[row][column][int(PHEROMONE_CONTROL)] > 0 and 10*PHEROMONE[row][column][int(PHEROMONE_CONTROL)]< 200:  #multiply by 10 for better display

                    color = [0, 0, 50 + 10*PHEROMONE[row][column][int(PHEROMONE_CONTROL)]]
                    pygame.draw.rect(WIN, tuple(color), [ CELL_WIDTH * column, CELL_HEIGHT * row, CELL_WIDTH, CELL_HEIGHT])

                elif PHEROMONE[row][column][int(PHEROMONE_CONTROL)] > 0 and 10*PHEROMONE[row][column][int(PHEROMONE_CONTROL)]>= 200: #if there is too much pheromone fill with (0,0,255)

                    color = [0, 0, 255]
                    pygame.draw.rect(WIN, tuple(color), [ CELL_WIDTH * column, CELL_HEIGHT * row, CELL_WIDTH, CELL_HEIGHT])
    
def draw_window(ants):
    global PHEROMONE
    # draw all ants
    for obj in ants:
        
        if obj.task == 0:   # ant looks for food

            if obj.PHEROMONE_1 > (PHEROMONE_QUANTITY + 3* PHEROMONE_QUANTITY * SPREADING_COEFFICIENT):  # if ant has enough of second type of pheromone, it spreads the pheromone
                ap.spread_pheromone(obj.X, obj.Y, obj.orientation, MAP, PHEROMONE, 1, SPREADING_COEFFICIENT, PHEROMONE_QUANTITY)
                obj.PHEROMONE_1 -= (PHEROMONE_QUANTITY + 3* PHEROMONE_QUANTITY * SPREADING_COEFFICIENT) # ants have finite amount of pheromones
            
            if MAP[obj.X, obj.Y] == 0:
                # if ant is on the grass then first check if in the foward cells there is food, nest or border    
                if obj.check(1, MAP):
                    obj.detect(1, MAP)

                elif obj.check(2, MAP):
                    
                    obj.detect(2, MAP)
                
                elif obj.check(-1, MAP):
                   
                    obj.antidetect(-1, MAP, PHEROMONE)
                
                else:    # go where pheromone level is the highest
                    obj.pheromone_detect(MAP, PHEROMONE)          

      

            elif MAP[obj.X, obj.Y] == 1: #if ant found food:
            
                MAP[obj.X, obj.Y] = 0    # deplete food from the map
                obj.task = 1             # change task to finding home
                obj.image = ANT_RETURNER # change image
                obj.orientation = (obj.orientation - 4) % 8  #go back
               

            elif MAP[obj.X, obj.Y] == 2:
                #ant failed to find food
                obj.orientation = np.random.randint(0,8) #select new direction
                obj.PHEROMONE_0 = 1000 # restore pheromones
                obj.PHEROMONE_1 = 1000 # restore pheromones
            else:      #just in case;
                print("---", MAP[obj.X, obj.Y],)
                obj.pheromone_detect(MAP, PHEROMONE)
        else:  #ant looks for nest

            #spread pheromone for ants which look for food
            if obj.PHEROMONE_0 > (PHEROMONE_QUANTITY + 3* PHEROMONE_QUANTITY * SPREADING_COEFFICIENT):
                    ap.spread_pheromone(obj.X, obj.Y, obj.orientation, MAP, PHEROMONE, 0, SPREADING_COEFFICIENT,  PHEROMONE_QUANTITY)
                    obj.PHEROMONE_0 -= (PHEROMONE_QUANTITY + 3* PHEROMONE_QUANTITY * SPREADING_COEFFICIENT)

            if MAP[obj.X, obj.Y] == 2:  #  ant found nest
                obj.task = 0            # change task to finding food
                obj.image = ANT_FINDER  # change image
                obj.orientation = (obj.orientation - 4) % 8 # go back

                obj.PHEROMONE_0 = 1000  # restore pheromones
                obj.PHEROMONE_1 = 1000  # restore pheromones

            elif MAP[obj.X, obj.Y] == 0: # if ant did not find a nest
                if obj.check(2, MAP):    # check for nest
                    obj.detect(2, MAP)   # go to nest
                   
                elif obj.check(-1, MAP): #check for obstacles
                    obj.antidetect(-1, MAP, PHEROMONE) # go in different direction 

                elif obj.check(1, MAP):  # check for food
                    obj.antidetect(1, MAP, PHEROMONE)  #go in different direction
                
              
                else:  #just in case  
                    obj.pheromone_detect(MAP, PHEROMONE)
            else:  #if ant looking for nest is at the square with food; should not happen; may cause tunneling of ants through food
                obj.pheromone_detect(MAP, PHEROMONE)
                # obj.antidetect(1, MAP, PHEROMONE)
                if obj.check(-1, MAP): #check for obstacles
                    obj.antidetect(-1, MAP, PHEROMONE) # go in different direction 
                # obj.orientation = (obj.orientation - 4) % 8 # go back
        
        obj.movement(obj.orientation, MAP)         # update the position of ant
        
        
        PHEROMONE = ap.pheromone_decay(PHEROMONE, DECAY_CONSTANT_0, DECAY_CONSTANT_1) # update pheromones distribution due to their decay
        
        #draw image of ant
        WIN.blit(pygame.transform.rotate(obj.image, obj.orientation*45), (CELL_HEIGHT * obj.Y - 4/5 * (CELL_HEIGHT), CELL_WIDTH * obj.X - 4/5 * (CELL_WIDTH)  ))
    
    
    pygame.display.update() # display MAP and ants


def main():
    clock = pygame.time.Clock( )
    run = True


    #generate ants
    ants = []
    for i in range(NUMBER_OF_ANTS):
        
        ants.append( ap.ant(start[0], start[1], i%8, ANT_FINDER ) )

    
    ants = np.array(ants)
 
    # at first there are no pheromones 
    PHEROMONE_CONTROL = -1
    draw_map(PHEROMONE_CONTROL)


    while run:
        clock.tick(FPS)        # get constant number of FPS

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:   #quit button
                run = False

            keys_pressed = pygame.key.get_pressed()     # find pressed keys

            if keys_pressed[pygame.K_1]: # if key 1 is pressed
                PHEROMONE_CONTROL = 0
            elif keys_pressed[pygame.K_2]: # if key 2 is pressed 
                PHEROMONE_CONTROL = 1
            else:
                PHEROMONE_CONTROL = -1

        draw_map(PHEROMONE_CONTROL)

        draw_window(ants)
        

    pygame.quit()
        

if __name__=="__main__":
    main()
