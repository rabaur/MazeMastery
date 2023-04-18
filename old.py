import math
from gturtle import *

def square(size, color):
    setFillColor(color)
    setPenColor(color)
    startPath()
    rt(90)
    repeat 4:
        fd(size)
        rt(90)
    lt(90)
    fillPath()

def draw_maze(
    graph,
    agent_pos,
    visited,
    cell_size,
    start_pos,
    end_pos,
    agent_color="SandyBrown",
    color="SlateGray",
    visited_color="CornFlowerBlue",
    visited_color_min = 0.5,
    grid_color="Silver",
    grid_width=2,
    wall_color="black",
    wall_width=None
):
    if not wall_width:
        wall_width = int(cell_size / 5)
    """
    Draws a maze-graph.
    """
    # Determine size of grid
    m = max([r for r, _ in graph]) + 1
    n = max([c for _, c in graph]) + 1
    
    # Sanity checks
    if ((agent_pos[0] < 0 or agent_pos[1] >= m) or (agent_pos[1] < 0 or agent_pos[1] >= n)):
        raise Exception("Agent position is outside of the maze! Something must be wrong.")
    
    # Draw cells.
    r_min = int(100 * visited_color_min)
    g_min = int(149 * visited_color_min)
    b_min = int(237 * visited_color_min)
    n_vis = float(len(visited))
    for i in range(m):
        for j in range(n):
            setPos(j * cell_size, i * -cell_size)
            if (i, j) in visited:
                index = visited.index((i, j))
                percent = index / n_vis * (1.0 - visited_color_min)
                square(cell_size, (int(r_min + percent * 100), int(g_min + percent * 149), int(b_min + percent * 237)))
            elif (i, j) == agent_pos:
                square(cell_size, agent_color)
            else:
                square(cell_size, color)
    
    # Draw boundaries.
    setPos(0, 0)
    setPenColor(grid_color)
    setPenWidth(grid_width)
    rt(90)
    
    # Rows
    for i in range(m + 1):
        setPos(0, i * -cell_size)
        fd(n * cell_size)
        bk(n * cell_size)
    
    setPos(0, 0)
    lt(90)
    
    # Columns
    for j in range(n + 1):
        setPos(j * cell_size, 0)
        bk(m * cell_size)
        fd(m * cell_size)
    
    # Draw inner walls: For each cell, check if there is a missing neighbor.
    # If so, draw a wall neighboring the two cells that are not neighbors.
    setPenColor(wall_color)
    setPenWidth(wall_width)
    for i in range(m):
        for j in range(n):
            node = (i, j)
            neighbors = graph[node]
            if (i - 1, j) not in neighbors:
                # Upper wall
                setPos(j * cell_size, i * -cell_size)
                rt(90)
                fd(cell_size)
                lt(90)
            if (i, j - 1) not in neighbors:
                # Left wall
                setPos(j * cell_size, i * -cell_size)
                bk(cell_size)
                fd(cell_size)
            if (i, j + 1) not in neighbors:
                # Right wall
                setPos((j + 1) * cell_size, i * -cell_size)
                bk(cell_size)
                fd(cell_size)
            if (i + 1, j) not in neighbors:
                # Lower wall
                setPos(j * cell_size, (i + 1) * -cell_size)
                rt(90)
                fd(cell_size)
                bk(cell_size)
                lt(90)
    # Draw start and end-positions.
    setPenColor("white")
    setFontSize(int(cell_size / 2))
    setPos(start_pos[1] * cell_size, start_pos[0] * -cell_size - 2 * cell_size / 3)
    label("Start")
    setPos(end_pos[1] * cell_size, end_pos[0] * -cell_size - 2 * cell_size / 3)
    label("End")

import random
from collections import deque

class maze:
    '''
    This is the main class to create maze.
    '''
    def __init__(self,rows=10,cols=10):
        '''
        rows--> No. of rows of the maze
        cols--> No. of columns of the maze
        Need to pass just the two arguments. The rest will be assigned automatically
        maze_map--> Will be set to a Dicationary. Keys will be cells and
                    values will be another dictionary with keys=['E','W','N','S'] for
                    East West North South and values will be 0 or 1. 0 means that 
                    direction(EWNS) is blocked. 1 means that direction is open.
        grid--> A list of all cells
        path--> Shortest path from start(bottom right) to goal(by default top left)
                It will be a dictionary
        _win,_cell_width,_canvas -->    _win and )canvas are for Tkinter window and canvas
                                        _cell_width is cell width calculated automatically
        _agents-->  A list of aganets on the maze
        markedCells-->  Will be used to mark some particular cell during
                        path trace by the agent.
        _
        '''
        self.rows=rows
        self.cols=cols
        self.maze_map={}
        self.grid=[]
        self.path={} 
        self._cell_width=50  
        self._win=None 
        self._canvas=None
        self._agents=[]
        self.markCells=[]
        self._grid=[]
        y=0
        for n in range(self.cols):
            x = 1
            y = 1+y
            for m in range(self.rows):
                self.grid.append((x,y))
                self.maze_map[x,y]={'E':0,'W':0,'N':0,'S':0}
                x = x + 1
    
    def _Open_East(self,x, y):
        '''
        To remove the East Wall of the cell
        '''
        self.maze_map[x,y]['E']=1
        if y+1<=self.cols:
            self.maze_map[x,y+1]['W']=1

    def _Open_West(self,x, y):
        self.maze_map[x,y]['W']=1
        if y-1>0:
            self.maze_map[x,y-1]['E']=1

    def _Open_North(self,x, y):
        self.maze_map[x,y]['N']=1
        if x-1>0:
            self.maze_map[x-1,y]['S']=1

    def _Open_South(self,x, y):
        self.maze_map[x,y]['S']=1
        if x+1<=self.rows:
            self.maze_map[x+1,y]['N']=1
    
    def CreateMaze(self,x=1,y=1,pattern=None,loopPercent=0):
        '''
        One very important function to create a Random Maze
        pattern-->  It can be 'v' for vertical or 'h' for horizontal
                    Just the visual look of the maze will be more vertical/horizontal
                    passages will be there.
        loopPercent-->  0 means there will be just one path from start to goal (perfect maze)
                        Higher value means there will be multiple paths (loops)
                        Higher the value (max 100) more will be the loops
        saveMaze--> To save the generated Maze as CSV file for future reference.
        loadMaze--> Provide the CSV file to generate a desried maze
        theme--> Dark or Light
        '''
        _stack=[]
        _closed=[]
        self._goal=(x,y)
        def blockedNeighbours(cell):
            '''
            To find the blocked neighbours of a cell
            '''
            n=[]
            for d in self.maze_map[cell].keys():
                if self.maze_map[cell][d]==0:
                    if d=='E' and (cell[0],cell[1]+1) in self.grid:
                        n.append((cell[0],cell[1]+1))
                    elif d=='W' and (cell[0],cell[1]-1) in self.grid:
                        n.append((cell[0],cell[1]-1))
                    elif d=='N' and (cell[0]-1,cell[1]) in self.grid:
                        n.append((cell[0]-1,cell[1]))
                    elif d=='S' and (cell[0]+1,cell[1]) in self.grid:
                        n.append((cell[0]+1,cell[1]))
            return n

        def removeWallinBetween(cell1,cell2):
            '''
            To remove wall in between two cells
            '''
            if cell1[0]==cell2[0]:
                if cell1[1]==cell2[1]+1:
                    self.maze_map[cell1]['W']=1
                    self.maze_map[cell2]['E']=1
                else:
                    self.maze_map[cell1]['E']=1
                    self.maze_map[cell2]['W']=1
            else:
                if cell1[0]==cell2[0]+1:
                    self.maze_map[cell1]['N']=1
                    self.maze_map[cell2]['S']=1
                else:
                    self.maze_map[cell1]['S']=1
                    self.maze_map[cell2]['N']=1

        def isCyclic(cell1,cell2):
            '''
            To avoid too much blank(clear) path.
            '''
            ans=False
            if cell1[0]==cell2[0]:
                if cell1[1]>cell2[1]: cell1,cell2=cell2,cell1
                if self.maze_map[cell1]['S']==1 and self.maze_map[cell2]['S']==1:
                    if (cell1[0]+1,cell1[1]) in self.grid and self.maze_map[(cell1[0]+1,cell1[1])]['E']==1:
                        ans= True
                if self.maze_map[cell1]['N']==1 and self.maze_map[cell2]['N']==1:
                    if (cell1[0]-1,cell1[1]) in self.grid and self.maze_map[(cell1[0]-1,cell1[1])]['E']==1:
                        ans= True
            else:
                if cell1[0]>cell2[0]: cell1,cell2=cell2,cell1
                if self.maze_map[cell1]['E']==1 and self.maze_map[cell2]['E']==1:
                    if (cell1[0],cell1[1]+1) in self.grid and self.maze_map[(cell1[0],cell1[1]+1)]['S']==1:
                        ans= True
                if self.maze_map[cell1]['W']==1 and self.maze_map[cell2]['W']==1:
                    if (cell1[0],cell1[1]-1) in self.grid and self.maze_map[(cell1[0],cell1[1]-1)]['S']==1:
                        ans= True
            return ans

        def BFS(cell):
            '''
            Breadth First Search
            To generate the shortest path.
            This will be used only when there are multiple paths (loopPercent>0) or
            Maze is loaded from a CSV file.
            If a perfect maze is generated and without the load file, this method will
            not be used since the Maze generation will calculate the path.
            '''
            frontier = deque()
            frontier.append(cell)
            path = {}
            visited = {(self.rows,self.cols)}
            while len(frontier) > 0:
                cell = frontier.popleft()
                if self.maze_map[cell]['W'] and (cell[0],cell[1]-1) not in visited:
                    nextCell = (cell[0],cell[1]-1)
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
                if self.maze_map[cell]['S'] and (cell[0]+1,cell[1]) not in visited:    
                    nextCell = (cell[0]+1,cell[1])
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
                if self.maze_map[cell]['E'] and (cell[0],cell[1]+1) not in visited:
                    nextCell = (cell[0],cell[1]+1)
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
                if self.maze_map[cell]['N'] and (cell[0]-1,cell[1]) not in visited:
                    nextCell = (cell[0]-1,cell[1])
                    path[nextCell] = cell
                    frontier.append(nextCell)
                    visited.add(nextCell)
            fwdPath={}
            cell=self._goal
            while cell!=(self.rows,self.cols):
                try:
                    fwdPath[path[cell]]=cell
                    cell=path[cell]
                except:
                    print('Path to goal not found!')
                    return
            return fwdPath

        # if maze is to be generated randomly
        _stack.append((x,y))
        _closed.append((x,y))
        biasLength=2 # if pattern is 'v' or 'h'
        if(pattern is not None and pattern.lower()=='h'):
            biasLength=max(self.cols//10,2)
        if(pattern is not None and pattern.lower()=='v'):
            biasLength=max(self.rows//10,2)
        bias=0

        while len(_stack) > 0:
            cell = []
            bias+=1

            # 
            if(x , y +1) not in _closed and (x , y+1) in self.grid:
                cell.append("E")
            if (x , y-1) not in _closed and (x , y-1) in self.grid:
                cell.append("W")
            if (x+1, y ) not in _closed and (x+1 , y ) in self.grid:
                cell.append("S")
            if (x-1, y ) not in _closed and (x-1 , y) in self.grid:
                cell.append("N") 
            if len(cell) > 0:    
                if pattern is not None and pattern.lower()=='h' and bias<=biasLength:
                    if('E' in cell or 'W' in cell):
                        if 'S' in cell:cell.remove('S')
                        if 'N' in cell:cell.remove('N')
                elif pattern is not None and pattern.lower()=='v' and bias<=biasLength:
                    if('N' in cell or 'S' in cell):
                        if 'E' in cell:cell.remove('E')
                        if 'W' in cell:cell.remove('W')
                else:
                    bias=0
                current_cell = (random.choice(cell))
                if current_cell == "E":
                    self._Open_East(x,y)
                    self.path[x, y+1] = x, y
                    y = y + 1
                    _closed.append((x, y))
                    _stack.append((x, y))

                elif current_cell == "W":
                    self._Open_West(x, y)
                    self.path[x , y-1] = x, y
                    y = y - 1
                    _closed.append((x, y))
                    _stack.append((x, y))

                elif current_cell == "N":
                    self._Open_North(x, y)
                    self.path[(x-1 , y)] = x, y
                    x = x - 1
                    _closed.append((x, y))
                    _stack.append((x, y))

                elif current_cell == "S":
                    self._Open_South(x, y)
                    self.path[(x+1 , y)] = x, y
                    x = x + 1
                    _closed.append((x, y))
                    _stack.append((x, y))

            else:
                x, y = _stack.pop()

        ## Multiple Path Loops
        if loopPercent!=0:
            
            x,y=self.rows,self.cols
            pathCells=[(x,y)]
            while x!=self.rows or y!=self.cols:
                x,y=self.path[(x,y)]
                pathCells.append((x,y))
            notPathCells=[i for i in self.grid if i not in pathCells]
            random.shuffle(pathCells)
            random.shuffle(notPathCells)
            pathLength=len(pathCells)
            notPathLength=len(notPathCells)
            count1,count2=pathLength/3*loopPercent/100,notPathLength/3*loopPercent/100
            
            #remove blocks from shortest path cells
            count=0
            i=0
            while count<count1: #these many blocks to remove
                if len(blockedNeighbours(pathCells[i]))>0:
                    cell=random.choice(blockedNeighbours(pathCells[i]))
                    if not isCyclic(cell,pathCells[i]):
                        removeWallinBetween(cell,pathCells[i])
                        count+=1
                    i+=1
                        
                else:
                    i+=1
                if i==len(pathCells):
                    break
            #remove blocks from outside shortest path cells
            if len(notPathCells)>0:
                count=0
                i=0
                while count<count2: #these many blocks to remove
                    if len(blockedNeighbours(notPathCells[i]))>0:
                        cell=random.choice(blockedNeighbours(notPathCells[i]))
                        if not isCyclic(cell,notPathCells[i]):
                            removeWallinBetween(cell,notPathCells[i])
                            count+=1
                        i+=1
                            
                    else:
                        i+=1
                    if i==len(notPathCells):
                        break
            self.path=BFS((self.rows,self.cols))

def pyamaze_walls_to_neighbors(m, n, row, col, wall_dict):
    neighbors = []
    row -= 1
    col -= 1
    for dir, val in wall_dict.items():
        if val == 1:
            if dir == 'E':
                if col + 1 < n: neighbors.append((row, col + 1))
            elif dir == 'N':
                if row - 1 >= 0: neighbors.append((row - 1, col))
            elif dir == 'S':
                if row + 1 < m: neighbors.append((row + 1, col))
            else:
                if col - 1 >= 0: neighbors.append((row, col - 1))
    return neighbors           

def pyamaze_to_graph(maze_dict):
    graph = {}
    m = max([r for r, _ in maze_dict])
    n = max([c for _, c in maze_dict])
    for (row, col), walls in maze_dict.items():
        graph[(row - 1, col - 1)] = pyamaze_walls_to_neighbors(m, n, row, col, walls)
    return graph

def create_maze(rows, cols, loopPercent):
    m = maze(rows, cols)
    m.CreateMaze(loopPercent=loopPercent)
    return pyamaze_to_graph(m.maze_map)

"""
-------------------------------------------------------------------------------------------------------------------
Programme ab hier!
-------------------------------------------------------------------------------------------------------------------
"""
# Ändere die Zahl zu einer anderen ganzen Zahl um das Labyrinth zu verändern
random.seed(0)

# Nr. Zeilen und Spalten
rows = 10
cols = 10

# Hier wird das Labyrinth erstellt.
graph = create_maze(rows, cols, 100)

# Kreiere die Turtle.
makeTurtle()
ht()
end_pos = (4, 4)

visited = [] # Global um pass-by reference and value verwirrung zu vermeiden

def DFS(current):
    global visited
    if end_pos in visited:
        return
    visited.append(current)
    
    # Nicht entfernen! ↓ 
    draw_maze(graph=graph, agent_pos=current, visited=visited, cell_size=30, start_pos=(0, 0), end_pos=end_pos)
    delay(1000) # Mache die Zahl grösser um längere Pausen zu haben.
    clear()
    # Nicht entfernen! ↑

    # Schreibe Dein Programm hier!
    neighbors = graph[current]
    for neighbor in neighbors:
        if neighbor not in visited:
            DFS(neighbor)

# Rufe hier DFS auf!
DFS((0, 0))
    