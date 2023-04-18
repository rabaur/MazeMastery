import random
from utils import get_maze_size

def creates_hole(maze, c0, c1):
    """
    Check if the removal of the wall between neighbor1 and neighbor2 creates a
    empty space of size at least 2x2 or larger.

    Assumes that wall between c0 and c1 exists.
    """
    m, n = get_maze_size(maze)

    if (c0[0] == c1[0]):
        # Rows agree, so we would remove a vertical wall.
        assert c0[1] != c1[1]

        # Make sure c0 is always left of c1
        if c1[1] < c0[1]: c0, c1 = c1, c0

        # Check if removal of this wall would create a hole above and below.
        for i in range(max(0, c0[0] - 1), c0[0] + 1):
            # Count number of neighbors within 2x2 subgraph whose North-West cell
            # is (i, c0[1]).
            count = 0
            count += (i, c0[1] + 1) in maze[(i, c0[1])] # East neighbor of North-West cell
            count += (i + 1, c0[1]) in maze[(i, c0[1])] # South neighbor of North-West cell
            count += (i, c0[1] + 1) in maze[(i + 1, c0[1] + 1)] # North neighbor of South-East cell
            count += (i + 1, c0[1]) in maze[(i + 1, c0[1] + 1)] # West neighbor of South-East cell

            assert count <= 3 # If the maze has a 2x2 whole already, we messed up.
            print(f"{count=}")
            if count + 1 == 4:
                print("Hole above and below")
                return True
    else:
        # Columns agree, so we would remove a horizontal wall.
        assert c0[0] != c1[0]

        # Make sure c0 is always above c1
        if c1[0] < c0[0]: c0, c1 = c1, c0

        # Check if removal of this wall would create a hole to the left and right.
        for j in range(max(0, c0[1] - 1), c1[1] + 1):
            # Count number of neighbors within 2x2 subgraph whose North-West cell
            # is (c0[0], j).
            count = 0
            count += (c0[0], j + 1) in maze[(c0[0], j)] # East neighbor of North-West cell
            count += (c0[0] + 1, j) in maze[(c0[0], j)] # South neighbor of North-West cell
            count += (c0[0], j + 1) in maze[(c0[0] + 1, j + 1)] # North neighbor of South-East cell
            count += (c0[0] + 1, j) in maze[(c0[0] + 1, j + 1)] # West neighbor of South-East cell

            assert count <= 3 # If the maze has a 2x2 whole already, we messed up.
            print(f"{count=}")
            if count + 1 == 4:
                print("Hole to the left and right")
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
                if creates_hole(maze, (i, j), wall):
                    continue
                if random.random() <= p_remove:
                    # Remove wall (connect neighbors)
                    print("Removing wall between", (i, j), "and", wall)
                    maze[(i, j)].append(wall)
                    maze[wall].append((i, j))

    return maze

if __name__ == "__main__":
    maze = create_maze(10, 10, (0, 0))
    print(maze)
