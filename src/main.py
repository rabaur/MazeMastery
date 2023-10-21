from mazemastery.api import *
from level1 import solve as level1
from level2 import solve as level2
from level3 import solve as level3
from level4 import solve as level4
from level5 import solve as level5
from level6 import solve as level6


def test():
    while not has_minotaur():
        put_blue_gem()
        for neighbor in get_neighbors():
            if not has_blue_gem(neighbor):
                new_pos = neighbor
        set_pos(new_pos)


run(3, test, delay=100, cell_size=50, rows=11, cols=11)
