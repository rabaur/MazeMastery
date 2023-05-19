import time
from minosrecurse.solver import State

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
        print("putting blue gem at", cell)
        state.renderer.push_blue_gem_buffer(cell)
        state.blue_gem_coords.append(cell)


def put_red_gem(cell):
    state = State()
    if cell not in state.red_gem_coords:
        print("putting red gem at", cell)
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