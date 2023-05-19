import tkinter as tk
import random
from minosrecurse.maze_utils import get_maze_size
import threading


class Colors:
    green_base = "#4b9a49"
    green_border = "#316e30"
    grass_base = "#64b663"
    grass_top = "#a6d5a5"
    brown_base = "#8c7748"
    brown_highlight = "#b8a375"
    brown_border = "#65512f"
    blues = {
        0: "#0069aa",
        1: "#0098dc",
        2: "#00cdf9",
        3: "#94fdff",
        4: "#ffffff",
        "main": "#0cf1ff",
    }
    reds = {
        0: "#9d2231",
        1: "#e12937",
        2: "#ff5858",
        3: "#ff9ba2",
        4: "#ffffff",
        "main": "#ff616b",
    }

class Renderer:
    def __init__(
        self,
        maze,
        minotaur_coords,
        cell_size=50,
        grid_width=None,
        gem_size=None,
        minotaur_size=None,
        delay=100,
        offset_rows=1,
        offset_cols=1,
    ):
        self._maze = maze
        self._minotaur_coords = minotaur_coords
        self._cell_size = cell_size
        self._grid_width = grid_width if grid_width else cell_size // 20
        self._offset_rows = offset_rows
        self._offset_cols = offset_cols
        self._delay = delay
        self._m, self._n = get_maze_size(maze)

        # Derived sizes
        self._wall_width = self._cell_size // 10
        self._gem_size = gem_size if gem_size else cell_size // 2
        self._minotaur_size = minotaur_size if minotaur_size else cell_size // 2
        self._gem_third = self._gem_size // 3
        self._gem_sixth = self._gem_size // 6
        self._cell_third = self._cell_size // 3
        self._shadow_offset = self._cell_size // 3
        self._maze_extents = [
            self._offset_cols * self._cell_size,
            self._offset_rows * self._cell_size,
            (self._n + self._offset_cols) * self._cell_size,
            (self._m + self._offset_rows) * self._cell_size,
        ]

        # Buffers tracking changes of state, such that we do not need to redraw
        # all items on every update_draw call.
        self._blue_gem_buffer = set()
        self._red_gem_buffer = set()

        # Canvas to draw on
        self._root = tk.Tk()
        self._root.title("Maze")
        self._menu_buttons = {
            "put_red_gem": tk.Button(self._root, font=f"Courier {self._cell_size // 4}", height=1, text="put_red_gem(pos)"),
            "put_blue_gem": tk.Button(self._root, font=f"Courier {self._cell_size // 4}", height=1, text="put_blue_gem(pos)"),
            "has_red_gem": tk.Button(self._root, font=f"Courier {self._cell_size // 4}", height=1, text="has_red_gem(pos)"),
            "has_blue_gem": tk.Button(self._root, font=f"Courier {self._cell_size // 4}", height=1, text="has_blue_gem(pos)"),
            "push": tk.Button(self._root, font=f"Courier {self._cell_size // 4}", height=1, text="push(pos)"),
            "pop": tk.Button(self._root, font=f"Courier {self._cell_size // 4}", height=1, text="pop()"),
            "found_minotaur": tk.Button(self._root, font=f"Courier {self._cell_size // 4}", height=1, text="found_minotaur()"),
            "was_found": tk.Button(self._root, font=f"Courier {self._cell_size // 4}", height=1, text="was_found()")
        }
        self._canvas = tk.Canvas(
            self._root, width=(self._n + 2) * cell_size, height=(self._m + 2) * cell_size
        )
        self._canvas.grid(row=0, column=0, rowspan=len(self._menu_buttons.values()))
        for i, button in enumerate(self._menu_buttons.values()):

            # Configure common attributes
            button.configure(
                background=Colors.green_base,
                activebackground=Colors.green_border,
                borderwidth=10,
                relief=tk.RAISED,
                fg="white",
            )
            button.grid(row=i, column=1, sticky=tk.W)
        self._canvas.configure(bg=Colors.brown_highlight)
        self._root.configure(bg=Colors.brown_highlight)

    def initial_draw(self):
        """
        Draws components of the maze that will remain unchanged throughout the
        game.
        """
        self.draw_maze()
        self.draw_minotaur()

    
    def update_draw(self, old_pos, curr_pos):
        """
        Draws components of the maze that will change throughout the game.
        Should be called after every move. Will clear buffers.
        """
        print(threading.current_thread())
        self.draw_path_segment(old_pos, curr_pos)
        self.draw_row_col_numbers(curr_pos)
        self.draw_gems(self._blue_gem_buffer, self._red_gem_buffer)
        self.draw_player(curr_pos)
        self._canvas.update()
        self._red_gem_buffer = set()
        self._blue_gem_buffer = set()

    
    def draw_wall(self, start_x, start_y, end_x, end_y, wall_width, wall_color):
        self._canvas.create_line(
            start_x,
            start_y,
            end_x,
            end_y,
            width=wall_width,
            fill=wall_color,
            tag="wall",
            capstyle=tk.ROUND,
        )

    def draw_walls(self, wall_width, wall_color):
        for i in range(self._m):
            for j in range(self._n):
                off_i = i + self._offset_rows
                off_j = j + self._offset_cols
                if not (i - 1, j) in self._maze[(i, j)]:  # Northern neighbor missing
                    self.draw_wall(
                        start_x=off_j * self._cell_size,
                        start_y=off_i * self._cell_size,
                        end_x=(off_j + 1) * self._cell_size,
                        end_y=off_i * self._cell_size,
                        wall_width=wall_width,
                        wall_color=wall_color,
                    )
                if not (i, j - 1) in self._maze[(i, j)]:  # Western neighbor missing
                    self.draw_wall(
                        start_x=off_j * self._cell_size,
                        start_y=off_i * self._cell_size,
                        end_x=off_j * self._cell_size,
                        end_y=(off_i + 1) * self._cell_size,
                        wall_width=wall_width,
                        wall_color=wall_color,
                    )
                if not (i, j + 1) in self._maze[(i, j)]:  # Eastern neighbor missing
                    self.draw_wall(
                        start_x=(off_j + 1) * self._cell_size,
                        start_y=off_i * self._cell_size,
                        end_x=(off_j + 1) * self._cell_size,
                        end_y=(off_i + 1) * self._cell_size,
                        wall_width=wall_width,
                        wall_color=wall_color,
                    )
                if not (i + 1, j) in self._maze[(i, j)]:  # Southern neighbor missing
                    self.draw_wall(
                        start_x=off_j * self._cell_size,
                        start_y=(off_i + 1) * self._cell_size,
                        end_x=(off_j + 1) * self._cell_size,
                        end_y=(off_i + 1) * self._cell_size,
                        wall_width=wall_width,
                        wall_color=wall_color,
                    )
    
    def draw_wall_shadows(self):
        for i in range(self._m):
            for j in range(self._n):
                off_i = i + self._offset_rows
                off_j = j + self._offset_cols
                if not (i - 1, j) in self._maze[(i, j)]:  # Horizontal shadow

                    # If there is a wall to the left, we need to adjust
                    # the shadow to the left because of the thickness of the
                    # wall
                    if (i, j - 1) not in self._maze[(i, j)]:
                        left_x = off_j * self._cell_size
                    else:
                        left_x = off_j * self._cell_size - 2 * self._wall_width
                    
                    # If there is a wall to the right, we need to clip the shadow to avoid bleeding beyong the wall
                    if (i, j + 1) not in self._maze[(i, j)]:
                        right_x = (off_j + 1) * self._cell_size
                    else:
                        right_x = (off_j + 1) * self._cell_size + self._shadow_offset
                    self._canvas.create_polygon(
                        left_x, off_i * self._cell_size,
                        (off_j + 1) * self._cell_size, off_i * self._cell_size - 2 * self._wall_width,  # compensating for wall-width
                        right_x, off_i * self._cell_size,
                        right_x, off_i * self._cell_size + self._shadow_offset,
                        left_x + self._shadow_offset, off_i * self._cell_size + self._shadow_offset,
                        fill=Colors.brown_border,
                        tag="shadow"
                    )
                    
                if not (i, j - 1) in self._maze[(i, j)]:  # Vertical shadow
                    # If there is no wall to the top, we need to adjust the 
                    # shadow to the top because of the tickness of the wall
                    if (i - 1, j) not in self._maze[(i, j)]:
                        top_y = off_i * self._cell_size
                    else:
                        top_y = off_i * self._cell_size - 2 * self._wall_width

                    # If there is a wall below, we need to clip the shadow to
                    # avoid bleeding beyong the wall
                    if (i + 1, j) not in self._maze[(i, j)]:
                        bottom_y = (off_i + 1) * self._cell_size
                    else:
                        bottom_y = (off_i + 1) * self._cell_size + self._shadow_offset
                    self._canvas.create_polygon(
                        off_j * self._cell_size, top_y,
                        off_j * self._cell_size + self._shadow_offset, top_y + self._shadow_offset,
                        off_j * self._cell_size + self._shadow_offset, bottom_y,
                        off_j * self._cell_size, bottom_y,
                        off_j * self._cell_size - 2 * self._wall_width, (off_i + 1) * self._cell_size,
                        fill=Colors.brown_border,
                        tag="shadow"
                    )


    def draw_grid(self):
        for i in range(self._m + self._offset_rows):
            self._canvas.create_line(
                self._offset_cols + self._cell_size,
                i * self._cell_size,
                (self._n + self._offset_cols) * self._cell_size,
                i * self._cell_size,
                width=self._grid_width,
                fill=Colors.brown_border,
                tag="grid",
            )
        for j in range(self._n + self._offset_cols):
            self._canvas.create_line(
                j * self._cell_size,
                self._offset_rows + self._cell_size,
                j * self._cell_size,
                (self._m + self._offset_rows) * self._cell_size,
                width=self._grid_width,
                fill=Colors.brown_border,
                tag="grid",
            )
    
    def draw_gem(self, pos, gem_size, color):
        """
        Draws a fancy gem at in the cell (i, j).
        """
        # Random position in the cell (i, j)
        i, j = pos
        offset = (self._cell_size - gem_size) // 2
        base_x = (j + self._offset_cols) * self._cell_size + offset
        base_y = (i + self._offset_rows) * self._cell_size + offset
        xs = [base_x + i * self._gem_third for i in range(4)]
        ys = list(reversed([base_y + i * self._gem_third for i in range(4)]))

        # Shadow
        self._canvas.create_oval(
            xs[0] + self._gem_sixth, ys[1],
            xs[3] + self._gem_sixth, ys[0] + self._gem_sixth,
            fill=Colors.brown_border,
            outline=""
        )

        # Full gem
        self._canvas.create_polygon(
            xs[0], ys[1],
            xs[0], ys[2],
            xs[1], ys[3],
            xs[2], ys[3],
            xs[3], ys[2],
            xs[3], ys[1],
            xs[2], ys[0],
            xs[1], ys[0],
            fill=color[0],
            width=2
        )

        # Middle
        self._canvas.create_polygon(
            xs[1], ys[1],
            xs[1], ys[2],
            xs[2], ys[2],
            xs[2], ys[1],
            fill=color["main"],
            outline=color[1],
            width=2
        )

        # Shine
        self._canvas.create_polygon(
            xs[1], ys[1],
            xs[1], ys[1] - self._gem_sixth,
            xs[1] + self._gem_sixth, ys[2],
            xs[2], ys[2],
            fill=color[3],
            outline=""
        )

        # Color 1
        self._canvas.create_polygon(
            xs[2], ys[0],
            xs[1], ys[0],
            xs[1], ys[1],
            xs[2], ys[1],
            fill=color[1],
            outline=color[0],
            width=2
        )
        self._canvas.create_polygon(
            xs[2], ys[1],
            xs[2], ys[2],
            xs[3], ys[2],
            xs[3], ys[1],
            fill=color[1],
            outline=color[0],
            width=2
        )

        # Color 2
        self._canvas.create_polygon(
            xs[1], ys[0],
            xs[0], ys[1],
            xs[1], ys[1],
            fill=color[2],
            outline=color[1]
        )
        self._canvas.create_polygon(
            xs[2], ys[2],
            xs[2], ys[3],
            xs[3], ys[2],
            fill=color[2],
            outline=color[1],
            width=2
        )
        
        # Color 3
        self._canvas.create_polygon(
            xs[1], ys[1],
            xs[0], ys[1],
            xs[0], ys[2],
            xs[1], ys[2],
            fill=color[3],
            outline=color[1],
            width=2
        )

        # Color 4
        self._canvas.create_polygon(
            xs[1], ys[1],
            xs[0], ys[1],
            xs[0], ys[2],
            xs[1], ys[2],
            fill=color[3],
            outline=color[1],
            width=2
        )
        self._canvas.create_polygon(
            xs[1], ys[2],
            xs[1], ys[3],
            xs[2], ys[3],
            xs[2], ys[2],
            fill=color[3],
            outline=color[0],
            width=2
        )

        # Color 5
        self._canvas.create_polygon(
            xs[1], ys[2],
            xs[0], ys[2],
            xs[1], ys[3],
            fill=color[4],
            outline=color[1],
            width=2
        )
    
    def draw_grass_blades(self, pos, num_grass=3, num_blades=4, blade_width=4):
        """
        Draws some weeds at a random position in the cell (i, j).
        """
        max_height = self._cell_size // 2
        min_height = self._cell_size // 4

        # Random position in the cell (i, j)
        k, j = pos

        # Generate positions before drawing to potentially change drawing order
        base_positions = []
        for _ in range(num_grass):
            x = (j + self._offset_cols) * self._cell_size + random.randint(0, self._cell_size - num_blades * 2 * blade_width)
            y = (k + self._offset_rows) * self._cell_size + random.randint(0, self._cell_size)
            base_positions.append((x, y))
        
        # Order positions lexicographically by x, then y
        base_positions.sort(key=lambda pos: (pos[0], pos[1]))
        
        for (x, y) in base_positions:
            for k in range(num_blades):
                blade_height = random.randint(min_height, max_height)
                blade_x = x + k * 2 * blade_width
                
                # Shadow
                shadow_offset_x = min(blade_x + self._shadow_offset * blade_height / max_height, self._maze_extents[2]) - blade_x
                shadow_offset_y = min(y + self._shadow_offset * blade_height / max_height, self._maze_extents[3]) - y
                shadow_offset = min(shadow_offset_x, shadow_offset_y)
                self._canvas.create_line(
                    blade_x,
                    y,
                    # Make shadow offset proportional to blade height
                    blade_x + shadow_offset,
                    y + shadow_offset,
                    width=blade_width,
                    fill=Colors.green_border,
                    tag="grass_blade"
                )
                
                self._canvas.create_rectangle(
                    blade_x,
                    y,
                    blade_x + blade_width,
                    y - blade_height,
                    fill=Colors.grass_base,
                    outline="",
                    tag="grass_blade",
                )

                # Small highlight
                self._canvas.create_rectangle(
                    blade_x,
                    y - blade_height + blade_width,
                    blade_x + blade_width,
                    y - blade_height,
                    fill=Colors.grass_top,
                    outline="",
                    tag="grass_blade",
                )

    
    def draw_grass(self):
        """
        Instead of rendering empty cells with four walls in case a cell is not 
        connnected to the maze, we render it as a path of grass.
        """
        for i in range(self._m):
            for j in range(self._n):
                if self._maze[(i, j)] != []:
                    continue
                off_i = i + self._offset_rows
                off_j = j + self._offset_cols
                self._canvas.create_rectangle(
                    off_j * self._cell_size,
                    off_i * self._cell_size,
                    (off_j + 1) * self._cell_size,
                    (off_i + 1) * self._cell_size,
                    fill=Colors.green_base,
                    outline="",
                    tag="cell",
                )
        for i in range(self._m):
            for j in range(self._n):
                if self._maze[(i, j)] == []:
                        self.draw_grass_blades((i, j))

    def draw_maze(self):
        """
        Render a maze using tkinter.
        """
        self.draw_cells(Colors.brown_base)
        self.draw_grid()

        # Creating illusion of thick walls by overlaying multiple walls
        self.draw_walls(self._wall_width * 4, Colors.brown_border)
        self.draw_wall_shadows()
        self.draw_walls(self._wall_width * 3, Colors.brown_base)
        self.draw_walls(self._wall_width * 2, Colors.green_border)
        self.draw_walls(self._wall_width, Colors.green_base)

        # Cover empty cells.
        self.draw_grass()

    def draw_player(self, pos):
        """
        Render the player using tkinter.
        """
        self._canvas.delete("player")
        self._canvas.create_oval(
            (pos[1] + self._offset_cols) * self._cell_size + self._cell_size // 4,
            (pos[0] + self._offset_rows) * self._cell_size + self._cell_size // 4,
            (pos[1] + self._offset_cols) * self._cell_size + 3 * self._cell_size // 4,
            (pos[0] + self._offset_rows) * self._cell_size + 3 * self._cell_size // 4,
            fill="green",
            tag="player",
        )
    
    def draw_pebble(self, pos):
        i, j = pos
        x = random.randint(j * self._cell_size, (j + 1) * self._cell_size)
        y = random.randint(i * self._cell_size, (i + 1) * self._cell_size)

        # Draw pebble.
        max_size = min(self._cell_size // 8, 15)
        min_size = 3
        size = random.randint(min_size, max_size)

        # Base
        self._canvas.create_rectangle(
            x,
            y,
            x + size,
            y + size,
            fill=Colors.brown_border,
            outline="",
            tag="cell",
        )

        # Highlight
        self._canvas.create_rectangle(
            x + 2,
            y + 2,
            x + size - 2,
            y + size // 2,
            fill=Colors.brown_highlight,
            outline="",
            tag="cell",
        )
        

    def draw_cells(self, cell_color, pebble_count=10):
        """
        Render the cells using tkinter.
        """
        for i in range(self._m):
            for j in range(self._n):
                off_i = i + self._offset_rows
                off_j = j + self._offset_cols
                self._canvas.create_rectangle(
                    off_j * self._cell_size,
                    off_i * self._cell_size,
                    (off_j + 1) * self._cell_size,
                    (off_i + 1) * self._cell_size,
                    fill=cell_color,
                    outline="",
                    tag="cell",
                )
                # Draw random pebbles
                for _ in range(pebble_count):
                    self.draw_pebble((off_i, off_j))

    def draw_gems(self, blue_gem_coords, red_gem_coords):
        """
        Render gems using tkinter.
        """
        self._canvas.delete("gem")  # delete old gems
        for i, j in blue_gem_coords:
            self.draw_gem((i, j), self._cell_size // 2, Colors.blues)
    
        for i, j in red_gem_coords:
            self.draw_gem((i, j), self._cell_size // 2, Colors.reds)

    def draw_minotaur(self):
        """
        Render minotaur using tkinter.
        """
        self._canvas.delete("minotaur")  # delete old minotaur
        i, j = self._minotaur_coords
        i += self._offset_rows
        j += self._offset_cols
        # Horns (base)
        self._canvas.create_oval(
            j * self._cell_size,
            i * self._cell_size,
            j * self._cell_size + self._cell_size,
            i * self._cell_size + self._cell_size // 2,
            fill="black",
            tag="minotaur",
            outline="lightgrey",
        )

        # Horns (mask)
        self._canvas.create_oval(
            j * self._cell_size + self._cell_size // 5,
            i * self._cell_size,
            j * self._cell_size + self._cell_size // 5 * 4,
            i * self._cell_size + self._cell_size // 4,
            fill="lightgrey",
            tag="minotaur",
            outline="",
        )

        # Body
        self._canvas.create_oval(
            j * self._cell_size + self._cell_size // 2 - self._minotaur_size // 2,
            i * self._cell_size + self._cell_size // 2 - self._minotaur_size // 2,
            j * self._cell_size + self._cell_size // 2 + self._minotaur_size // 2,
            i * self._cell_size + self._cell_size // 2 + self._minotaur_size // 2,
            fill="black",
            tag="minotaur",
        )

        # Eyes
        self._canvas.create_oval(
            j * self._cell_size + self._cell_size // 2 - self._minotaur_size // 3,
            i * self._cell_size + self._cell_size // 2 - self._minotaur_size // 4,
            j * self._cell_size + self._cell_size // 2 - self._minotaur_size // 8,
            i * self._cell_size + self._cell_size // 2,
            fill="red",
            tag="minotaur",
        )

        self._canvas.create_oval(
            j * self._cell_size + self._cell_size // 2 + self._minotaur_size // 8,
            i * self._cell_size + self._cell_size // 2 - self._minotaur_size // 4,
            j * self._cell_size + self._cell_size // 2 + self._minotaur_size // 3,
            i * self._cell_size + self._cell_size // 2,
            fill="red",
            tag="minotaur",
        )

    def draw_path_segment(self, source, target):
        """
        Render a path segment using tkinter.
        """
        self._canvas.create_line(
            (source[1] + self._offset_cols) * self._cell_size + self._cell_size // 2,
            (source[0] + self._offset_rows) * self._cell_size + self._cell_size // 2,
            (target[1] + self._offset_cols) * self._cell_size + self._cell_size // 2,
            (target[0] + self._offset_rows) * self._cell_size + self._cell_size // 2,
            fill="green",
            width=5,
            tag="path",
        )

    def draw_row_col_numbers(self, pos, font_size=None):
        """
        Render row and column numbers using tkinter.
        """
        if font_size is None:
            font_size = self._cell_size // 4
        self._canvas.delete("number")  # delete old numbers
        for i in range(self._m):
            self._canvas.create_text(
                (self._offset_cols - 0.5) * self._cell_size,
                (i + self._offset_rows + 0.5) * self._cell_size,
                text=str(i),
                font=f"Arial {self._cell_size // 4} {'bold' if pos[0] == i else ''}",
                fill=Colors.blues[1] if pos[0] == i else "white",
                anchor="e",
                tag="number"
            )
        for j in range(self._n):
            self._canvas.create_text(
                (j + self._offset_cols + 0.5) * self._cell_size,
                (self._offset_rows - 2/3) * self._cell_size,
                text=str(j),
                font=f"Arial {self._cell_size // 4} {'bold' if pos[1] == j else ''}",
                fill=Colors.blues[1] if pos[1] == j else "white",
                anchor="n",
                tag="number"
            )
    
    def push_blue_gem_buffer(self, pos):
        self._blue_gem_buffer.add(pos)
    
    def push_red_gem_buffer(self, pos):
        self._red_gem_buffer.add(pos)
