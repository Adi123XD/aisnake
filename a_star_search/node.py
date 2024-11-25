import pygame
import math
from queue import PriorityQueue
from a_star_constants import *

win = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Search Algorithm")



class Spot:
    def __init__(self, row, col, width, total_rows ):
        self.row = row 
        self.col= col
        self.color = WHITE
        self.x = col * width
        self.y = row * width
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        
    def get_pos(self):
        return self.row, self.col
    def is_closed(self):
        return self.color ==RED
    
    def is_open (self):
        return self.color==GREEN
    def is_barrier(self):
        return self.color==BLACK
    def is_start(self):
        return self.color==ORANGE
    def is_end(self):
        return self.color==TURQUOISE
    
    def reset(self):
        self.color=WHITE
    def make_start(self):
        self.color=ORANGE  
    def make_open(self):
        self.color=GREEN
    def make_barrier(self):
        self.color=BLACK
    def make_end(self):
        self.color=TURQUOISE
    def make_path(self):
        self.color = PURPLE
    def make_closed(self):
        self.color=RED
        
    def draw(self,win):
        pygame.draw.rect(win, self.color,(self.x, self.y , self.width,self.width))
    def update_neighbors(self,grid):
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row-1][self.col])
            
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier(): #DOWN
            self.neighbors.append(grid[self.row+1][self.col])
            
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col-1])
            
        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col+1])
    def update_neighbors_snakegame(self, grid, snake_body):
        self.neighbors = []  # Reset neighbors to avoid duplication
        
        # Check UP
        if self.row > 0:
            neighbor = grid[self.row - 1][self.col]
            if neighbor not in snake_body:  # Exclude snake body as barriers
                self.neighbors.append(neighbor)

        # Check DOWN
        if self.row < self.total_rows - 1:
            neighbor = grid[self.row + 1][self.col]
            if neighbor not in snake_body:
                self.neighbors.append(neighbor)

        # Check LEFT
        if self.col > 0:
            neighbor = grid[self.row][self.col - 1]
            if neighbor not in snake_body:
                self.neighbors.append(neighbor)

        # Check RIGHT
        if self.col < self.total_rows - 1:
            neighbor = grid[self.row][self.col + 1]
            if neighbor not in snake_body:
                self.neighbors.append(neighbor)
            
    def __lt__(self, other):
        return False
    
def h(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)

def make_grid(rows, width):
    grid=[]
    gap = width//rows
    # here rows and cols will be the same as i am planning to make a square shaped window 
    for i in range(rows ):
        grid.append([])
        for j in range(rows) :
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRAY, (j * gap, 0), (j * gap, width))

def draw(win, rows, grid, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()
    
def get_clicked_pos(pos, rows,width):
    gap = width//rows
    x, y = pos 
    row = y//gap
    col = x//gap
    return row,col

# A* algorithm 
def reconstruct_path(came_from , current , draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm (draw , grid , start , end ):
    count =0 
    open_set = PriorityQueue()
    open_set.put((0,count, start))
    came_from ={}
    
    g_score = {spot : float("inf") for row in grid for spot in row }
    g_score[start]=0
    
    f_score = {spot : float("inf") for row in grid for spot in row }
    f_score[start]=h(start.get_pos(), end.get_pos())
    
    open_set_hash={start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        current = open_set.get()[2]
        open_set_hash.remove(current)
            
        if current ==end :
            current.make_end()
            reconstruct_path(came_from, end, draw)
            return True 
        for neighbor in current.neighbors :
            temp_g_score = g_score[current]+1
            if (temp_g_score<g_score[neighbor]):
                g_score[neighbor]=temp_g_score
                f_score[neighbor] = temp_g_score +h(neighbor.get_pos(), end.get_pos())
                came_from[neighbor]=current
                    
                if (neighbor not in open_set_hash):
                    count +=1
                    open_set.put((f_score[neighbor], count , neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
            draw()
            if(current !=start):
                current.make_closed()
    return False