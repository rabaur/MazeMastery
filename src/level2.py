from mazemastery.api import *


def solve() -> None:
    while not has_minotaur():
        i, j = get_pos()
        new_pos = (i, j + 1)
        set_pos(new_pos)