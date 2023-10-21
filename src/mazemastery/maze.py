import random
import math


def randomize_neighbor_order(maze):
    """
    Randomizes the order of neighbors of each cell in the maze to
    avoid users relying on a specific order.
    """
    for node, neighbors in maze.items():
        random.shuffle(neighbors)
        maze[node] = neighbors
    return maze


def get_maze_size(maze):
    m = max(i for i, _ in maze.keys()) + 1  # Number of rows
    n = max(j for _, j in maze.keys()) + 1  # Number of columns
    return m, n


def create_corridor(length):
    """
    Generates a maze of length `length` that is a single path.
    """
    maze = {}
    for j in range(1, length - 1):
        maze[(0, j)] = [(0, j + 1), (0, j - 1)]
    maze[(0, 0)] = [(0, 1)]
    maze[(0, length - 1)] = [(0, length - 2)]
    maze = randomize_neighbor_order(maze)
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
        for ii, jj in path:
            if ii < i:
                num_unvisited[0] += 1
            if ii > i:
                num_unvisited[3] += 1
            if jj < j:
                num_unvisited[1] += 1
            if jj > j:
                num_unvisited[2] += 1
        potential_neighbors = [(i + di, j + dj) for di, dj in offsets]
        neighbors_counts = [
            (n, z)
            for (n, z) in zip(potential_neighbors, num_unvisited)
            if n[0] >= 0 and n[0] < rows and n[1] >= 0 and n[1] < cols
        ]
        neighbors_counts = [(n, z) for (n, z) in neighbors_counts if n not in path]
        if len(neighbors_counts) == 0:
            break
        neighbors = [n for (n, _) in neighbors_counts]
        counts = [z for (_, z) in neighbors_counts]
        probs = softmax(counts, temp=-temp)
        pos = weighted_choice(neighbors, probs)
    maze = {(i, j): [] for i in range(rows) for j in range(cols)}
    for i in range(1, len(path) - 1):
        maze[path[i]] = [path[i - 1], path[i + 1]]
    maze[path[0]] = [path[1]]
    maze[path[-1]] = [path[-2]]
    maze = randomize_neighbor_order(maze)
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


def count_neighbors_in_2x2_subgraph(maze, bi, bj):
    """
    Count number of neighbors within 2x2 subgraph whose North-West cell
    is (bi, bj).
    """
    count = 0
    count += (bi, bj + 1) in maze[(bi, bj)]  # East of North-West
    count += (bi + 1, bj) in maze[(bi, bj)]  # South of North-West
    count += (bi, bj + 1) in maze[(bi + 1, bj + 1)]  # North of South-East
    count += (bi + 1, bj) in maze[(bi + 1, bj + 1)]  # West of South-East cell
    return count


def creates_2x2_hole(maze, c0, c1):
    """
    Check if the removal of the wall between neighbor1 and neighbor2 creates a
    empty space of size at least 2x2 or larger.

    Assumes that wall between c0 and c1 exists.
    """
    c0, c1 = sorted([c0, c1])

    if c0[0] == c1[0]:
        # Rows agree, so we would remove a vertical wall.

        # Check if removal of this wall would create a hole above and below.
        for i in range(max(0, c0[0] - 1), c0[0] + 1):
            # Count number of neighbors within 2x2 subgraph whose North-West cell
            # is (i, c0[1]).
            count = count_neighbors_in_2x2_subgraph(maze, i, c0[1])

            if count + 1 == 4:
                # In this case, the removal of the wall would create a hole.
                return True
    else:
        # Columns agree, so we would remove a horizontal wall.

        # Check if removal of this wall would create a hole to the left and right.
        for j in range(max(0, c0[1] - 1), c1[1] + 1):
            # Count number of neighbors within 2x2 subgraph whose North-West cell
            # is (c0[0], j).
            count = count_neighbors_in_2x2_subgraph(maze, c0[0], j)

            if count + 1 == 4:
                # In this case, the removal of the wall would create a hole.
                return True
    return False


def create_maze(rows, cols, start, p_remove=0.9):
    """
    Performs randomized depth-first search to create a maze.
    """

    # The maze graph is represented as a dictionary of sets.
    # A node is a 2-tupel (i, j) representing the row and column of a cell.
    # The list of neighbors of a node is the set of nodes that can be reached
    # from the node.
    maze = {(i, j): [] for i in range(rows) for j in range(cols)}
    prev = {(i, j): None for i in range(rows) for j in range(cols)}
    stack = [start]
    visited = set()
    offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    while len(stack) > 0:
        current = stack.pop()
        if prev[current]:
            if prev[current] not in current:
                maze[current].append(prev[current])
                maze[prev[current]].append(current)
        visited.add(current)
        i, j = current
        neighbors = [(i + di, j + dj) for di, dj in offsets]
        neighbors = [n for n in neighbors if n in maze and n not in visited]
        if len(neighbors) == 0:
            continue
        random.shuffle(neighbors)
        for neighbor in neighbors:
            prev[neighbor] = current
            stack.append(neighbor)

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            all_neighbors = [(i + di, j + dj) for di, dj in offsets]
            walls = [n for n in all_neighbors if n not in maze[(i, j)]]
            for wall in walls:
                if creates_2x2_hole(maze, (i, j), wall):
                    continue
                if random.random() <= p_remove:
                    # Remove wall (by connecting neighbors)
                    maze[(i, j)].append(wall)
                    maze[wall].append((i, j))

    for node, neighbors in maze.items():
        maze[node] = list(set(neighbors))

    maze = randomize_neighbor_order(maze)

    return maze


if __name__ == "__main__":
    maze = create_maze(10, 10, (0, 0))
    print(maze)
