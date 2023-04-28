red_gem_coords = []
blue_gem_coords = []
minotaurus = (0, 0)

def put_blue_gem(cell):
    if cell not in blue_gem_coords:
        blue_gem_coords.append(cell)

def has_red_gem(cell):
    return cell in red_gem_coords

def has_blue_gem(cell):
    return cell in blue_gem_coords

def turn_gem_red(cell):
    if cell in blue_gem_coords:
        blue_gem_coords.remove(cell)
        red_gem_coords.append(cell)

def found_minotaurus():
    global found
    found = True

def was_found():
    return found

def get_neighbors(pos):
    ...

# Correct solution
def DFS(pos):
    if was_found():
        return
    if pos == minotaurus:
        found_minotaurus()
        return
    put_blue_gem(pos)
    neighbors = get_neighbors(pos)
    for neighbor in neighbors:
        if not has_blue_gem(neighbor) and not has_red_gem(neighbor):
            DFS(neighbor)
    turn_gem_red(pos)

# Abstieg 1: 
def DFS(pos):
    if was_found():
        return
    if pos == minotaurus:
        found_minotaurus()
        return
    put_blue_gem(pos)
    neighbors = get_neighbors(pos)
    for neighbor in neighbors:
        if not has_blue_gem(neighbor) and not has_red_gem(neighbor):
            DFS(neighbor)
    turn_gem_red(pos)