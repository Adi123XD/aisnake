import torch
import random 
import numpy as np 
from snake_game_ai import Direction,SnakeGameAI, Point
from collections import deque
from constants import *

class Agent :
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness
        self.gamma =0
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model= None
        self.trainer= None        
        # TODO: model, trainer
    
    def get_state(self, game):
        # fetch the head of the snake 
        head = game.snake[0]
        
        # points surroudning it to check where the danger lies 
        point_r = Point(head.x+BLOCK_SIZE, head.y)
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y-BLOCK_SIZE)
        point_d = Point(head.x, head.y+BLOCK_SIZE)
        
        # current direction 
        dir_r = game.direction ==Direction.RIGHT
        dir_l = game.direction ==Direction.LEFT
        dir_u = game.direction ==Direction.UP
        dir_d = game.direction ==Direction.DOWN
        
        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r))or 
            (dir_l and game.is_collision(point_l))or 
            (dir_u and game.is_collision(point_u))or 
            (dir_d and game.is_collision(point_d)),
            
            # Danger right 
            (dir_r and game.is_collision(point_d))or 
            (dir_d and game.is_collision(point_l))or 
            (dir_l and game.is_collision(point_u))or 
            (dir_u and game.is_collision(point_r)),
            
            # Danger left  
            (dir_r and game.is_collision(point_u))or 
            (dir_d and game.is_collision(point_r))or 
            (dir_l and game.is_collision(point_d))or 
            (dir_u and game.is_collision(point_l)),
            
            # move direction 
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x, #food left 
            game.food.x > game.head.x, #food right 
            game.food.y < game.head.y, #food up
            game.food.y > game.head.y  #food down 
        ]
        return np.array(state,dtype=int)
        
    
    def remember(self, state , action , reward, next_state, done):
        self.memory.append(state , action , reward, next_state, done)
        
        # popleft if max memory is reached
    
    def train_long_memory(self):
        if len(self.memory)> BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else :
            mini_sample = self.memory
        states , actions , rewards, next_states , dones = zip(*mini_sample)
        self.trainer.train(states,actions,rewards,next_states,dones)
    
    def train_short_memory(self,state , action , reward, next_state, done):
        self.trainer.train(state , action , reward, next_state, done)
    
    def get_action(self, state):
        # random move : tradeoff  betweem exploration /exploitation
        self.epsilon = 80- self.n_games
        if(random.randint(0,200)< self.epsilon):
            final_move = [0,0,0]
            move = random.randint(0,2)
            final_move[move]=1
        else :
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model.predict(state0)
            move = torch.argmax(prediction).item()
            final_move[move]=1
        return final_move
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0  
    agent= Agent()
    game = SnakeGameAI()
    
    while True:
        # 1. get old state 
        state_old = agent.get_state(game)
        
        # 2. get move 
        final_move = agent.get_action(state_old)
        
        # 3. perform the move and calculate the new state 
        reward , done , score = game.play_step(final_move)
        state_new = agent.get_state(game)
        
        # train short memory 
        agent.train_short_memory(state_old, final_move, reward, state_old, done)
        
        # remeber 
        agent.remember(state_old, final_move, reward, state_new, done)
        
        if done :
            # train long memory and plot the result 
            game.reset()
            agent.n_games+=1
            agent.train_long_memory()
            
            if score>record:
                record =score 
                # agent.model.save()
                
            print("Game : ", agent.n_games, "Score : ",score, "record : ",record)
            # TODO: plot     
        
        
        

if __name__=="__main__":
    train()
