from minosrecurse.maze import create_maze
from minosrecurse.maze_utils import create_corridor, create_SAW
from minosrecurse.renderer import Renderer
from minosrecurse.state import State
import threading
import random

def pos():
    state = State()
    return state.pos


def minotaur():
    state = State()
    return state.minotaur_coords

def move(new_pos):
    state = State()
    if new_pos not in state.maze[state.pos]:
        print("OUCH!")
        new_pos = state.pos
    
    old_pos = state.pos
    state.pos = new_pos
    state.renderer.update_draw(old_pos, state.pos)
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

class Solver:
    """
    Solver is the interface for students to create and refine the maze. Solver
    creates the first State instance (and thus the only, since State is a
    singleton class) and initializes the maze and renderer, but holds no direct
    reference to the renderer, instead passes it to the state after initialization.
    """

    def __init__(self, level, rows=10, cols=10, cell_size=50):
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
        self._renderer = Renderer(maze, minotaur_coords, cell_size=cell_size)
        self._state = State(
            maze=maze, renderer=self._renderer, minotaur_coords=minotaur_coords
        )
        self._renderer.initial_draw()

    # To be implemented by students
    def solve():
        pass

    def run(self):
        solution_thread = threading.Thread(target=self.solve, name="solution_thread")
        solution_thread.start()
        self._renderer.root.mainloop()