
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

    def __new__(
        cls,
        maze=None,
        renderer=None,
        start_pos=(0, 0),
        minotaur_coords=(0, 0),
        blue_gem_coords=[],
        red_gem_coords=[],
        stack=[],
        found=False,
        lives=5,
        *args,
        **kwargs
    ):
        if cls._self is None:
            cls._self = super(State, cls).__new__(cls, *args, **kwargs)
            cls._self.__maze = maze
            cls._self.__renderer = renderer
            cls._self.__pos = start_pos
            cls._self.__minotaur_coords = minotaur_coords
            cls._self.__blue_gem_coords = blue_gem_coords
            cls._self.__red_gem_coords = red_gem_coords
            cls._self.__stack = stack
            cls._self.__found = found
            cls._self.__lives = lives
        return cls._self

    def __init__(
        self,
        maze=None,
        renderer=None,
        start_pos=(0, 0),
        minotaur_coords=(0, 0),
        blue_gem_coords=[],
        red_gem_coords=[],
        stack=[],
        found=False,
        lives=5,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

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
    def minotaur_coords(self):
        return self.__minotaur_coords

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

    @property
    def found(self):
        return self.__found

    @found.setter
    def found(self, new):
        self.__found = new
    
    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, new):
        self.__lives = new