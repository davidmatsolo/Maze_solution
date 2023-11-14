
import random
from collections import deque



class Location:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def get_column_index(self):
        return self.column

    def get_row_index(self):
        return self.row

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1] * width for _ in range(height)]
        self.start_location = None
        self.goal_location = None
        self.enemy = None

    def is_valid_cell(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def set_cell(self, x, y, value):
        if self.is_valid_cell(x, y):
            self.grid[y][x] = value

    def get_cell(self, x, y):
        if self.is_valid_cell(x, y):
            return self.grid[y][x]
        return None

    def set_start_location(self, x, y):
        if self.is_valid_cell(x, y):
            self.start_location = Location(x, y)

    def set_goal_location(self, x, y):
        if self.is_valid_cell(x, y):
            self.goal_location = Location(x, y)

    def set_enemy(self, enemy):
        self.enemy = enemy

    def get_enemy(self):
        return self.enemy

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def  get_start_location(self):
        return self.start_location

    def is_goal(self, location):
        goal_location = self.goal_location
        return goal_location is not None and location == goal_location

    def is_wall(self, location):
        x, y = location.get_column_index(), location.get_row_index()
        return self.is_valid_cell(x, y) and self.get_cell(x, y)

    def is_enemy(self, location):
        enemy_location = self.get_enemy().get_enemy_location()
        return enemy_location is not None and location == enemy_location

    def print_grid(self):
        for row in self.grid:
            print(row)



    def get_grid(self):
        return self.grid

    def generate_maze(self, goal):
        start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        self.start_location = Location(start_x, start_y)
        self.grid[start_y][start_x] = 0

        queue = deque([(start_x, start_y)])

        while queue:
            current_x, current_y = queue.popleft()

            if (current_x, current_y) == goal:
                break

            neighbors = []
            if current_x > 1:  # Left
                neighbors.append((current_x - 2, current_y))
            if current_x < self.width - 2:  # Right
                neighbors.append((current_x + 2, current_y))
            if current_y > 1:  # Up
                neighbors.append((current_x, current_y - 2))
            if current_y < self.height - 2:  # Down
                neighbors.append((current_x, current_y + 2))

            random.shuffle(neighbors)

            for neighbor_x, neighbor_y in neighbors:
                if self.grid[neighbor_y][neighbor_x] == 1:
                    self.grid[neighbor_y][neighbor_x] = 0
                    self.grid[current_y + (neighbor_y - current_y) // 2][current_x + (neighbor_x - current_x) // 2] = 0
                    queue.append((neighbor_x, neighbor_y))

            goal_x = goal[0]
            goal_y = goal[1]
            self.grid[goal_x][goal_y] = 0
            self.goal_location = Location(goal_x, goal_y)

# ...

maze = Maze(10, 10)  # Create a 10x10 maze
goal = (9, 9)  # Set the goal position
maze.generate_maze(goal)  # Generate the maze moving towards the goal
maze.print_grid()  # Print the maze grid
print(maze.get_start_location().get_column_index())


"""
[
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    ]
"""