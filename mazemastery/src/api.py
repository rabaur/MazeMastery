import time
from mazemastery.src.solver import State

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