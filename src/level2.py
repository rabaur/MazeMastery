from mazemastery.api import *

def solve():
    while (not has_minotaur(get_pos())):
        i, j = get_pos()
        new_pos = (i, j + 1)
        set_pos(new_pos)