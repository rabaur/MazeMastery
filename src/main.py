from mazemastery.api import *
from level1 import solve as level1
from level2 import solve as level2
from level3 import solve as level3
from level4 import solve as level4
from level5 import solve as level5
from level6 import solve as level6

run(1, level1, delay=100, cell_size=100, rows=7, cols=7, seed=2)
