import pygame
from a_star_constants import *
from node import *
from random import choice
from enum import Enum
from collections import namedtuple
from queue import PriorityQueue
from snake import SnakeGame,Direction,a_star_snake_algorithm

def draw_score(win, score):
    font = pygame.font.Font('arial.ttf', 25)  # Create a font object
    score_text = font.render(f"Score: {score}", True, BLACK)  # Render the score text
    win.blit(score_text, (0, 0))  # Draw the score on the screen at position (10, 10)


def place_food(grid, snake):
    empty_spots = [spot for row in grid for spot in row if spot not in snake.body]
    food = choice(empty_spots)
    food.make_closed()  # Mark food with a TURQUOISE color
    return food


def main(win , width):
    # here width is the width of pygame screen
    ROWS =20
    clock = pygame.time.Clock()
    grid = make_grid(ROWS,width)
    snake = SnakeGame(grid=grid)
    food = place_food(grid,snake)
    path=[]
    
    run=True
    while run:
        draw(win, ROWS, grid, width)  # Redraw the game
        draw_score(win, snake.score)  # Display the current score
        pygame.display.update()  # Update the display
        clock.tick(10)  # Control the game speed (10 FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # Change the direction based on user input
                if event.key == pygame.K_UP and snake.direction != Direction.DOWN:
                    snake.direction = Direction.UP
                elif event.key == pygame.K_DOWN and snake.direction != Direction.UP:
                    snake.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and snake.direction != Direction.RIGHT:
                    snake.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != Direction.LEFT:
                    snake.direction = Direction.RIGHT

        # Recalculate the path if needed
        if not path or food != path[-1]:  # If path is empty or food has moved
            for row in grid:
                for spot in row:
                    spot.update_neighbors_snakegame(grid, snake.body)  # Update neighbors dynamically
            path = a_star_snake_algorithm(grid, snake.head, food)
        # Move the snake and check the game state
        # Move the snake using the A* path
        if snake.alive:
            if snake.move_ai(path, grid, food):  # Move AI-controlled snake
                food = place_food(grid, snake)  # Place new food if eaten
        else:
            print(f"Game Over! Your Score: {snake.score}")
            run = False


    pygame.quit()
    
    
if __name__=="__main__":
    win = pygame.display.set_mode((WIDTH,WIDTH))
    pygame.display.set_caption("A* snake ai")
    main(win,WIDTH)  