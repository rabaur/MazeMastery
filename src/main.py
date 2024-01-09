from mazemastery.api import run
from level1 import solve as level1
from level2 import solve as level2
from level3 import solve as level3
from level4 import solve as level4
from level5 import solve as level5
from level6 import solve as level6

run(4, level5, delay=100, cell_size=50, rows=7, cols=8, seed=2)
