from minosrecurse.solver import *

def level1():
    while (not was_found()):
        i, j = pos()
        neighbor = (i, j + 1)
        move(neighbor)


def level2():
    while (not was_found()):
        i, j = pos()
        neighbor = (i, j + 1)
        move(neighbor)
        if neighbor == minotaur():
            found_minotaur()

def level3():
    while (not was_found()):
        put_blue_gem(pos())
        all_neighbors = get_neighbors(pos())
        neighbors = []
        for neighbor in all_neighbors:
            if not has_blue_gem(neighbor):
                neighbors.append(neighbor)
        neighbor = neighbors[0]
        move(neighbor)
        if neighbor == minotaur():
            found_minotaur()


def level4():
    while (not was_found()):
        put_blue_gem(pos())
        all_neighbors = get_neighbors(pos())
        neighbors = []
        for neighbor in all_neighbors:
            if not has_blue_gem(neighbor):
                neighbors.append(neighbor)
        if neighbors == []:
            put_red_gem(pos())
            neighbors = []
            for neighbor in all_neighbors:
                if not has_red_gem(neighbor):
                    neighbors.append(neighbor)
        neighbor = neighbors[0]
        move(neighbor)
        if neighbor == minotaur():
            found_minotaur()


def level5():
    while (not was_found()):
        put_blue_gem(pos())
        all_neighbors = get_neighbors(pos())
        neighbors = []
        for neighbor in all_neighbors:
            if not has_blue_gem(neighbor):
                neighbors.append(neighbor)
        if neighbors == []:
            put_red_gem(pos())
            neighbor = pop()
        else:
            push(pos())
            neighbor = neighbors[0]
        move(neighbor)
        if neighbor == minotaur():
            found_minotaur()


def level6():
    put_blue_gem(pos())
    put_blue_gem(pos())
    all_neighbors = get_neighbors(pos())

    for neighbor in all_neighbors:
        if not has_blue_gem(neighbor):
            old_pos = pos()
            if was_found(): return

            move(neighbor)
            if neighbor == minotaur():
                found_minotaur()
            level6()
            put_red_gem(pos())
            move(old_pos)

class MySolver(Solver):

    def solve(self):
        level6()

solver = MySolver(level=6, rows=10, cols=10, cell_size=20)
solver.run()
