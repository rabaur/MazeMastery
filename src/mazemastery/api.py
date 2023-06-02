import time
import random
from mazemastery.maze import create_maze, create_corridor, create_SAW
from mazemastery.renderer import GUI
import threading
from mazemastery.state import State

def get_pos():
    state = State()
    return state.pos

def minotaur():
    state = State()
    return state.minotaur_coords

def set_pos(new_pos):
    state = State()
    if state.dead:
        return
    if new_pos not in state.maze[state.pos]:
        state.lives -= 1
        new_pos = state.pos
    old_pos = state.pos
    state.pos = new_pos
    if state.lives == 0:
        state.renderer.draw_popup("You died!")
        state.dead = True
    state.renderer.update_draw(old_pos, state.pos, state.lives)
    time.sleep(state.renderer.delay / 1000)
    while (state.renderer.debug):
        time.sleep(state.renderer.delay / 1000)

def put_blue_gem(cell):
    state = State()
    if cell not in state.blue_gem_coords:
        state.renderer.push_blue_gem_buffer(cell)
        state.blue_gem_coords.append(cell)


def put_red_gem(cell):
    state = State()
    if cell not in state.red_gem_coords:
        state.renderer.push_red_gem_buffer(cell)
        state.red_gem_coords.append(cell)


def has_blue_gem(cell):
    state = State()
    return cell in state.blue_gem_coords


def has_red_gem(cell):
    state = State()
    return cell in state.red_gem_coords

def has_minotaur(cell):
    state = State()
    return cell == state.minotaur_coords


def found_minotaur():
    state = State()
    state.found = True


def was_found():
    state = State()
    return state.found


def get_neighbors(pos):
    state = State()
    return state.maze[pos]


def push(pos):
    state = State()
    state.stack.append(pos)

def pop():
    state = State()
    popped = state.stack.pop()
    return popped

def run(level, solve, rows=10, cols=10, cell_size=50, delay=1000, seed=None):
    random.seed(seed)
    if level == 1:
        maze = create_corridor(cols)
        minotaur_coords = (0, cols - 1)
    elif level == 2:
        maze = create_corridor(cols)
        minotaur_coords = (0, random.choice(range(1, cols - 1)))
    elif level == 3:
        maze, path = create_SAW(rows, cols)
        minotaur_coords = path[-1]
    elif level == 4:
        maze = create_maze(rows, cols, (0, 0), 0.0)
        minotaur_coords = (rows - 4, cols - 4)
    elif level == 5:
        maze = create_maze(rows, cols, (0, 0), 0.2)
        minotaur_coords = (rows - 4, cols - 4)
    elif level == 6:
        maze = create_maze(rows, cols, (0, 0), 0.2)
        minotaur_coords = (rows - 4, cols - 4)
    renderer = GUI(maze, minotaur_coords, cell_size=cell_size, delay=delay)
    state = State(
        maze=maze, renderer=renderer, minotaur_coords=minotaur_coords
    )
    renderer.initial_draw()
    solution_thread = threading.Thread(target=solve, name="solution_thread")
    solution_thread.start()
    renderer.root.mainloop()