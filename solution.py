import tkinter as tk
import random
from minosrecurse.maze import create_maze
from minosrecurse.maze_utils import create_corridor, create_SAW
from minosrecurse.renderer import (
    draw_maze,
    draw_gems,
    draw_minotaurus,
    draw_player,
    draw_path_segment,
)

LEVEL = 6
random.seed(0)
red_gem_coords = []
blue_gem_coords = []
found = False
rows, cols = 15, 10
cell_size = 50

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
    minotaurus = (rows - 1, cols - 1)
elif LEVEL == 5:
    maze = create_maze(rows, cols, (0, 0), 1.0)
    minotaurus = (rows - 1, cols - 1)
elif LEVEL == 6:
    maze = create_maze(rows, cols, (0, 0), 1.0)
    minotaurus = (rows - 1, cols - 1)


root = tk.Tk()
root.title("Maze")
canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size)
canvas.pack()
render_delay = 250

draw_maze(maze, canvas=canvas, cell_size=cell_size)
draw_minotaurus(minotaurus, canvas, cell_size // 2, cell_size)
pos = (0, 0)


def move(new):
    global pos
    if new not in maze[pos]:
        print("OUCH!")
        new = pos
    draw_path_segment(pos, new, canvas, cell_size)
    pos = new
    render(pos)


def render(pos):
    draw_gems(blue_gem_coords, red_gem_coords, canvas, cell_size // 2, cell_size)
    draw_player(canvas, pos, cell_size)
    canvas.update()
    canvas.after(render_delay)


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


def search1():
    global pos
    while True:
        i, j = pos
        neighbor = (i, j + 1)
        move(neighbor)

def search2():
    global pos
    while (not was_found()):
        i, j = pos
        neighbor = (i, j + 1)
        move(neighbor)
        if neighbor == minotaurus:
            found_minotaurus()

def search3():
    global pos
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

def search4():
    global pos
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

# Probably remove
def search5():
    global pos
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

def search6():
    if was_found():
        return
    put_blue_gem(pos)
    all_neighbors = get_neighbors(pos)
    for neighbor in all_neighbors:
        if not has_blue_gem(neighbor) and not has_red_gem(neighbor):
            if neighbor == minotaurus:
                found_minotaurus()
            move(neighbor)
            search6()
            put_red_gem(pos)


if LEVEL == 1:
    search1()
elif LEVEL == 2:
    search2()
elif LEVEL == 3:
    search3()
elif LEVEL == 4:
    search4()
elif LEVEL == 5:
    search5()
elif LEVEL == 6:
    search6()


# Run the main loop
root.mainloop()
