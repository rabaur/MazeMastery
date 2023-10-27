from typing import Any

from mazemastery.types import Coord, Maze, Renderer


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

    # Type declarations where mypy can't figure it out on its own
    __maze: Maze
    __renderer: Renderer
    __minotaur_coords: Coord

    def __new__(
        cls,
        maze: Maze | None=None,
        renderer: Renderer | None=None,
        start_pos: Coord=(0, 0),
        minotaur_coords: Coord=(0, 0),
        blue_gem_coords: list[Coord]=[],
        red_gem_coords: list[Coord]=[],
        stack: list[Coord]=[],
        found: bool=False,
        initial_lives: int=5,
        dead: bool=False,
        level: int=1,
        *args: Any,
        **kwargs: Any,
    ) -> "State":
        if cls._self is None:
            if maze is None or renderer is None:
                raise RuntimeError("First state must be initialized with a maze and a renderer")
            cls._self = super(State, cls).__new__(cls, *args, **kwargs)
            cls._self.__maze = maze
            cls._self.__renderer = renderer
            cls._self.__pos = start_pos
            cls._self.__minotaur_coords = minotaur_coords
            cls._self.__blue_gem_coords = blue_gem_coords
            cls._self.__red_gem_coords = red_gem_coords
            cls._self.__stack = stack
            cls._self.__found = found
            cls._self.__initial_lives = initial_lives
            cls._self.__lives = initial_lives
            cls._self.__dead = dead
            cls._self.__level = level
        return cls._self

    def __init__(
        self,
        maze: Maze | None=None,
        renderer: Renderer | None=None,
        start_pos: Coord=(0, 0),
        minotaur_coords: Coord=(0, 0),
        blue_gem_coords: list[Coord]=[],
        red_gem_coords: list[Coord]=[],
        stack: list[Coord]=[],
        found: bool=False,
        initial_lives: int=5,
        dead: bool=False,
        level: int=1,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)

    @property
    def maze(self) -> Maze:
        return self.__maze

    @property
    def renderer(self) -> Renderer:
        return self.__renderer

    @property
    def pos(self) -> Coord:
        return self.__pos

    @pos.setter
    def pos(self, new: Coord) -> None:
        self.__pos = new

    @property
    def minotaur_coords(self) -> Coord:
        return self.__minotaur_coords

    @property
    def blue_gem_coords(self) -> list[Coord]:
        return self.__blue_gem_coords

    @blue_gem_coords.setter
    def blue_gem_coords(self, new: list[Coord]) -> None:
        self.__blue_gem_coords = new

    @property
    def red_gem_coords(self) -> list[Coord]:
        return self.__red_gem_coords

    @red_gem_coords.setter
    def red_gem_coords(self, new: list[Coord]) -> None:
        self.__red_gem_coords = new

    @property
    def stack(self) -> list[Coord]:
        return self.__stack

    @stack.setter
    def stack(self, new: list[Coord]) -> None:
        self.__stack = new

    @property
    def found(self) -> bool:
        return self.__found

    @found.setter
    def found(self, new: bool) -> None:
        self.__found = new

    @property
    def lives(self) -> int:
        return self.__lives

    @lives.setter
    def lives(self, new: int) -> None:
        self.__lives = new

    @property
    def initial_lives(self) -> int:
        return self.__initial_lives

    @initial_lives.setter
    def initial_lives(self, new: int) -> None:
        self.__initial_lives = new

    @property
    def dead(self) -> bool:
        return self.__dead

    @dead.setter
    def dead(self, new: bool) -> None:
        self.__dead = new

    @property
    def level(self) -> int:
        return self.__level
    
    @level.setter
    def level(self, new: int) -> None:
        self.__level = new
