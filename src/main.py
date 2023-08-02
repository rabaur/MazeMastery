from mazemastery.api import *

def level1():
    while (is_searching()):
        i, j = get_pos()
        new_pos = (i, j + 1)
        set_pos(new_pos)

def level2():
    while (is_searching()):
        i, j = get_pos()
        new_pos = (i, j + 1)
        set_pos(new_pos)
        if has_minotaur(new_pos):
            stop()

def level3():
    while (is_searching()):
        put_blue_gem(get_pos())
        all_neighbors = get_neighbors(get_pos())
        for neighbor in all_neighbors:
            if not has_blue_gem(neighbor):
                new_pos = neighbor
        set_pos(new_pos)
        if has_minotaur(new_pos):
            stop()

def level4():
    while (is_searching()):
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
        new_pos = neighbors[0]
        set_pos(new_pos)
        if has_minotaur(new_pos):
            stop()


def level5():
    stack = [get_pos()]
    while (is_searching()):
        put_blue_gem(get_pos())
        all_neighbors = get_neighbors(get_pos())
        neighbors = []
        for neighbor in all_neighbors:
            if not has_blue_gem(neighbor):
                neighbors.append(neighbor)
        if neighbors == []:
            put_red_gem(get_pos())
            new_pos = stack.pop()
        else:
            stack.append(get_pos())
            new_pos = neighbors[0]
        set_pos(new_pos)
        if has_minotaur(new_pos):
            stop()


def level6():
    put_blue_gem(get_pos())
    all_neighbors = get_neighbors(get_pos())
    for neighbor in all_neighbors:
        if not has_blue_gem(neighbor):
            new_pos = neighbor
            old_pos = get_pos()
            if not is_searching(): return
            set_pos(new_pos)
            if has_minotaur(new_pos):
                stop()
            level6()
            put_red_gem(get_pos())
            set_pos(old_pos)

run(3, level3, delay=1000, cell_size=100, rows=5, cols=11)
