from mazemastery.api import (
    get_pos,
    set_pos,
    get_neighbors,
    has_minotaur,
    put_blue_gem,
    has_blue_gem,
    put_red_gem,
    has_red_gem
)


def level1() -> None:
    """Solves a horizontal corridor with the minotaur at the end."""
    while True:
        i, j = get_pos()
        new_pos = (i, j + 1)
        set_pos(new_pos)


def level2() -> None:
    """Solves a horizontal corridor with the minotaur at a random position."""
    while not has_minotaur():
        i, j = get_pos()
        new_pos = (i, j + 1)
        set_pos(new_pos)


def level3() -> None:
    """Solves a horizontal corridor with the minotaur at a random position."""
    while not has_minotaur():
        i, j = get_pos()
        new_pos = (i + 1, j)
        set_pos(new_pos)


def level4() -> None:
    """Solves a zigzig-like mike with the minotaur at the end"""
    steps = 0
    while not has_minotaur():
        i, j = get_pos()
        if steps % 2 == 0:
            new_pos = (i, j + 1)
        else:
            new_pos = (i + 1, j)
        set_pos(new_pos)
        steps += 1


def level5() -> None:
    """Solves a unicursal maze with the minotaur at a random position."""
    while not has_minotaur():
        put_blue_gem()
        for neighbor in get_neighbors():
            if not has_blue_gem(neighbor):
                new_pos = neighbor
                break
        set_pos(new_pos)


def level6() -> None:
    """
    Solves a perfect maze (no loops) with the minotaur at a random position.
    """
    while not has_minotaur():
        put_blue_gem()
        found_neighbor = False
        for neighbor in get_neighbors():
            if not has_blue_gem(neighbor):
                found_neighbor = True
                new_pos = neighbor
                break
        if not found_neighbor:
            put_red_gem()
            for neighbor in get_neighbors():
                if not has_red_gem(neighbor):
                    new_pos = neighbor
                    break
        set_pos(new_pos)


def level7() -> None:
    """
    Solves a general maze with the minotaur at a random position using a
    stack.
    """
    stack = [get_pos()]
    while not has_minotaur():
        put_blue_gem()
        found_neighbor = False
        for neighbor in get_neighbors():
            if not has_blue_gem(neighbor):
                found_neighbor = True
                new_pos = neighbor
                break
        if not found_neighbor:
            put_red_gem()
            new_pos = stack.pop()
        else:
            stack.append(get_pos())
        set_pos(new_pos)


found_minotaur = False


def level8() -> None:
    """
    Solves a general maze with the minotaur at a random position using
    recursion.
    """
    global found_minotaur
    put_blue_gem()
    for neighbor in get_neighbors():
        if not has_blue_gem(neighbor):
            new_pos = neighbor
            old_pos = get_pos()
            if has_minotaur() or found_minotaur:
                found_minotaur = True
                return
            set_pos(new_pos)
            level8()
            put_red_gem()
            set_pos(old_pos)
    return
