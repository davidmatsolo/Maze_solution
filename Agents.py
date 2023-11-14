import pygame
import heapq
from Datastructures import Maze


# Maze colors
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (255, 255, 255)
START_COLOR = (0, 255, 0)
GOAL_COLOR = (255, 0, 0)
AGENT_COLOR = (0, 0, 255)

# Pygame window dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Maze dimensions
MAZE_ROWS = 10
MAZE_COLS = 10
CELL_SIZE = WINDOW_WIDTH // MAZE_COLS

# Pygame initialization
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze Solver")


class AStarPathfinder:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def heuristic(self, current, goal):
        # Calculate Manhattan distance as the heuristic
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def get_neighbors(self, cell):
        # Get valid neighboring cells (up, down, left, right)
        row, col = cell
        neighbors = []
        if row > 0 and not self.maze[row - 1][col]:
            neighbors.append((row - 1, col))
        if row < self.rows - 1 and not self.maze[row + 1][col]:
            neighbors.append((row + 1, col))
        if col > 0 and not self.maze[row][col - 1]:
            neighbors.append((row, col - 1))
        if col < self.cols - 1 and not self.maze[row][col + 1]:
            neighbors.append((row, col + 1))
        return neighbors

    def reconstruct_path(self, came_from, current):
        # Backtrack from goal to start to construct the path
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(current)
        return path[::-1]

    def solve(self, start, goal):
        open_list = []
        closed_set = set()
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        heapq.heappush(open_list, (f_score[start], start))

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            closed_set.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue

                neighbor_g_score = g_score[current] + 1  # Assuming all movements have a cost of 1

                if neighbor not in g_score or neighbor_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = neighbor_g_score
                    f_score[neighbor] = neighbor_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return None  # No path found


class Displayer:
    def __init__(self, maze_array):
        self.maze_array = maze_array

    def draw_maze(self):
        for row in range(len(self.maze_array)):
            for col in range(len(self.maze_array[0])):
                cell_color = WALL_COLOR if self.maze_array[row][col] else PATH_COLOR
                pygame.draw.rect(window, cell_color,
                                 (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_path(self, path):
        for cell in path:
            pygame.draw.rect(window, PATH_COLOR,
                             (cell[1] * CELL_SIZE, cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_agent(self, cell):
        pygame.draw.rect(window, AGENT_COLOR,
                         (cell[1] * CELL_SIZE, cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def run_game():
    maze = Maze(10, 10)  # Create a 10x10 maze
    goal = (9, 9)  # Set the goal position
    maze.generate_maze(goal)  # Generate the maze moving towards the goal
    maze.print_grid()  # Print the maze grid
    print(maze.get_start_location().get_column_index())
    maze_array = maze.get_grid()

    pathfinder = AStarPathfinder(maze_array)
    start_cell = (0, 0)
    goal_cell = (MAZE_ROWS - 1, MAZE_COLS - 1)

    path = pathfinder.solve(start_cell, goal_cell)

    if path:
        displayer = Displayer(maze_array)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            window.fill((0, 0, 0))
            displayer.draw_maze()
            displayer.draw_path(path)

            for cell in path:
                displayer.draw_agent(cell)
                pygame.display.update()
                pygame.time.wait(300)  # Delay between agent movements

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.update()


run_game()
