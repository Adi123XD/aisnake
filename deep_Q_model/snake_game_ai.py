import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
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
class SnakeGameAI:
    def __init__(self,w=640,h=480):
        # w and h are the sizes of the game screen
        self.w=w
        self.h=h
        
        
        # initialise the display 
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption("NagLok")
        self.clock = pygame.time.Clock()
        
        self.reset()
        
    def reset(self):
        # initialise the game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2,self.h/2)
        self.snake = [self.head , Point(self.head.x-BLOCK_SIZE, self.head.y),
                    Point(self.head.x-2*BLOCK_SIZE, self.head.y)]
        self.score =0
        self.food = None 
        self._place_food()
        self.frame_iteration = 0
        
    def _place_food(self):
        x= random.randint(0 , (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y= random.randint(0 , (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food= Point(x,y)
        if self.food in self.snake:
            self._place_food()
            
    
    # def play_step(self,action):
    #     self.frame_iteration+=1
    #     # 1. Collect the user input 
    #     for event in pygame.event.get():
    #         if event.type==pygame.QUIT:
    #             pygame.quit()
    #             quit()
    #     # 2. Move 
    #     self._move(action)
    #     self.snake.insert(0,self.head)

                
        
        
    #     # 3. check if there is any collision 
    #     game_over = False 
    #     reward =0
    #     if self.is_collision()or self.frame_iteration>100*len(self.snake):
    #         game_over = True 
    #         reward = -10
    #         return reward , game_over, self.score
        
    #     # 4. place a new food or just move 
    #     if (self.head == self.food):
    #         self.score+=1
    #         reward =10
    #         self._place_food()
    #     else :
    #         self.snake.pop()
    #     # 5. update the ui and the clock
    #     self._update_ui()
    #     self.clock.tick(SPEED)
    #     # 6. return game over and the score 
    #     return reward, game_over , self.score
    
    
    def play_step(self, action):
        self.frame_iteration += 1
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. Move
        self._move(action)
        self.snake.insert(0, self.head)

        # 3. Check for collisions
        reward = -0.5  # Default reward for doing nothing
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -24  # Heavy penalty for collisions
            return reward, game_over, self.score

        # 4. Place a new food or move
        if self.head == self.food:
            self.score += 1
            reward = 20  # Reward for eating food
            self._place_food()
        else:
            # Reward for getting closer to the food
            dist_old = self._distance(self.snake[1], self.food)
            dist_new = self._distance(self.head, self.food)
            if dist_new < dist_old:
                reward += 0.3  # Positive reward for getting closer
            else:
                reward -= 0.1  # Slight penalty for moving away
            self.snake.pop()

        # 5. Update the UI and clock
        self._update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

    
    
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
        
    def _move(self, action):  
        
        # [straight, right , left] 
        clockwise =[Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(self.direction)
        
        if(np.array_equal(action, [1,0,0])):
            # which means that we continue the previous direction 
            new_dir = clockwise[idx]
        elif (np.array_equal(action, [0,1,0])):
            new_dir = clockwise[(idx+1)%4]  
            # taking  a right turn if right then go dowm if down then go left etc
        else :
            # time for left turn 
            new_dir = clockwise[(idx-1)%4]
        self.direction = new_dir
        x=self.head.x
        y=self.head.y
        
        if self.direction==Direction.RIGHT:
            x=x+BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x-=BLOCK_SIZE
        elif self.direction == Direction.UP:
            y-=BLOCK_SIZE
        elif self.direction==Direction.DOWN:
            y+=BLOCK_SIZE
        self.head = Point(x,y)  
        
    def is_collision(self, pt=None):
        if pt is None :
            pt = self.head
        # check if the snake hits the boundary 
        if (pt.x>self.w-BLOCK_SIZE or pt.x <0 
            or pt.y>self.h-BLOCK_SIZE or pt.y<0):
            return True
        
        # check if the snake hits itself 
        if pt in self.snake[1:]:
            # because the first element of the snake is its head itself
            return True
        # otherwise there is no collision 
        return False 
    
    
    def _distance(self, p1, p2):
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

        
        
        
        
        
        
