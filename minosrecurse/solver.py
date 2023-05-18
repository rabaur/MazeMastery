class State:
    """
    State is a singleton class that holds the current state of the maze solver,
    e.g., the current positions of the player, the position of gems, etc. All
    functions that manipulate the state instantiate this class and modify its
    attributes. By doing so, we don't need to bind these state-changing methods
    to a single class (so no knowledge about OOP is required) and we don't 
    need to expose state as global variables (which could be imported and
    manipulated by the students directly).
    """

    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(
        self,
        maze,
        renderer,
        start_pos=(0, 0),
        minotaurus=(0, 0),
        blue_gem_coords=[],
        red_gem_coords=[],
        stack=[]
    ):
        self.__maze = maze
        self.__renderer = renderer
        self.__pos = start_pos
        self.__minotaurus = minotaurus
        self.__blue_gem_coords = blue_gem_coords
        self.__red_gem_coords = red_gem_coords
        self.__stack = stack
    
    @property
    def maze(self):
        return self.__maze

    @property
    def renderer(self):
        return self.__renderer

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, new):
        self.__pos = new
    
    @property
    def minotaurus(self):
        return self.__minotaurus

    @property
    def blue_gem_coords(self):
        return self.__blue_gem_coords

    @blue_gem_coords.setter
    def blue_gem_coords(self, new):
        self.__blue_gem_coords = new
    
    @property
    def red_gem_coords(self):
        return self.__red_gem_coords

    @red_gem_coords.setter
    def red_gem_coords(self, new):
        self.__red_gem_coords = new
    
    @property
    def stack(self):
        return self.__stack

    @stack.setter
    def stack(self, new):
        self.__stack = new

def move(new):
    state = State()
    if new not in state.maze[state.pos]:
        print("OUCH!")
        new = state.pos
    old = state.pos
    state.pos = new
    state.renderer.render(pos, old)


if __name__ == "__main__":
    state = State()
    print(state.pos)
    state.pos = (1, 1)
    print(state.pos)
