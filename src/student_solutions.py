from mazemastery.api import *

# Participant 1 - Level 1 and 2
def level1and2():
 while(True):
  if(has_minotaur(get_pos())):
   pass
  else:
   n = get_neighbors(get_pos())
   for i in n:
    if has_minotaur(i):
     put_red_gem(get_pos())
     set_pos(i)
    if not has_red_gem(i):
     put_red_gem(i)
     set_pos(n[0])
     
# Participant 1 - Level 3
def level3():
 z = True
 while(z==True):
  if(has_minotaur(get_pos())):
   z = False
   pass
  else:
   n = get_neighbors(get_pos())
   for i in n:
    if has_minotaur(i):
     put_red_gem(get_pos())
     set_pos(i)
     z = False
    if not has_red_gem(i):
     put_red_gem(i)
     set_pos(i) 

# Participant 2 - Level 1
def level1():
 i,j = get_pos()
 set_pos((i,j))
 for x in range(0,9):
  j = i+1
  set_pos((i,j)) 

# Participant 2 - Level 2
def level2():
 i,j = get_pos()
 set_pos((i,j))
 while not has_minotaur():
  j = i+1
  set_pos((i,j)) 

# Participant 3 - Level 1 and 2
def level1and2():
 while not has_minotaur(get_pos()):
  neigh = get_neighbors(get_pos())
  for i in neigh:
   if i[1]>get_pos()[1]:
    set_pos(i) 

# Participant 3 - Level 3
def level2():
 while not has_minotaur(get_pos()):
  neigh = get_neighbors(get_pos())
  put_blue_gem(get_pos())
  for i in neigh:
   if not has_blue_gem(i):
    set_pos(i) 

# Participant 4 - Level 1 and 2
def level1():
    j = 0
    while(True):
        j+=1
        set_pos(0,j) 

# Participant 4 - Level 1 and 2
def level1():
    j = 0
    while(True):
        j+=1
        set_pos(0,j)

# Participant 4 - Level 3
def solve():
    visited = set()
    visited.add(get_pos())
    if has_minotaur(get_pos()):
        return
    queue = get_neighbors(get_pos())
    i = 0
    while queue:
        top = queue.pop()
        if top in visited:
            continue
        set_pos(top)
        visited.add(top)
        if has_minotaur(get_pos()):
            break
        neighbours = get_neighbors(get_pos())
        queue.extend(neighbours)
        i += 1