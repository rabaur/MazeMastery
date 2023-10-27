from mazemastery.api import *


def solve() -> None:
    while not has_minotaur():
        put_blue_gem()
        for neighbor in get_neighbors():
            if not has_blue_gem(neighbor):
                new_pos = neighbor
                break
        set_pos(new_pos)