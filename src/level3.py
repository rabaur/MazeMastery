from mazemastery.api import *

def solve():
    while (not has_minotaur(get_pos())):
        put_blue_gem()
        for neighbor in get_neighbors():
            if not has_blue_gem(neighbor):
                new_pos = neighbor
                break
        set_pos(new_pos)