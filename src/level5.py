from mazemastery.api import *

def solve():
    stack = [get_pos()]
    while (not has_minotaur(get_pos())):
        put_blue_gem()
        found_neighbor = False
        for neighbor in get_neighbors():
            if not has_blue_gem(neighbor):
                found_neighbor = True
                new_pos = neighbor
                break
        if not found_neighbor:
            put_red_gem()
            new_pos = stack.pop()
        else:
            stack.append(get_pos())
        set_pos(new_pos)