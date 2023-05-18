import random
from minosrecurse.maze import create_maze
from minosrecurse.maze_utils import create_corridor, create_SAW
from minosrecurse.renderer import Renderer

LEVEL = 6
random.seed(6)
red_gem_coords = []
blue_gem_coords = []
found = False
rows, cols = 10, 15

if LEVEL == 1:
    maze = create_corridor(cols)
    minotaurus = (0, cols - 1)
elif LEVEL == 2:
    maze = create_corridor(cols)
    minotaurus = (0, random.choice(range(1, cols - 1)))
elif LEVEL == 3:
    maze, path = create_SAW(rows, cols)
    minotaurus = path[-1]
elif LEVEL == 4:
    maze = create_maze(rows, cols, (0, 0), 0.0)
    minotaurus = (rows - 4, cols - 4)
elif LEVEL == 5:
    maze = create_maze(rows, cols, (0, 0), 0.2)
    minotaurus = (rows - 4, cols - 4)
elif LEVEL == 6:
    maze = create_maze(rows, cols, (0, 0), 0.2)
    minotaurus = (rows - 4, cols - 4)

renderer = Renderer(maze, delay=1000)

renderer.draw_maze()
renderer.draw_minotaurus(minotaurus)
pos = (0, 0)


def move(new):
    global pos

    if new not in maze[pos]:
        print("OUCH!")
        new = pos
    renderer.draw_path_segment(pos, new)
    pos = new
    render(pos)


def render(pos):
    renderer.draw_row_col_numbers(pos)
    renderer.draw_gems(blue_gem_coords, red_gem_coords)
    renderer.draw_player(pos)
    renderer.update()
    renderer.after()


def put_blue_gem(cell):
    if cell not in blue_gem_coords:
        blue_gem_coords.append(cell)


def has_red_gem(cell):
    return cell in red_gem_coords


def has_blue_gem(cell):
    return cell in blue_gem_coords


def put_red_gem(cell):
    if cell not in red_gem_coords:
        red_gem_coords.append(cell)


def found_minotaurus():
    global found
    found = True


def was_found():
    return found


def get_neighbors(pos):
    """
    For students to implement.
    """
    return maze[pos]


stack = []


def level1():
    while (not was_found()):
        i, j = pos
        neighbor = (i, j + 1)
        move(neighbor)


def level2():
    while (not was_found()):
        i, j = pos
        neighbor = (i, j + 1)
        move(neighbor)
        if neighbor == minotaurus:
            found_minotaurus()

# Level 2.5: Two complexities. Neighbors and gems
# Maybe hardcoding the direction as intermediate level.

def level3():
    while (not was_found()):
        put_blue_gem(pos)
        all_neighbors = get_neighbors(pos)
        neighbors = []
        for neighbor in all_neighbors:
            if not has_blue_gem(neighbor):
                neighbors.append(neighbor)
        neighbor = neighbors[0]
        move(neighbor)
        if neighbor == minotaurus:
            found_minotaurus()


def level4():
    while (not was_found()):
        put_blue_gem(pos)
        all_neighbors = get_neighbors(pos)
        neighbors = []
        for neighbor in all_neighbors:
            if not has_blue_gem(neighbor):
                neighbors.append(neighbor)
        if neighbors != []:
            neighbor = neighbors[0]
            move(neighbor)
        else:
            for neighbor in all_neighbors:
                if not has_red_gem(neighbor):
                    put_red_gem(pos)
                    move(neighbor)
        if neighbor == minotaurus:
            found_minotaurus()


def level5():
    while (not was_found()):
        put_blue_gem(pos)
        all_neighbors = get_neighbors(pos)
        neighbors = []
        for neighbor in all_neighbors:
            if not has_blue_gem(neighbor):
                neighbors.append(neighbor)
        if neighbors != []:
            stack.append(pos)
            neighbor = neighbors[0]
        else:
            put_red_gem(pos)
            neighbor = stack.pop()
        move(neighbor)
        if neighbor == minotaurus:
            found_minotaurus()

def level6():
    put_blue_gem(pos)
    all_neighbors = get_neighbors(pos)
    for neighbor in all_neighbors:
        if not has_blue_gem(neighbor):
            old_pos = pos
            if was_found(): return
            move(neighbor)
            if neighbor == minotaurus:
                found_minotaurus()
            level6()
            put_red_gem(pos)
            move(old_pos)

if LEVEL == 1:
    level1()
elif LEVEL == 2:
    level2()
elif LEVEL == 3:
    level3()
elif LEVEL == 4:
    level4()
elif LEVEL == 5:
    level5()
elif LEVEL == 6:
    level6()
