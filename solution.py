import tkinter as tk
import random
from minosrecurse.maze import create_maze
from minosrecurse.renderer import draw_maze, draw_gems, draw_minotaurus

random.seed(0)
red_gem_coords = []
blue_gem_coords = []
found = False
rows, cols = 15, 10
cell_size = 50
maze = create_maze(rows, cols, (0, 0), 0.2)
root = tk.Tk()
root.title("Maze")
canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size)
canvas.pack()
render_delay = 100

draw_maze(maze, canvas=canvas, cell_size=cell_size)
minotaurus = random.choice(list(maze.keys()))
draw_minotaurus(minotaurus, canvas, cell_size // 2, cell_size)

def render():
    draw_gems(blue_gem_coords, red_gem_coords, canvas, cell_size // 2, cell_size)
    canvas.update()
    canvas.after(render_delay)

def put_blue_gem(cell):
    if cell not in blue_gem_coords:
        blue_gem_coords.append(cell)

def has_red_gem(cell):
    return cell in red_gem_coords

def has_blue_gem(cell):
    return cell in blue_gem_coords

def turn_gem_red(cell):
    if cell in blue_gem_coords:
        blue_gem_coords.remove(cell)
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

def DFS(pos):
    """
    For students to implement.
    """
    print(found)
    if was_found():
        return

    if pos == minotaurus:
        found_minotaurus()
        return

    put_blue_gem(pos)
    
    render()

    neighbors = get_neighbors(pos)
    for neighbor in neighbors:
        if not has_blue_gem(neighbor) and not has_red_gem(neighbor):
            DFS(neighbor)
    turn_gem_red(pos)
    
    render()

DFS((0, 0))

# Run the main loop
root.mainloop()