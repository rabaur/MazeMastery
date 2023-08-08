from mazemastery.api import *

def solve():
    while (True):
        i, j = get_pos()
        new_pos = (i, j + 1)
        set_pos(new_pos)