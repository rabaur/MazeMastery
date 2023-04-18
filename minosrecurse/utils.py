
def get_maze_size(maze):
    m = max(i for i, _ in maze.keys()) + 1  # Number of rows
    n = max(j for _, j in maze.keys()) + 1  # Number of columns
    return m, n