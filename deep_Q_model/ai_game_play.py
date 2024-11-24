import torch
from snake_game_ai import SnakeGameAI, Direction, Point
from model import Linear_QNet
from agent import Agent
from constants import *

def play_with_trained_model():
    # Initialize game
    game = SnakeGameAI()
    agent = Agent()
    
    # Load the trained model
    model = Linear_QNet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
    model.load()
    model.eval()  # Set model to evaluation mode

    while True:
        # Get current state
        state = agent.get_state(game)
        
        # Predict the best action
        state_tensor = torch.tensor(state, dtype=torch.float)
        with torch.no_grad():  # Disable gradient calculations
            prediction = model(state_tensor)
        move = torch.argmax(prediction).item()

        # Convert move to action
        action = [0, 0, 0]
        action[move] = 1

        # Perform the action
        reward, game_over, score = game.play_step(action)
        
        if game_over:
            print(f"Game Over! Final Score: {score}")
            game.reset()
            
# # Helper function to get the state (copied from Agent class)
# def get_state(game):
#     head = game.snake[0]
#     point_r = Point(head.x + BLOCK_SIZE, head.y)
#     point_l = Point(head.x - BLOCK_SIZE, head.y)
#     point_u = Point(head.x, head.y - BLOCK_SIZE)
#     point_d = Point(head.x, head.y + BLOCK_SIZE)

#     dir_r = game.direction == Direction.RIGHT
#     dir_l = game.direction == Direction.LEFT
#     dir_u = game.direction == Direction.UP
#     dir_d = game.direction == Direction.DOWN

#     state = [
#         # Danger straight
#         (dir_r and game.is_collision(point_r)) or 
#         (dir_l and game.is_collision(point_l)) or 
#         (dir_u and game.is_collision(point_u)) or 
#         (dir_d and game.is_collision(point_d)),

#         # Danger right
#         (dir_r and game.is_collision(point_d)) or 
#         (dir_d and game.is_collision(point_l)) or 
#         (dir_l and game.is_collision(point_u)) or 
#         (dir_u and game.is_collision(point_r)),

#         # Danger left
#         (dir_r and game.is_collision(point_u)) or 
#         (dir_d and game.is_collision(point_r)) or 
#         (dir_l and game.is_collision(point_d)) or 
#         (dir_u and game.is_collision(point_l)),

#         # Move direction
#         dir_l,
#         dir_r,
#         dir_u,
#         dir_d,

#         # Food location
#         game.food.x < game.head.x,  # food left
#         game.food.x > game.head.x,  # food right
#         game.food.y < game.head.y,  # food up
#         game.food.y > game.head.y  # food down
#     ]
#     return np.array(state, dtype=int)

if __name__ == "__main__":
    play_with_trained_model()
