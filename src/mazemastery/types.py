from typing import TYPE_CHECKING, Literal

Coord = tuple[int, int]
Maze = dict[Coord, list[Coord]]
ColorDict = dict[int | Literal["main"], str]

# This avoid circular imports.
# See https://docs.python.org/3/library/typing.html#typing.TYPE_CHECKING
if TYPE_CHECKING:
    from mazemastery.renderer import Renderer as Renderer
else:
    Renderer = object
