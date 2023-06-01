from mazemastery.api import *
from mazemastery.solver import Solver

def level1():
    while (not was_found()):
        i, j = get_pos()
        neighbor = (i, j + 1)
        set_pos(neighbor)


def level2():
    while (not was_found()):
        i, j = get_pos()
        neighbor = (i, j + 1)
        set_pos(neighbor)
        if has_minotaur(neighbor):
            found_minotaur()

def level3():
    while (not was_found()):
        put_blue_gem(get_pos())
        all_neighbors = get_neighbors(get_pos())
        neighbors = []
        for neighbor in all_neighbors:
            if not has_blue_gem(neighbor):
                neighbors.append(neighbor)
        neighbor = neighbors[0]
        set_pos(neighbor)
        if has_minotaur(neighbor):
            found_minotaur()

def level4():
    while (not was_found()):
        put_blue_gem(get_pos())
        all_neighbors = get_neighbors(get_pos())
        neighbors = []
        for neighbor in all_neighbors:
            if not has_blue_gem(neighbor):
                neighbors.append(neighbor)
        if neighbors == []:
            put_red_gem(get_pos())
            neighbors = []
            for neighbor in all_neighbors:
                if not has_red_gem(neighbor):
                    neighbors.append(neighbor)
        neighbor = neighbors[0]
        set_pos(neighbor)
        if has_minotaur(neighbor):
            found_minotaur()


def level5():
    while (not was_found()):
        put_blue_gem(get_pos())
        all_neighbors = get_neighbors(get_pos())
        neighbors = []
        for neighbor in all_neighbors:
            if not has_blue_gem(neighbor):
                neighbors.append(neighbor)
        if neighbors == []:
            put_red_gem(get_pos())
            neighbor = pop()
        else:
            push(get_pos())
            neighbor = neighbors[0]
        set_pos(neighbor)
        if has_minotaur(neighbor):
            found_minotaur()


def level6():
    put_blue_gem(get_pos())
    all_neighbors = get_neighbors(get_pos())

    for neighbor in all_neighbors:
        if not has_blue_gem(neighbor):
            old_pos = get_pos()
            if was_found(): return
            set_pos(neighbor)
            if has_minotaur(neighbor):
                found_minotaur()
            level6()
            put_red_gem(get_pos())
            set_pos(old_pos)

class MySolver(Solver):

    def solve(self):
        level5()

solver = MySolver(level=3, rows=10, cols=10, cell_size=100)
solver.run()
