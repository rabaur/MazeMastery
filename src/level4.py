from mazemastery.api import *


def solve() -> None:
    while not has_minotaur():
        put_blue_gem()
        found_neighbor = False
        for neighbor in get_neighbors():
            if not has_blue_gem(neighbor):
                found_neighbor = True
                new_pos = neighbor
                break
        if not found_neighbor:
            put_red_gem()
            for neighbor in get_neighbors():
                if not has_red_gem(neighbor):
                    new_pos = neighbor
                    break
        set_pos(new_pos)