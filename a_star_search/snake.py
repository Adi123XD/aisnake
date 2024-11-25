import pygame
import random
from enum import Enum
from collections import namedtuple
from queue import PriorityQueue
from a_star_constants import *
from node import h

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

# Constants for A* Algorithm


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple("Point", ['x', 'y'])

class SnakeGame:
    def __init__(self, grid):
        rows = len(grid)
        mid_row, mid_col = rows // 2, rows // 2  # Middle of the grid
        # Set the head to the middle element of the grid
        self.head = grid[mid_row][mid_col]

        # Initial snake body of 3 blocks
        self.body = [
            self.head,  # The head is the first block
            grid[mid_row][mid_col - 1],  # Block to the left
            grid[mid_row][mid_col - 2],  # Second block to the left
        ]
        self.direction = Direction.RIGHT  # Initial movement direction
        self.grow = False  # Growth flag
        self.alive = True  # Track if the snake is alive
        self.score = 0  # Initial score

        # Make the initial snake blue
        for segment in self.body:
            segment.color = BLUE
            
    def move(self, grid, food):
        next_spot = None

        # Determine the next spot based on the direction
        if self.direction == Direction.RIGHT and self.head.col < self.head.total_rows - 1:
            next_spot = grid[self.head.row][self.head.col + 1]
        elif self.direction == Direction.LEFT and self.head.col > 0:
            next_spot = grid[self.head.row][self.head.col - 1]
        elif self.direction == Direction.UP and self.head.row > 0:
            next_spot = grid[self.head.row - 1][self.head.col]
        elif self.direction == Direction.DOWN and self.head.row < self.head.total_rows - 1:
            next_spot = grid[self.head.row + 1][self.head.col]

        # Check for collisions
        if not next_spot or next_spot in self.body:
            self.alive = False
            return False

        # Update the snake's body
        self.body.insert(0,next_spot)
        self.head = next_spot
        self.head.color = BLUE

        if self.grow:
            self.grow = False  # Keep the tail when growing
        else:
            tail = self.body.pop()
            tail.reset()  # Reset the tail's color

        # Check if the snake eats food
        if next_spot == food:
            self.grow = True
            self.score += 1
            return True

        return False
    
    
    
    def move_ai(self, path, grid, food):
        # TODO: if not path then continue for now 
        # TODO: later use hamiltonian circuit concept
        if not path:
            self.alive = False
            return False

        next_spot = path.pop(0)

        if next_spot in self.body:
            self.alive = False
            return False

        self.body.insert(0, next_spot)
        self.head = next_spot
        self.head.color = BLUE

        if self.grow:
            self.grow = False
        else:
            tail = self.body.pop()
            tail.reset()

        if next_spot == food:
            self.grow = True
            self.score += 1
            return True

        return False
    
# this code is for the snake ai using a*
def a_star_snake_algorithm(grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()  # Reverse the path to start from the head
            return path

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

    return None  # Return None if no path is found
