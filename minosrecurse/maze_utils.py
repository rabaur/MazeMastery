import random

def get_maze_size(maze):
    m = max(i for i, _ in maze.keys()) + 1  # Number of rows
    n = max(j for _, j in maze.keys()) + 1  # Number of columns
    return m, n

def create_corridor(length):
    """
    Generates a maze of length `length` that is a single path.
    """
    maze = {}
    for j in range(1, length-1):
        maze[(0, j)] = [(0, j+1), (0, j-1)]
    maze[(0, 0)] = [(0, 1)]
    maze[(0, length-1)] = [(0, length-2)]
    return maze

def create_SAW(rows, cols, temp=0.5):
    """
    Generates a maze of size `rows` x `cols` that contains a self-avoiding walk.
    """
    path = []
    pos = (0, 0)
    offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    while True:
        path.append(pos)
        i, j = pos

        # Count number of unvisited cells for each of the possible directions
        num_unvisited = {
            "up": 0,
            "left": 0,
            "right": 0,
            "down": 0
        }
        for ii in range(rows):
            for jj in range(cols):
                if (ii, jj) in path:
                    continue
                if ii < i:
                    num_unvisited["up"] += 1
                if ii > i:
                    num_unvisited["down"] += 1
                if jj < j:
                    num_unvisited["left"] += 1
                if jj > j:
                    num_unvisited["right"] += 1
        print(num_unvisited)
        potential_neighbors = [(pos[0] + di, pos[1] + dj) for di, dj in offsets]
        neighbors = [n for n in potential_neighbors if n[0] >= 0 and n[0] < rows and n[1] >= 0 and n[1] < cols]
        neighbors = [n for n in neighbors if n not in path]
        if len(neighbors) == 0:
            break
        pos = random.choice(neighbors)
    maze = {(i, j): [] for i in range(rows) for j in range(cols)}
    for i in range(1, len(path) - 1):
        maze[path[i]] = [path[i-1], path[i+1]]
    maze[path[0]] = [path[1]]
    maze[path[-1]] = [path[-2]]
    return maze, path