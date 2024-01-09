import math
import os
import random
import tkinter as tk
from typing import Dict, List, Tuple

from PIL import Image, ImageTk  # type: ignore

from mazemastery.debug_menu import DebugMenu
from mazemastery.maze import get_maze_size
from mazemastery.styles import Colors
from mazemastery.types import ColorDict, Coord


class Renderer:
    def __init__(
        self,
        maze: Dict[Tuple[int, int], List[Tuple[int, int]]],
        minotaur_coords: Tuple[int, int],
        cell_size: int = 50,
        grid_width: int | None = None,
        gem_size: int | None = None,
        minotaur_size: int | None = None,
        delay: int = 100,
        offset_rows: int = 2,
        offset_cols: int = 1,
        initial_pos: Tuple[int, int] = (0, 0),
        initial_lives: int = 5
    ):
        """
        A class for rendering a maze.

        Args:
            maze: Graph representing the maze.
            minotaur_coords: Coordinates of the minotaur.
            cell_size: Size cell-side in pixels.
            grid_width: Width of the grid lines in pixels.
            gem_size: Size of the gems in pixels.
            minotaur_size: Size of the minotaur in pixels.
            delay: Delay between frames in milliseconds.
            offset_rows: Number of rows to offset the maze by to add space on
                top of the maze.
            offset_cols: Number of columns to offset the maze by to add space
                on the left of the maze.
        """
        self.maze = maze
        self.minotaur_coords = minotaur_coords
        self.cell_size = cell_size
        self.grid_width = grid_width if grid_width else cell_size // 20
        self.offset_rows = offset_rows
        self.offset_cols = offset_cols
        self.delay = delay
        self.m, self.n = get_maze_size(maze)
        self.initial_lives = initial_lives

        # Derived sizes
        self.wall_width = self.cell_size // 10
        self.gem_size = gem_size if gem_size else cell_size // 2
        self.minotaur_size = minotaur_size if minotaur_size else cell_size // 2
        self.gem_third = self.gem_size // 3
        self.gem_sixth = self.gem_size // 6
        self.cell_third = self.cell_size // 3
        self.shadow_offset = self.cell_size // 3
        self.maze_extents = [
            self.offset_cols * self.cell_size,
            self.offset_rows * self.cell_size,
            (self.n + self.offset_cols) * self.cell_size,
            (self.m + self.offset_rows) * self.cell_size,
        ]

        # Whether the renderer is in debug mode
        self.debug = False

        # Buffers tracking changes of state, such that we do not need to redraw
        # all items on every update_draw call.
        self.blue_gem_buffer: set[Coord] = set()
        self.red_gem_buffer: set[Coord] = set()
        self.initial_pos = initial_pos

        # Canvas to draw on
        self.root = tk.Tk()
        self.root.title("Maze")

        self.canvas = tk.Canvas(
            self.root,
            width=(self.n + self.offset_cols + 1) * cell_size,
            height=(self.m + self.offset_rows + 1) * cell_size
        )
        self.debug_menu = DebugMenu(self)
        self.canvas.grid(row=0, column=0, rowspan=len(self.debug_menu.api_buttons) + len(self.debug_menu.state_labels) + self.offset_rows + 2 + 2)
        self.canvas.configure(bg=Colors.brown_highlight)
        self.root.configure(bg=Colors.brown_highlight)

        # For sprites
        self.sprites: dict = {}
        self.sprite_path = os.path.join(os.path.dirname(__file__), os.path.join("sprites"))

    def initial_draw(self) -> None:
        """
        Draws components of the maze that will remain unchanged throughout the
        game.
        """
        self.debug_menu.update_menu()
        self.draw_maze()
        self.draw_hearts(num=self.initial_lives, filled=self.initial_lives)
        self.draw_minotaur()
        self.draw_player(self.initial_pos, self.initial_pos)
        self.draw_initial_row_col_numbers()

    def update_draw(self, old_pos: Coord, curr_pos: Coord, lives: int) -> None:
        """
        Draws components of the maze that will change throughout the game.
        Should be called after every move. Will clear buffers.
        """
        # self.draw_path_segment(old_pos, curr_pos)
        self.draw_row_col_numbers(old_pos, curr_pos)
        self.draw_gems()
        self.draw_player(old_pos, curr_pos)
        self.draw_hearts(num=self.initial_lives, filled=lives)
        self.canvas.update()
        self.red_gem_buffer = set()
        self.blue_gem_buffer = set()

    def draw_wall(self, start_x: int, start_y: int, end_x: int, end_y: int, wall_width: int, wall_color: str) -> None:
        self.canvas.create_line( # type: ignore
            start_x,
            start_y,
            end_x,
            end_y,
            width=wall_width,
            fill=wall_color,
            tag="wall",
            capstyle=tk.ROUND,
        )

    def draw_walls(self, wall_width: int, wall_color: str) -> None:
        for i in range(self.m):
            for j in range(self.n):
                off_i = i + self.offset_rows
                off_j = j + self.offset_cols
                if not (i - 1, j) in self.maze[(i, j)]:  # Northern neighbor missing
                    self.draw_wall(
                        start_x=off_j * self.cell_size,
                        start_y=off_i * self.cell_size,
                        end_x=(off_j + 1) * self.cell_size,
                        end_y=off_i * self.cell_size,
                        wall_width=wall_width,
                        wall_color=wall_color,
                    )
                if not (i, j - 1) in self.maze[(i, j)]:  # Western neighbor missing
                    self.draw_wall(
                        start_x=off_j * self.cell_size,
                        start_y=off_i * self.cell_size,
                        end_x=off_j * self.cell_size,
                        end_y=(off_i + 1) * self.cell_size,
                        wall_width=wall_width,
                        wall_color=wall_color,
                    )
                if not (i, j + 1) in self.maze[(i, j)]:  # Eastern neighbor missing
                    self.draw_wall(
                        start_x=(off_j + 1) * self.cell_size,
                        start_y=off_i * self.cell_size,
                        end_x=(off_j + 1) * self.cell_size,
                        end_y=(off_i + 1) * self.cell_size,
                        wall_width=wall_width,
                        wall_color=wall_color,
                    )
                if not (i + 1, j) in self.maze[(i, j)]:  # Southern neighbor missing
                    self.draw_wall(
                        start_x=off_j * self.cell_size,
                        start_y=(off_i + 1) * self.cell_size,
                        end_x=(off_j + 1) * self.cell_size,
                        end_y=(off_i + 1) * self.cell_size,
                        wall_width=wall_width,
                        wall_color=wall_color,
                    )

    def draw_wall_shadows(self) -> None:
        for i in range(self.m):
            for j in range(self.n):
                off_i = i + self.offset_rows
                off_j = j + self.offset_cols
                if not (i - 1, j) in self.maze[(i, j)]:  # Horizontal shadow
                    # If there is a wall to the left, we need to adjust
                    # the shadow to the left because of the thickness of the
                    # wall
                    if (i, j - 1) not in self.maze[(i, j)]:
                        left_x = off_j * self.cell_size
                    else:
                        left_x = off_j * self.cell_size - 2 * self.wall_width

                    # If there is a wall to the right, we need to clip the shadow to avoid bleeding beyong the wall
                    if (i, j + 1) not in self.maze[(i, j)]:
                        right_x = (off_j + 1) * self.cell_size
                    else:
                        right_x = (off_j + 1) * self.cell_size + self.shadow_offset
                    self.canvas.create_polygon( # type: ignore
                        left_x,
                        off_i * self.cell_size,
                        (off_j + 1) * self.cell_size,
                        off_i * self.cell_size
                        - 2 * self.wall_width,  # compensating for wall-width
                        right_x,
                        off_i * self.cell_size,
                        right_x,
                        off_i * self.cell_size + self.shadow_offset,
                        left_x + self.shadow_offset,
                        off_i * self.cell_size + self.shadow_offset,
                        fill=Colors.brown_border,
                        tag="shadow",
                    )

                if not (i, j - 1) in self.maze[(i, j)]:  # Vertical shadow
                    # If there is no wall to the top, we need to adjust the
                    # shadow to the top because of the tickness of the wall
                    if (i - 1, j) not in self.maze[(i, j)]:
                        top_y = off_i * self.cell_size
                    else:
                        top_y = off_i * self.cell_size - 2 * self.wall_width

                    # If there is a wall below, we need to clip the shadow to
                    # avoid bleeding beyong the wall
                    if (i + 1, j) not in self.maze[(i, j)]:
                        bottom_y = (off_i + 1) * self.cell_size
                    else:
                        bottom_y = (off_i + 1) * self.cell_size + self.shadow_offset
                    self.canvas.create_polygon( # type: ignore
                        off_j * self.cell_size,
                        top_y,
                        off_j * self.cell_size + self.shadow_offset,
                        top_y + self.shadow_offset,
                        off_j * self.cell_size + self.shadow_offset,
                        bottom_y,
                        off_j * self.cell_size,
                        bottom_y,
                        off_j * self.cell_size - 2 * self.wall_width,
                        (off_i + 1) * self.cell_size,
                        fill=Colors.brown_border,
                        tag="shadow",
                    )

    def draw_grid(self) -> None:

        # Horizontal lines
        for i in range(self.offset_rows, self.m + self.offset_rows):
            self.canvas.create_line( # type: ignore
                self.offset_cols + self.cell_size,
                i * self.cell_size,
                (self.n + self.offset_cols) * self.cell_size,
                i * self.cell_size,
                width=self.grid_width,
                fill=Colors.brown_border,
                tag="grid",
            )
        
        # Vertical lines
        for j in range(self.n + self.offset_cols):
            self.canvas.create_line( # type: ignore
                j * self.cell_size,
                self.offset_rows * self.cell_size,
                j * self.cell_size,
                (self.m + self.offset_rows) * self.cell_size,
                width=self.grid_width,
                fill=Colors.brown_border,
                tag="grid",
            )

    def draw_gem(self, pos: Coord, gem_size: int, color: ColorDict) -> None:
        """
        Draws a fancy gem at in the cell (i, j).
        """
        # Random position in the cell (i, j)
        i, j = pos
        offset = (self.cell_size - gem_size) // 2
        base_x = (j + self.offset_cols) * self.cell_size + offset
        base_y = (i + self.offset_rows) * self.cell_size + offset
        x = [base_x + i * self.gem_third for i in range(4)]
        y = list(reversed([base_y + i * self.gem_third for i in range(4)]))

        # Shadow
        self.canvas.create_oval(
            x[0] + self.gem_sixth,
            y[1],
            x[3] + self.gem_sixth,
            y[0] + self.gem_sixth,
            fill=Colors.brown_border,
            outline="",
        )

        # Full gem
        self.canvas.create_polygon(
            x[0], y[1],
            x[0], y[2],
            x[1], y[3],
            x[2], y[3],
            x[3], y[2],
            x[3], y[1],
            x[2], y[0],
            x[1], y[0],
            fill=color[0],
            width=2,
        )

        # Middle
        self.canvas.create_polygon(
            x[1], y[1],
            x[1], y[2],
            x[2], y[2],
            x[2], y[1],
            fill=color["main"],
            outline=color[1],
            width=2,
        )

        # Shine
        self.canvas.create_polygon(
            x[1], y[1],
            x[1], y[1] - self.gem_sixth,
            x[1] + self.gem_sixth, y[2],
            x[2], y[2],
            fill=color[3],
            outline="",
        )

        # Color 1
        self.canvas.create_polygon(
            x[2], y[0],
            x[1], y[0],
            x[1], y[1],
            x[2], y[1],
            fill=color[1],
            outline=color[0],
            width=2,
        )
        self.canvas.create_polygon(
            x[2], y[1],
            x[2], y[2],
            x[3], y[2],
            x[3], y[1],
            fill=color[1],
            outline=color[0],
            width=2,
        )

        # Color 2
        self.canvas.create_polygon(
            x[1], y[0], x[0], y[1], x[1], y[1], fill=color[2], outline=color[1]
        )
        self.canvas.create_polygon(
            x[2], y[2],
            x[2], y[3],
            x[3], y[2],
            fill=color[2],
            outline=color[1],
            width=2,
        )

        # Color 3
        self.canvas.create_polygon(
            x[1], y[1],
            x[0], y[1],
            x[0], y[2],
            x[1], y[2],
            fill=color[3],
            outline=color[1],
            width=2,
        )

        # Color 4
        self.canvas.create_polygon(
            x[1], y[1],
            x[0], y[1],
            x[0], y[2],
            x[1], y[2],
            fill=color[3],
            outline=color[1],
            width=2,
        )
        self.canvas.create_polygon(
            x[1], y[2],
            x[1], y[3],
            x[2], y[3],
            x[2], y[2],
            fill=color[3],
            outline=color[0],
            width=2,
        )

        # Color 5
        self.canvas.create_polygon(
            x[1], y[2],
            x[0], y[2],
            x[1], y[3],
            fill=color[4],
            outline=color[1],
            width=2,
        )

    def draw_grass_blades(self, pos: Coord, num_grass: int=3, num_blades: int=4) -> None:
        """
        Draws some weeds at a random position in the cell (i, j).
        """
        max_height = self.cell_size // 2
        min_height = self.cell_size // 4
        blade_width = int(math.ceil(self.cell_size / 20))

        # num_blades should be chosen so that num_blades * 2 * blade_width < cell_size
        num_blades = min(num_blades, self.cell_size // (2 * blade_width))

        # Random position in the cell (i, j)
        k, j = pos

        # Generate positions before drawing to potentially change drawing order
        base_positions = []
        for _ in range(num_grass):
            x = (j + self.offset_cols) * self.cell_size + random.randint(
                0, self.cell_size - num_blades * 2 * blade_width
            )
            y = (k + self.offset_rows) * self.cell_size + random.randint(
                0, self.cell_size
            )
            base_positions.append((x, y))

        # Order positions lexicographically by x, then y
        base_positions.sort(key=lambda pos: (pos[0], pos[1]))

        for x, y in base_positions:
            for k in range(num_blades):
                blade_height = random.randint(min_height, max_height)
                blade_x = x + k * 2 * blade_width

                # Shadow
                shadow_offset_x = (
                    min(
                        blade_x + self.shadow_offset * blade_height / max_height,
                        self.maze_extents[2],
                    )
                    - blade_x
                )
                shadow_offset_y = (
                    min(
                        y + self.shadow_offset * blade_height / max_height,
                        self.maze_extents[3],
                    )
                    - y
                )
                shadow_offset = min(shadow_offset_x, shadow_offset_y)
                self.canvas.create_line( # type: ignore
                    blade_x,
                    y,
                    # Make shadow offset proportional to blade height
                    blade_x + shadow_offset,
                    y + shadow_offset,
                    width=blade_width,
                    fill=Colors.green_border,
                    tag="grass_blade",
                )

                self.canvas.create_rectangle( # type: ignore
                    blade_x,
                    y,
                    blade_x + blade_width,
                    y - blade_height,
                    fill=Colors.grass_base,
                    outline="",
                    tag="grass_blade",
                )

                # Small highlight
                self.canvas.create_rectangle( # type: ignore
                    blade_x,
                    y - blade_height + blade_width,
                    blade_x + blade_width,
                    y - blade_height,
                    fill=Colors.grass_top,
                    outline="",
                    tag="grass_blade",
                )

    def draw_grass(self) -> None:
        """
        Instead of rendering empty cells with four walls in case a cell is not
        connnected to the maze, we render it as a path of grass.
        """
        for i in range(self.m):
            for j in range(self.n):
                if self.maze[(i, j)] != []:
                    continue
                off_i = i + self.offset_rows
                off_j = j + self.offset_cols
                self.canvas.create_rectangle( # type: ignore
                    off_j * self.cell_size,
                    off_i * self.cell_size,
                    (off_j + 1) * self.cell_size,
                    (off_i + 1) * self.cell_size,
                    fill=Colors.green_base,
                    outline="",
                    tag="cell",
                )
        for i in range(self.m):
            for j in range(self.n):
                if self.maze[(i, j)] == []:
                    self.draw_grass_blades((i, j))

    def draw_maze(self) -> None:
        """
        Render a maze using tkinter.
        """
        self.draw_cells(Colors.brown_base)
        self.draw_grid()

        # Creating illusion of thick walls by overlaying multiple walls
        self.draw_walls(self.wall_width * 4, Colors.brown_border)
        self.draw_wall_shadows()
        self.draw_walls(self.wall_width * 3, Colors.brown_base)
        self.draw_walls(self.wall_width * 2, Colors.green_border)
        self.draw_walls(self.wall_width, Colors.green_base)

        # Cover empty cells.
        self.draw_grass()

    def draw_player(self, prev_pos: Tuple[int, int], curr_pos : Tuple[int, int]) -> None:
        """
        Render the player.

        Args:
            prev_pos: Previous position of the player. Is needed to compute the
                direction of the movement of the player to render the correct 
                sprite.
            curr_pos: The position the player should be rendered at.
        
        Returns:
            None
        """
        self.canvas.delete("player")
        i, j = curr_pos
        i += self.offset_rows
        j += self.offset_cols

        # Shadow
        self.canvas.create_oval( # type: ignore
            j * self.cell_size + self.cell_size // 3,
            i * self.cell_size + 2 * self.cell_size // 3,
            j * self.cell_size + 4 * self.cell_size // 5,
            i * self.cell_size + 4 * self.cell_size // 5,
            fill=Colors.brown_border,
            outline="",
            tag="player",
        )

        file_name = ""
        if prev_pos[0] < curr_pos[0]:
            file_name = "warrior_down.png"
        elif prev_pos[0] > curr_pos[0]:
            file_name = "warrior_up.png"
        elif prev_pos[1] < curr_pos[1]:
            file_name = "warrior_right.png"
        else:
            file_name = "warrior_left.png"

        self.draw_sprite(file_name, self.cell_size, i, j, "player", use_offset=False, dy=-self.cell_size // 4)

    def draw_pebble(self, pos: Coord) -> None:
        i, j = pos
        x = random.randint(j * self.cell_size, (j + 1) * self.cell_size)
        y = random.randint(i * self.cell_size, (i + 1) * self.cell_size)

        # Draw pebble.
        max_size = self.cell_size // 8
        min_size = self.cell_size // 16
        size = random.randint(min_size, max_size)

        # Base
        self.canvas.create_rectangle( # type: ignore
            x,
            y,
            x + size,
            y + size,
            fill=Colors.brown_border,
            outline="",
            tag="cell",
        )

        # Highlight
        self.canvas.create_rectangle( # type: ignore
            x + 2,
            y + 2,
            x + size // 3 * 2,
            y + size // 3 * 2,
            fill=Colors.brown_highlight,
            outline="",
            tag="cell",
        )

    def draw_cells(self, cell_color: str, pebble_count: int = 10) -> None:
        """
        Render the cells using tkinter.
        """
        for i in range(self.m):
            for j in range(self.n):
                off_i = i + self.offset_rows
                off_j = j + self.offset_cols
                self.canvas.create_rectangle( # type: ignore
                    off_j * self.cell_size,
                    off_i * self.cell_size,
                    (off_j + 1) * self.cell_size,
                    (off_i + 1) * self.cell_size,
                    fill=cell_color,
                    outline="",
                    tag="cell",
                )
                # Draw random pebbles
                for _ in range(pebble_count):
                    self.draw_pebble((off_i, off_j))

    def draw_gems(self) -> None:
        """
        Render gems using tkinter.
        """
        for i, j in self.blue_gem_buffer:
            self.draw_gem((i, j), self.cell_size // 2, Colors.blues)

        for i, j in self.red_gem_buffer:
            self.draw_gem((i, j), self.cell_size // 2, Colors.reds)

    def draw_minotaur(self) -> None:
        """
        Render minotaur using tkinter.
        """
        self.canvas.delete("minotaur")
        i, j = self.minotaur_coords
        i += self.offset_rows
        j += self.offset_cols

        # Shadow
        self.canvas.create_oval(
            j * self.cell_size + self.cell_size // 3,
            i * self.cell_size + 2 * self.cell_size // 3,
            j * self.cell_size + 4 * self.cell_size // 5,
            i * self.cell_size + 4 * self.cell_size // 5,
            fill=Colors.brown_border,
            outline="",
        )

        self.draw_sprite("minotaur.png", self.cell_size, i, j, "minotaur", use_offset=False, dy=-self.cell_size // 4)

    def draw_path_segment(self, source: Coord, target: Coord) -> None:
        self.canvas.create_line( # type: ignore
            (source[1] + self.offset_cols) * self.cell_size + self.cell_size // 2,
            (source[0] + self.offset_rows) * self.cell_size + self.cell_size // 2,
            (target[1] + self.offset_cols) * self.cell_size + self.cell_size // 2,
            (target[0] + self.offset_rows) * self.cell_size + self.cell_size // 2,
            fill="green",
            width=5,
            tag="path",
        )

    def draw_initial_row_col_numbers(self, font_size: int | None = None) -> None:
        if font_size is None:
            font_size = self.cell_size // 4
        for i in range(self.m):
            self.canvas.create_text( # type: ignore
                (self.offset_cols - 0.5) * self.cell_size,
                (i + self.offset_rows + 0.5) * self.cell_size,
                text=str(i),
                font=f"Arial {font_size} {'bold' if self.initial_pos[0] == i else ''}",
                fill=Colors.blues[1] if self.initial_pos[0] == i else "white",
                anchor="e",
                tag=f"row_number_{i}",
            )
        for j in range(self.n):
            self.canvas.create_text( # type: ignore
                (j + self.offset_cols + 0.5) * self.cell_size,
                (self.offset_rows - 2 / 3) * self.cell_size,
                text=str(j),
                font=f"Arial {font_size} {'bold' if self.initial_pos[1] == j else ''}",
                fill=Colors.blues[1] if self.initial_pos[1] == j else "white",
                anchor="n",
                tag=f"col_number_{j}",
            )

    def draw_row_col_numbers(self, old_pos: Coord, pos: Coord, font_size: int | None=None) -> None:
        if font_size is None:
            font_size = self.cell_size // 4
        self.canvas.delete("number")  # delete old numbers
        if old_pos[0] != pos[0]:  # row number changed, update required
            self.canvas.delete(f"row_number_{old_pos[0]}")
            self.canvas.delete(f"row_number_{pos[0]}")
            self.canvas.create_text( # type: ignore
                (self.offset_cols - 0.5) * self.cell_size,
                (old_pos[0] + self.offset_rows + 0.5) * self.cell_size,
                text=str(old_pos[0]),
                font=f"Arial {font_size}",
                fill="white",
                anchor="e",
                tag=f"row_number_{old_pos[0]}",
            )
            self.canvas.create_text( # type: ignore
                (self.offset_cols - 0.5) * self.cell_size,
                (pos[0] + self.offset_rows + 0.5) * self.cell_size,
                text=str(pos[0]),
                font=f"Arial {font_size} bold",
                fill=Colors.blues[1],
                anchor="e",
                tag=f"row_number_{pos[0]}",
            )
        if old_pos[1] != pos[1]:  # col number changed, update required
            self.canvas.delete(f"col_number_{old_pos[1]}")
            self.canvas.delete(f"col_number_{pos[1]}")
            self.canvas.create_text( # type: ignore
                (old_pos[1] + self.offset_cols + 0.5) * self.cell_size,
                (self.offset_rows - 2 / 3) * self.cell_size,
                text=str(old_pos[1]),
                font=f"Arial {font_size}",
                fill="white",
                anchor="n",
                tag=f"col_number_{old_pos[1]}",
            )
            self.canvas.create_text( # type: ignore
                (pos[1] + self.offset_cols + 0.5) * self.cell_size,
                (self.offset_rows - 2 / 3) * self.cell_size,
                text=str(pos[1]),
                font=f"Arial {font_size} bold",
                fill=Colors.blues[1],
                anchor="n",
                tag=f"col_number_{pos[1]}",
            )
    
    def draw_hearts(self, num: int=5, filled: int=3, border_width: int | None=None, heart_size: int | None=None) -> None:
        """
        Draws 'num' hearts, 'filled' of which are filled in. Hearts are placed
        on the first row of the canvas and grow from right to left.
        """
        if border_width is None:
            border_width = self.cell_size // 20
        if heart_size is None:
            heart_size = self.cell_size // 4
        self.canvas.delete("heart") 
        for i in range(num):

            # Heart shadow
            self.draw_heart(
                x=(self.offset_cols + (self.n - 1 - i)) * self.cell_size + self.cell_size // 2 + self.cell_size // 10,
                y=self.cell_size // 2 + self.cell_size // 10,
                size=heart_size,
                color=Colors.brown_border
            )

            # Draw an outer heart a bit larger than the inner one
            self.draw_heart(
                x=(self.offset_cols + (self.n - 1 - i)) * self.cell_size + self.cell_size // 2,
                y=self.cell_size // 2,
                size=heart_size,
                color=Colors.reds[0]
            )

            # Draw an inner heart - if we are larger than filled, we draw a greyed out heart.
            self.draw_heart(
                x=(self.offset_cols + (self.n - 1 - i)) * self.cell_size + self.cell_size // 2,
                y=self.cell_size // 2 - border_width,
                size=heart_size- border_width,
                color=Colors.reds[1] if i < filled else Colors.reds[-1],
                highlight=i < filled,
                highlight_color=Colors.reds[3]
            )

    def draw_heart(
        self,
        x: int,
        y: int,
        size: int,
        highlight: bool = False,
        highlight_color: str = "white",
        color: str = "red"
    ) -> None:
        """
        Draws a heart (vertical) whose tip is at (x, y). Size is the side
        length of the square that forms the bottom of the heart.
        """

        # Tip
        cat = size / math.sqrt(2)
        self.canvas.create_polygon( # type: ignore
            x, y,
            x - cat, y - cat,
            x, y - 2 * cat,
            x + cat, y - cat,
            fill=color,
            tag="heart",
            outline=""
        )

        # Right part
        r = size / 2
        cx = x + cat / 2
        cy = y - 3 / 2 * cat
        self.canvas.create_oval( # type: ignore
            cx - r, cy - r,
            cx + r, cy + r,
            fill=color,
            tag="heart",
            outline=""
        )

        # Left part
        cx = x - cat / 2
        cy = y - 3 / 2 * cat
        self.canvas.create_oval( # type: ignore
            cx - r, cy - r,
            cx + r, cy + r,
            fill=color,
            tag="heart",
            outline=""
        )

        # Highlight
        if not highlight:
            return
        
        self.canvas.create_oval( # type: ignore
            cx - r / 2, cy - r / 2,
            cx + r / 2, cy + r / 2,
            fill=highlight_color,
            tag="heart",
            outline=""
        )
    
    def draw_popup(self, text: str, color: str = "black") -> None:
        self.end_screen = tk.Label(
            text=text,
            font="Arial 100 bold",
            bg=color,
            fg="white",
            borderwidth=self.cell_size // 2,
            relief=tk.RAISED,
            anchor=tk.CENTER,
            padx=self.cell_size,
            pady=self.cell_size
        )
        self.end_screen.grid(
            row=0,
            column=0,
            rowspan=len(self.debug_menu.api_buttons) + len(self.debug_menu.state_labels) + self.offset_rows + 2 + 2)
    
    def draw_cloud(self, pos: Coord, cloud_color: str = Colors.cloud) -> None:
        """
        Draws cloud surround the whole maze except a window around the player.
        """
        self.canvas.delete("cloud")
        # Left side
        self.canvas.create_rectangle( # type: ignore
            self.cell_size * self.offset_cols,
            self.cell_size,
            self.cell_size * self.offset_cols + self.cell_size * max(0, pos[1] - 1),
            self.cell_size * self.offset_rows + self.cell_size * self.m,
            fill=cloud_color,
            outline="",
            tag="cloud"
        )

        # Right side
        self.canvas.create_rectangle( # type: ignore
            self.cell_size * self.offset_cols + self.cell_size * min(self.n, pos[1] + 2),
            self.cell_size,
            self.cell_size * self.offset_cols + self.cell_size * self.n,
            self.cell_size * self.offset_rows + self.cell_size * self.m,
            fill=cloud_color,
            outline="",
            tag="cloud"
        )

        # Top
        self.canvas.create_rectangle( # type: ignore
            self.cell_size * self.offset_cols + self.cell_size * max(0, pos[1] - 1),
            self.cell_size,
            self.cell_size * self.offset_cols + self.cell_size * min(self.n, pos[1] + 2),
            self.cell_size + self.cell_size * max(0, pos[0] - 1),
            fill=cloud_color,
            outline="",
            tag="cloud"
        )

        # Bottom
        self.canvas.create_rectangle( # type: ignore
            self.cell_size * self.offset_cols + self.cell_size * max(0, pos[1] - 1),
            self.cell_size * self.offset_rows + self.cell_size * min(self.m, pos[0] + 2),
            self.cell_size * self.offset_cols + self.cell_size * min(self.n, pos[1] + 2),
            self.cell_size * self.offset_rows + self.cell_size * self.m,
            fill=cloud_color,
            outline="",
            tag="cloud"
        )
        i, j = pos

        # North west corner
        self.draw_sprite("cloud_nw.png", self.cell_size, -self.offset_rows, -self.offset_cols, "cloud")

        # North east corner
        self.draw_sprite("cloud_ne.png", self.cell_size, -self.offset_rows, self.n, "cloud")

        # South east corner
        self.draw_sprite("cloud_se.png", self.cell_size, self.m, self.n, "cloud")

        # South west corner
        self.draw_sprite("cloud_sw.png", self.cell_size, self.m, -self.offset_cols, "cloud")

        # Top border
        for l in range(self.n):
            self.draw_sprite("cloud_n.png", self.cell_size, -self.offset_rows, l, "cloud", str(l))
        
        # Bottom border
        for l in range(self.n):
            self.draw_sprite("cloud_s.png", self.cell_size, self.m, l, "cloud", str(l))
        
        # Left border
        for l in range(-self.offset_rows + 1, self.m):
            self.draw_sprite("cloud_w.png", self.cell_size, l, -self.offset_cols, "cloud", str(l))
        
        # Right border
        for l in range(-self.offset_rows + 1, self.m):
            self.draw_sprite("cloud_e.png", self.cell_size, l, self.n, "cloud", str(l))
        
        # North
        self.draw_sprite("cloud_s.png", self.cell_size, i - 2, j, "cloud")
        self.draw_sprite("cloud_s_seam.png", self.cell_size, i - 1, j, "cloud")

        # Nort East
        self.draw_sprite("cloud_ne_inner_corner.png", self.cell_size, i - 1, j + 1, "cloud")
        self.draw_sprite("cloud_ne_inner_corner_e.png", self.cell_size, i - 1, j + 2, "cloud")
        self.draw_sprite("cloud_ne_inner_corner_n.png", self.cell_size, i - 2, j + 1, "cloud")
        
        # East
        self.draw_sprite("cloud_w.png", self.cell_size, i, j + 2, "cloud")

        # South East
        self.draw_sprite("cloud_se_inner_corner.png", self.cell_size, i + 1, j + 1, "cloud")
        self.draw_sprite("cloud_se_inner_corner_e.png", self.cell_size, i + 1, j + 2, "cloud")
        self.draw_sprite("cloud_se_inner_corner_s.png", self.cell_size, i + 2, j + 1, "cloud")

        # South
        self.draw_sprite("cloud_n.png", self.cell_size, i + 2, j, "cloud")

        # South West
        self.draw_sprite("cloud_sw_inner_corner.png", self.cell_size, i + 1, j - 1, "cloud")
        self.draw_sprite("cloud_sw_inner_corner_s.png", self.cell_size, i + 2, j - 1, "cloud")
        self.draw_sprite("cloud_sw_inner_corner_w.png", self.cell_size, i + 1, j - 2, "cloud")

        # West
        self.draw_sprite("cloud_e.png", self.cell_size, i, j - 2, "cloud")

        # North West
        self.draw_sprite("cloud_nw_inner_corner.png", self.cell_size, i - 1, j - 1, "cloud")
        self.draw_sprite("cloud_nw_inner_corner_w.png", self.cell_size, i - 1, j - 2, "cloud")
        self.draw_sprite("cloud_nw_inner_corner_n.png", self.cell_size, i - 2, j - 1, "cloud")

    def draw_sprite(
            self,
            name: str,
            size: int,
            i: int,
            j: int,
            tag: str,
            unique_id: str | None = None,
            use_offset: bool = True,
            dx: int = 0,
            dy: int = 0
        ) -> None:
        """
        Draws a sprite at position (i, j).
        """
        image = Image.open(os.path.join(self.sprite_path, name))
        image = image.resize((size, size), Image.NEAREST)

        # Need to tie the image to the object somehow, otherwise it gets garbage collected
        stored_name = f"{name}{'_' + unique_id if unique_id is not None else ''}"
        self.sprites[stored_name] = ImageTk.PhotoImage(image)
        if use_offset:
            i += self.offset_rows
            j += self.offset_cols
        self.canvas.create_image(
            j * self.cell_size + self.cell_size // 2 + dx, 
            i * self.cell_size + self.cell_size // 2 + dy, 
            image=self.sprites[stored_name],
            tag=tag
        )

    def push_blue_gem_buffer(self, pos: Coord) -> None:
        self.blue_gem_buffer.add(pos)

    def push_red_gem_buffer(self, pos: Coord) -> None:
        self.red_gem_buffer.add(pos)
