import random
import math

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

def create_SAW(rows, cols, temp=0.01):
    """
    Generates a maze of size `rows` x `cols` that contains a self-avoiding walk.
    """
    path = []
    pos = (0, 0)
    offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    while True:
        if pos not in path:
            path.append(pos)
        i, j = pos

        # Count number of unvisited cells for each of the possible directions
        num_unvisited = [0, 0, 0, 0]
        for (ii, jj) in path:
            if ii < i:
                num_unvisited[0] += 1
            if ii > i:
                num_unvisited[3] += 1
            if jj < j:
                num_unvisited[1] += 1
            if jj > j:
                num_unvisited[2] += 1
        potential_neighbors = [(i + di, j + dj) for di, dj in offsets]
        neighbors_counts = [(n, z) for (n, z) in zip(potential_neighbors, num_unvisited) if n[0] >= 0 and n[0] < rows and n[1] >= 0 and n[1] < cols]
        neighbors_counts = [(n, z) for (n, z) in neighbors_counts if n not in path]
        if len(neighbors_counts) == 0:
            break
        neighbors = [n for (n, _) in neighbors_counts]
        counts = [z for (_, z) in neighbors_counts]
        probs = softmax(counts, temp=-temp)
        pos = weighted_choice(neighbors, probs)
    maze = {(i, j): [] for i in range(rows) for j in range(cols)}
    for i in range(1, len(path) - 1):
        maze[path[i]] = [path[i-1], path[i+1]]
    maze[path[0]] = [path[1]]
    maze[path[-1]] = [path[-2]]
    return maze, path

def softmax(vals, temp=0.5):
    """
    Softmax function with temperature `temp`.
    """
    max_val = max(vals)
    red_vals = [v - max_val for v in vals]
    exp_vals = [math.exp(temp * v) for v in red_vals]
    sum_exp_vals = sum(exp_vals)
    return [v / (sum_exp_vals) for v in exp_vals]

def weighted_choice(choices, probs):
    """
    Chooses a random element from `choices` with probabilities `probs`.
    """
    r = random.uniform(0, 1)
    total = 0
    for c, p in zip(choices, probs):
        total += p
        if total > r:
            return c
    return choices[-1]

