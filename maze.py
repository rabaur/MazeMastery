import random
from utils import get_maze_size

def count_neighbors_in_2x2_subgraph(maze, bi, bj):
    """
    Count number of neighbors within 2x2 subgraph whose North-West cell
    is (bi, bj).
    """
    count = 0
    count += (bi, bj + 1) in maze[(bi, bj)] # East of North-West
    count += (bi + 1, bj) in maze[(bi, bj)] # South of North-West
    count += (bi, bj + 1) in maze[(bi + 1, bj + 1)] # North of South-East
    count += (bi + 1, bj) in maze[(bi + 1, bj + 1)] # West of South-East cell
    return count

def creates_2x2_hole(maze, c0, c1):
    """
    Check if the removal of the wall between neighbor1 and neighbor2 creates a
    empty space of size at least 2x2 or larger.

    Assumes that wall between c0 and c1 exists.
    """
    c0, c1 = sorted([c0, c1])

    if (c0[0] == c1[0]):
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

    return maze

if __name__ == "__main__":
    maze = create_maze(10, 10, (0, 0))
    print(maze)
