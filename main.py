import pygame
import math

from queue import PriorityQueue

#width of the pygame window
WIDTH = 600
ROWS = 40   #the grid will be ROWS * ROWS, change this for differnt size grid

WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* algorithm")

#colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#each spot on the grid
class Spot:
    def __init__(self,row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE
    
    def make_path(self):
        self.color = PURPLE

    def make_end(self):
        self.color = TURQUOISE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):   #update neighbors of the current node
        self.neighbors = []
        #down
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])
        #up
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])
        #left
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])
        #right
        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])
        

    def __lt__(self, other):    #less than
        return False

def algorithm(draw, grid, start, end):  # A* algorithm logic
    count =0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) #initially add the start node
    #the open set looks like ( ( 0, 0, node ) )

    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}  #g score of all nodes is infinity initially
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}  #g score of all nodes is infinity initially
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start} 
    #since we don't have any method to check if an item exists in a priority queue hence we are using a
    #dictionary, which keeps track of all the nodes in open set right now.'''

    while not open_set.empty(): #loop runs till there is an item in open set.
        
        for event in pygame.event.get():    #get the events 
            if event.type == pygame.QUIT:
                pygame.quit()               #quit the window
            
        current = open_set.get()[2]         #get the current node which is at index 2
        open_set_hash.remove(current)       #remove this from open set

        if current==end:                    #if end is reached i.e path is found
            reconstruct_path(came_from, end, draw)      #draw the path
            end.make_end()
            return True
        
        for neighbor in current.neighbors:   #if this node is not end, keep looking
            
            temp_g_score = g_score[current] + 1     #the weight of each node is 1

            if temp_g_score < g_score[neighbor]:    #if the current path is less costly than the present path
                came_from[neighbor] = current       #update the g score and f score
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:   # if neighbor node not in open set we explore this path
                    count+=1
                    open_set.put((f_score[neighbor], count, neighbor))  #add the node to the open set
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()  #draw the current grid

        if current!=start:
            current.make_closed()
    return False

def reconstruct_path(came_from, current, draw): #draw the final path from start to end node
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def h(p1, p2):          # return the euclidean distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def make_grid(rows, width):     #make the grid initially
    grid=[]                     #holds all of the nodes of the graph
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)    #creating node from the Spot class
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):    #draw the grid lines
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0,i*gap), (width, i*gap))  #go from left to the right horizontally
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap,0), (j*gap, width))  #go from the top to bottom vertically

def draw(win, grid, rows, width):   #draw the grid
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, rows, width)     #draw grid lines
    pygame.display.update()

def get_clicked_pos(pos, rows, width):  #from the coordinates get the row and col
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row,col

def main(win, width):   #main
    grid = make_grid(ROWS, width)
    start = None
    end = None

    run = True

    while(run):
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if pygame.mouse.get_pressed()[0]:   #if left mouse pressed
                pos = pygame.mouse.get_pos()    #get position
                row, col = get_clicked_pos(pos, ROWS, width)    #get row, col from screen coordinates
                spot = grid[row][col]   #get the clicked node in the grid
                
                if not start and spot !=end:    #if start node is not selected
                    start = spot
                    start.make_start()
                
                elif not end and spot!=start:   #if end node is not selected
                    end = spot
                    end.make_end()
                
                elif spot!= end and spot!=start:    #make walls
                    spot.make_barrier()

            #right click removes the  already clicked node.
            elif pygame.mouse.get_pressed()[2]: #right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()            #remove the spot

                if spot==start:         #if clicked spot is start node
                    start = None
                elif spot==end:         #if clicked spot is end node
                    end = None
            if event.type == pygame.KEYDOWN:    #if a key is pressed
                if event.key == pygame.K_SPACE and start and end:   #if space key is pressed
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid) #update neighbors for each node
                    algorithm(lambda: draw(win,grid, ROWS, width), grid, start, end) #run the algorithm
                
                if event.key == pygame.K_c:     #press c key to clear the window
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    
    pygame.quit()

main(WIN, WIDTH)    #calling the program



    
    

    
        


