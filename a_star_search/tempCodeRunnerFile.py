import pygame
import random
from enum import Enum
from collections import namedtuple
from queue import PriorityQueue
from constants import *  # Assuming constants are defined as before

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

# Constants for A* Algorithm
BLOCK_SIZE = 20
SPEED = 40

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple("Point", ['x', 'y'])

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("NagLok")
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - 2 * BLOCK_SIZE, self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # AI decision making using A* algorithm
        game_over = False
        self.move_ai()

        # Check for collision
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # If the snake eats food
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # Update the UI and clock
        self._update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score

    def move_ai(self):
        # Use A* to find the path from the snake head to the food
        grid = self.create_grid()
        start = self.snake[0]
        end = self.food

        path = self.a_star(grid, start, end)
        if path:
            # Follow the first direction in the path
            next_move = path[1]  # Second point in the path is the first move
            self.direction = self.get_direction(self.snake[0], next_move)
            self._move(self.direction)

    def create_grid(self):
        grid = []
        for y in range(0, self.h, BLOCK_SIZE):
            row = []
            for x in range(0, self.w, BLOCK_SIZE):
                # If the point is part of the snake, mark it as blocked
                if Point(x, y) in self.snake:
                    row.append(1)  # Barrier
                else:
                    row.append(0)  # Open space
            grid.append(row)
        return grid

    def a_star(self, grid, start, end):
        # A* implementation
        start_node = (start.x // BLOCK_SIZE, start.y // BLOCK_SIZE)
        end_node = (end.x // BLOCK_SIZE, end.y // BLOCK_SIZE)

        # Initialize open and closed sets
        open_set = PriorityQueue()
        open_set.put((0, start_node))
        came_from = {}
        g_score = {start_node: 0}
        f_score = {start_node: self.heu(start_node, end_node)}

        while not open_set.empty():
            _, current = open_set.get()

            if current == end_node:
                # Reconstruct the path
                path = self.reconstruct_path(came_from, current)
                return path

            neighbors = self.get_neighbors(current, grid)
            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heu(neighbor, end_node)
                    open_set.put((f_score[neighbor], neighbor))

        return None  # No path found
    def heu(self,p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def get_neighbors(self, node, grid):
        # Return valid neighbors for the A* algorithm
        neighbors = []
        x, y = node
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[ny][nx] != 1:
                neighbors.append((nx, ny))

        return neighbors

    def reconstruct_path(self, came_from, current):
        # Reconstruct the path from end to start
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path

    def h(self, p1, p2):
        # Heuristic function (Manhattan distance)
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def get_direction(self, head, next_point):
        # Determine the direction based on the next point in the path
        if next_point[0] > head.x // BLOCK_SIZE:
            return Direction.RIGHT
        elif next_point[0] < head.x // BLOCK_SIZE:
            return Direction.LEFT
        elif next_point[1] > head.y // BLOCK_SIZE:
            return Direction.DOWN
        elif next_point[1] < head.y // BLOCK_SIZE:
            return Direction.UP

    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x = x + BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)
        self.snake.insert(0, self.head)

    def _is_collision(self):
        if (self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or
            self.head.y > self.h - BLOCK_SIZE or self.head.y < 0):
            return True

        if self.head in self.snake[1:]:
            return True
        return False


if __name__ == "__main__":
    game = SnakeGame()
    while True:
        game_over, score = game.play_step()
        if game_over:
            break
    print("Final Score is ", score)
    pygame.quit()
