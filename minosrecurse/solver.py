from minosrecurse.maze import create_maze
from minosrecurse.maze_utils import create_corridor, create_SAW
from minosrecurse.renderer import Renderer
import threading
import random
import time


class _State:
    """
    State is a singleton class that holds the current state of the maze solver,
    e.g., the current positions of the player, the position of gems, etc. All
    functions that manipulate the state instantiate this class and modify its
    attributes. By doing so, we don't need to bind these state-changing methods
    to a single class (so no knowledge about OOP is required) and we don't
    need to expose state as global variables (which could be imported and
    manipulated by the students directly).
    """

    _self = None

    def __new__(
        cls,
        maze=None,
        renderer=None,
        start_pos=(0, 0),
        minotaur_coords=(0, 0),
        blue_gem_coords=[],
        red_gem_coords=[],
        stack=[],
        found=False,
        *args,
        **kwargs
    ):
        if cls._self is None:
            cls._self = super(_State, cls).__new__(cls, *args, **kwargs)
            cls._self.__maze = maze
            cls._self.__renderer = renderer
            cls._self.__pos = start_pos
            cls._self.__minotaur_coords = minotaur_coords
            cls._self.__blue_gem_coords = blue_gem_coords
            cls._self.__red_gem_coords = red_gem_coords
            cls._self.__stack = stack
            cls._self.__found = found
        return cls._self

    def __init__(
        self,
        maze=None,
        renderer=None,
        start_pos=(0, 0),
        minotaur_coords=(0, 0),
        blue_gem_coords=[],
        red_gem_coords=[],
        stack=[],
        found=False,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

    @property
    def maze(self):
        return self.__maze

    @property
    def renderer(self):
        return self.__renderer

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, new):
        self.__pos = new

    @property
    def minotaur_coords(self):
        return self.__minotaur_coords

    @property
    def blue_gem_coords(self):
        return self.__blue_gem_coords

    @blue_gem_coords.setter
    def blue_gem_coords(self, new):
        self.__blue_gem_coords = new

    @property
    def red_gem_coords(self):
        return self.__red_gem_coords

    @red_gem_coords.setter
    def red_gem_coords(self, new):
        self.__red_gem_coords = new

    @property
    def stack(self):
        return self.__stack

    @stack.setter
    def stack(self, new):
        self.__stack = new

    @property
    def found(self):
        return self.__found

    @found.setter
    def found(self, new):
        self.__found = new

def pos():
    state = _State()
    return state.pos


def minotaur():
    state = _State()
    return state.minotaur_coords

def move(new_pos):
    state = _State()
    if new_pos not in state.maze[state.pos]:
        print("OUCH!")
        new_pos = state.pos
    
    old_pos = state.pos
    state.pos = new_pos
    state.renderer.update_draw(old_pos, state.pos, list(state.blue_gem_coords), list(state.red_gem_coords))
    print(threading.current_thread())
    time.sleep(0.5)


def put_blue_gem(cell):
    state = _State()
    if cell not in state.blue_gem_coords:
        state.renderer.push_blue_gem_buffer(cell)
        state.blue_gem_coords.append(cell)


def put_red_gem(cell):
    state = _State()
    if cell not in state.red_gem_coords:
        state.renderer.push_red_gem_buffer(cell)
        state.red_gem_coords.append(cell)


def has_blue_gem(cell):
    state = _State()
    return cell in state.blue_gem_coords


def has_red_gem(cell):
    state = _State()
    return cell in state.red_gem_coords


def found_minotaur():
    state = _State()
    state.found = True


def was_found():
    state = _State()
    return state.found


def get_neighbors(pos):
    state = _State()
    return state.maze[pos]


def push(pos):
    state = _State()
    new_stack = state.stack
    new_stack.append(pos)
    state.stack = new_stack


def pop():
    state = _State()
    stack = state.stack
    popped = stack.pop()
    state.stack = stack
    return popped


class Solver:
    """
    Solver is the interface for students to create and refine the maze. Solver
    creates the first State instance (and thus the only, since State is a
    singleton class) and initializes the maze and renderer, but holds no direct
    reference to the renderer, instead passes it to the state after initialization.
    """

    def __init__(self, level, rows=10, cols=10):
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
        renderer = Renderer(maze, minotaur_coords)
        self._state = _State(
            maze=maze, renderer=renderer, minotaur_coords=minotaur_coords
        )
        self.renderer.initial_draw()

    # To be implemented by students
    def solve():
        pass

    def run(self):
        print(threading.current_thread())
        solution_thread = threading.Thread(target=self.solve, name="solution_thread")
        solution_thread.start()
        self.renderer._root.mainloop()
