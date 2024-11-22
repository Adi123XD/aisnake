import pygame
import random
from enum import Enum
from collections import namedtuple
from constants import *

pygame.init()
font = pygame.font.Font('arial.ttf',25)

#reset
#reward
#play(action)->direction
#game_iteration
#is_collision
class Direction(Enum):
    RIGHT=1
    LEFT=2
    UP=3
    DOWN=4
Point = namedtuple("Point",['x', 'y'])
# BLOCK_SIZE=20
# SPEED=40
class SnakeGame:
    def __init__(self,w=640,h=480):
        # w and h are the sizes of the game screen
        self.w=w
        self.h=h
        
        
        # initialise the display 
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption("NagLok")
        self.clock = pygame.time.Clock()
        
        
        # initialise the game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2,self.h/2)
        self.snake = [self.head , Point(self.head.x-BLOCK_SIZE, self.head.y),
                    Point(self.head.x-2*BLOCK_SIZE, self.head.y)]
        self.score =0
        self.food = None 
        self._place_food()
        
    def _place_food(self):
        x= random.randint(0 , (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y= random.randint(0 , (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food= Point(x,y)
        if self.food in self.snake:
            self._place_food()
            
    
    def play_step(self):
        # 1. Collect the user input 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key==pygame.K_RIGHT:
                    self.direction= Direction.RIGHT
                elif event.key ==pygame.K_UP:
                    self.direction=Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        # 2. Move 
        self._move(self.direction)
        self.snake.insert(0,self.head)

                
        
        
        # 3. check if there is any collision 
        game_over = False 
        if self._is_collision():
            game_over = True 
            return game_over, self.score
        
        # 4. place a new food or just move 
        if (self.head == self.food):
            self.score+=1
            self._place_food()
        else :
            self.snake.pop()
        # 5. update the ui and the clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and the score 
        return game_over,self.score

    
    
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            # draw the snake 
            pygame.draw.rect(self.display ,BLUE1, pygame.Rect(pt.x , pt.y , BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display ,BLUE2, pygame.Rect(pt.x+4 , pt.y+4 , 12, 12))
            
        # draw the food 
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y , BLOCK_SIZE,BLOCK_SIZE))
        
        text = font.render("Score"+ str(self.score),True, WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()
        
    def _move(self, direction):
        x=self.head.x
        y=self.head.y
        
        if direction==Direction.RIGHT:
            x=x+BLOCK_SIZE
        elif direction == Direction.LEFT:
            x-=BLOCK_SIZE
        elif direction == Direction.UP:
            y-=BLOCK_SIZE
        elif direction==Direction.DOWN:
            y+=BLOCK_SIZE
        self.head = Point(x,y)  
        
    def _is_collision(self):
        # check if the snake hits the boundary 
        if (self.head.x>self.w-BLOCK_SIZE or self.head.x <0 
            or self.head.y>self.h-BLOCK_SIZE or self.head.y<0):
            return True
        
        # check if the snake hits itself 
        if self.head in self.snake[1:]:
            # because the first element of the snake is its head itself
            return True
        # otherwise there is no collision 
        return False 
        
        
        
        
        
        
if __name__=="__main__":
    game = SnakeGame()
    while True:
        game_over , score = game.play_step()
        if game_over==True:
            break
    print("Final Score is ", score)
    pygame.quit()