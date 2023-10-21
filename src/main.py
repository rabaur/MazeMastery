from mazemastery.api import *
from level1 import solve as level1
from level2 import solve as level2
from level3 import solve as level3
from level4 import solve as level4
from level5 import solve as level5
from level6 import solve as level6


def jumpy_recursion(node):
    if not has_blue_gem(node):
        set_pos(node)
        put_blue_gem()
        neighbors = get_neighbors()
        for neighbor in neighbors:
            if not has_blue_gem(neighbor):
                jumpy_recursion(neighbor)


run(4, lambda: jumpy_recursion((0, 0)), delay=100, cell_size=50, rows=7, cols=7, seed=2)
