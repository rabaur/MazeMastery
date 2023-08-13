from mazemastery.api import *

found_minotaur = False
def solve():
    global found_minotaur
    put_blue_gem()
    for neighbor in get_neighbors():
        if not has_blue_gem(neighbor):
            new_pos = neighbor
            old_pos = get_pos()
            if has_minotaur() or \
                found_minotaur:
                found_minotaur = True
                return
            set_pos(new_pos)
            solve()
            put_red_gem()
            set_pos(old_pos)
    return