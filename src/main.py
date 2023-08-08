from mazemastery.api import *

def level1():
    while (not has_minotaur(get_pos())):
        i, j = get_pos()
        new_pos = (i, j + 1)
        set_pos(new_pos)


def level2():
    while (not has_minotaur(get_pos())):
        i, j = get_pos()
        new_pos = (i, j + 1)
        set_pos(new_pos)


def level3():
    while (not has_minotaur(get_pos())):
        put_blue_gem()
        for neighbor in get_neighbors():
            if not has_blue_gem(neighbor):
                new_pos = neighbor
                break
        set_pos(new_pos)


def level4():
    while (not has_minotaur(get_pos())):
        put_blue_gem()
        found_neighbor = False
        for neighbor in get_neighbors():
            if not has_blue_gem(neighbor):
                new_pos = neighbor
                found_neighbor = True
                break
        if not found_neighbor:
            put_red_gem()
            for neighbor in get_neighbors():
                if not has_red_gem(neighbor):
                    new_pos = neighbor
                    break
        set_pos(new_pos)


def level5():
    stack = [get_pos()]
    while (not has_minotaur(get_pos())):
        put_blue_gem()
        found_neighbor = False
        for neighbor in get_neighbors():
            if not has_blue_gem(neighbor):
                new_pos = neighbor
                found_neighbor = True
                break
        if not found_neighbor:
            put_red_gem()
            new_pos = stack.pop()
        else:
            stack.append(get_pos())
        set_pos(new_pos)


found_minotaur = False
def level6():
    global found_minotaur
    put_blue_gem()
    for neighbor in get_neighbors():
        if not has_blue_gem(neighbor):
            new_pos = neighbor
            old_pos = get_pos()
            if has_minotaur(get_pos()) or found_minotaur:
                found_minotaur = True
                return
            set_pos(new_pos)
            level6()
            put_red_gem()
            set_pos(old_pos)


run(5, level5, delay=100, cell_size=100, rows=11, cols=11)
