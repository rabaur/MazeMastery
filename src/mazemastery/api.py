import random
import threading
import time
from typing import Callable
import multiprocessing

from mazemastery.maze import maze_factory
from mazemastery.renderer import Renderer
from mazemastery.state import State
from mazemastery.types import Coord


def get_pos() -> Coord:
    state = State()
    return state.pos


def minotaur() -> Coord:
    state = State()
    return state.minotaur_coords


def set_pos(new_pos: Coord) -> None:
    state = State()
    if state.dead:
        return
    if new_pos not in state.maze[state.pos]:
        print(f"Invalid move: {new_pos} is not a neighbor of {state.pos}")
        # We don't subtract a life on level 1
        print(f"{state.level} state.level")
        if state.level != 1:
            print("You lose a life!")
            state.lives -= 1
        new_pos = state.pos
    old_pos = state.pos

    # The end screen on level 1 cannot be checked with a seperate solution
    # thread, since we don't strictly need to terminate the solution for it
    # to be valid (since the minotaur is at the end of the corridor).
    if state.level == 1 and new_pos == state.minotaur_coords:
        state.renderer.draw_popup("You found the minotaur!\nContinue to the next level ...")
    state.pos = new_pos
    if state.lives == 0:
        state.renderer.draw_popup("You died!")
        state.dead = True
    state.renderer.update_draw(old_pos, state.pos, state.lives)
    time.sleep(state.renderer.delay / 1000)
    while state.renderer.debug:
        time.sleep(state.renderer.delay / 1000)


def put_blue_gem() -> None:
    state = State()
    pos = state.pos
    if pos not in state.blue_gem_coords:
        state.renderer.push_blue_gem_buffer(pos)
        state.blue_gem_coords.append(pos)


def put_red_gem() -> None:
    state = State()
    pos = state.pos
    if pos not in state.red_gem_coords:
        state.renderer.push_red_gem_buffer(pos)
        state.red_gem_coords.append(pos)


def has_blue_gem(cell: Coord) -> bool:
    state = State()
    return cell in state.blue_gem_coords


def has_red_gem(cell: Coord) -> bool:
    state = State()
    return cell in state.red_gem_coords


def has_minotaur() -> bool:
    state = State()
    return state.pos == state.minotaur_coords


def is_neighbor(pos: Coord, neighbor: Coord) -> bool:
    state = State()
    return neighbor in state.maze[pos]


def are_neighbors(pos1: Coord, pos2: Coord) -> bool:
    state = State()
    return pos2 in state.maze[pos1]


def get_neighbors() -> list[Coord]:
    state = State()
    pos = state.pos
    return state.maze[pos]


def run(
    level: int,
    solve: Callable[[], None],
    rows: int = 10,
    cols: int = 10,
    cell_size: int = 50,
    delay: int = 1000,
    seed: int | None = None,
) -> None:
    random.seed(seed)
    maze, minotaur_coords = maze_factory(level, rows, cols)
    renderer = Renderer(
        maze,
        minotaur_coords,
        cell_size=cell_size,
        delay=delay
    )
    State(
        maze=maze,
        renderer=renderer,
        minotaur_coords=minotaur_coords,
        level=level,
    )
    renderer.initial_draw()
    solution_thread = threading.Thread(target=solve, name="solution_thread")
    solution_thread.start()

    # This function runs on a seperate thread and repeatedly checks if the
    # the solution thread is dead. If so, we check if the player has found the
    # minotaur.
    def check_if_found_minotaur():
        while True:
            time.sleep(0.1)
            if solution_thread.is_alive():
                continue
            state = State()
            if state.pos == state.minotaur_coords:
                renderer.draw_popup("You found the minotaur!\nContinue to the next level ...")
            break
    check_solution_thread = threading.Thread(
        target=check_if_found_minotaur,
        name="check_if_found_minotaur_thread"
    )
    check_solution_thread.start()
    renderer.root.mainloop()
