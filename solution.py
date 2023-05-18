from minosrecurse.solver import Solver, pos, minotauros, move, put_blue_gem, has_red_gem, has_blue_gem, put_red_gem, found_minotaurus, was_found, get_neighbors, push, pop

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
        if neighbor == minotauros():
            found_minotaurus()

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
        if neighbor == minotauros():
            found_minotaurus()


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
        if neighbor == minotauros():
            found_minotaurus()


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
        if neighbor == minotauros():
            found_minotaurus()


def level6():
    put_blue_gem(pos)
    all_neighbors = get_neighbors(pos())

    for neighbor in all_neighbors:
        if not has_blue_gem(neighbor):
            old_pos = pos()
            if was_found(): return

            move(neighbor)
            if neighbor == minotauros():
                found_minotaurus()
            level6()
            put_red_gem(pos())
            move(old_pos)

class MySolver(Solver):

    def solve(self):
        level2()

solver = MySolver(level=5)
solver.solve()
