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
        initial_pos=(0, 0)
    ):
        self.maze = maze
        self.minotaur_coords = minotaur_coords
        self.cell_size = cell_size
        self.grid_width = grid_width if grid_width else cell_size // 20
        self.offset_rows = offset_rows
        self.offset_cols = offset_cols
        self.delay = delay
        self.m, self.n = get_maze_size(maze)

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
        self.blue_gem_buffer = set()
        self.red_gem_buffer = set()
        self.initial_pos = initial_pos

        # Canvas to draw on
        self.root = tk.Tk()
        self.root.title("Maze")
        self.debug_button = tk.Button(self.root, font=f"Arial {self.cell_size // 4}", height=1, text="Debug")
        self.maze_state_mod_buttons = {
            "put_red_gem": tk.Button(self.root, font=f"Courier {self.cell_size // 4}", height=1, text="put_red_gem(pos)"),
            "put_blue_gem": tk.Button(self.root, font=f"Courier {self.cell_size // 4}", height=1, text="put_blue_gem(pos)"),
            "has_red_gem": tk.Button(self.root, font=f"Courier {self.cell_size // 4}", height=1, text="has_red_gem(pos)"),
            "has_blue_gem": tk.Button(self.root, font=f"Courier {self.cell_size // 4}", height=1, text="has_blue_gem(pos)"),
            "push": tk.Button(self.root, font=f"Courier {self.cell_size // 4}", height=1, text="push(pos)"),
            "pop": tk.Button(self.root, font=f"Courier {self.cell_size // 4}", height=1, text="pop()"),
            "found_minotaur": tk.Button(self.root, font=f"Courier {self.cell_size // 4}", height=1, text="found_minotaur()"),
            "was_found": tk.Button(self.root, font=f"Courier {self.cell_size // 4}", height=1, text="was_found()")
        }
        self.canvas = tk.Canvas(
            self.root, width=(self.n + 2) * cell_size, height=(self.m + 2) * cell_size
        )
        self.canvas.grid(row=0, column=0, rowspan=len(self.maze_state_mod_buttons.values()))
        self.debug_button.grid(row=0, column=1)
        for i, button in enumerate(self.maze_state_mod_buttons.values()):

            # Configure common attributes
            button.configure(
                background=Colors.green_base,
                activebackground=Colors.green_border,
                borderwidth=10,
                relief=tk.RAISED,
                fg="white",
            )
            button.grid(row=i + 1, column=1, sticky=tk.W)
        self.canvas.configure(bg=Colors.brown_highlight)
        self.root.configure(bg=Colors.brown_highlight)
    
    def render_menu(self):
        if self._debug:
            self.debug_button.configure(background=Colors.green_base)

    def initial_draw(self):
        """
        Draws components of the maze that will remain unchanged throughout the
        game.
        """
        self.draw_maze()
        self.draw_minotaur()
        self.draw_initial_row_col_numbers()

    
    def update_draw(self, old_pos, curr_pos):
        """
        Draws components of the maze that will change throughout the game.
        Should be called after every move. Will clear buffers.
        """
        self.draw_path_segment(old_pos, curr_pos)
        self.draw_row_col_numbers(old_pos, curr_pos)
        self.draw_gems(self.blue_gem_buffer, self.red_gem_buffer)
        self.draw_player(curr_pos)
        self.canvas.update()
        self.red_gem_buffer = set()
        self.blue_gem_buffer = set()

    
    def draw_wall(self, start_x, start_y, end_x, end_y, wall_width, wall_color):
        self.canvas.create_line(
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
    
    def draw_wall_shadows(self):
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
                    self.canvas.create_polygon(
                        left_x, off_i * self.cell_size,
                        (off_j + 1) * self.cell_size, off_i * self.cell_size - 2 * self.wall_width,  # compensating for wall-width
                        right_x, off_i * self.cell_size,
                        right_x, off_i * self.cell_size + self.shadow_offset,
                        left_x + self.shadow_offset, off_i * self.cell_size + self.shadow_offset,
                        fill=Colors.brown_border,
                        tag="shadow"
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
                    self.canvas.create_polygon(
                        off_j * self.cell_size, top_y,
                        off_j * self.cell_size + self.shadow_offset, top_y + self.shadow_offset,
                        off_j * self.cell_size + self.shadow_offset, bottom_y,
                        off_j * self.cell_size, bottom_y,
                        off_j * self.cell_size - 2 * self.wall_width, (off_i + 1) * self.cell_size,
                        fill=Colors.brown_border,
                        tag="shadow"
                    )


    def draw_grid(self):
        for i in range(self.m + self.offset_rows):
            self.canvas.create_line(
                self.offset_cols + self.cell_size,
                i * self.cell_size,
                (self.n + self.offset_cols) * self.cell_size,
                i * self.cell_size,
                width=self.grid_width,
                fill=Colors.brown_border,
                tag="grid",
            )
        for j in range(self.n + self.offset_cols):
            self.canvas.create_line(
                j * self.cell_size,
                self.offset_rows + self.cell_size,
                j * self.cell_size,
                (self.m + self.offset_rows) * self.cell_size,
                width=self.grid_width,
                fill=Colors.brown_border,
                tag="grid",
            )
    
    def draw_gem(self, pos, gem_size, color):
        """
        Draws a fancy gem at in the cell (i, j).
        """
        # Random position in the cell (i, j)
        i, j = pos
        offset = (self.cell_size - gem_size) // 2
        base_x = (j + self.offset_cols) * self.cell_size + offset
        base_y = (i + self.offset_rows) * self.cell_size + offset
        xs = [base_x + i * self.gem_third for i in range(4)]
        ys = list(reversed([base_y + i * self.gem_third for i in range(4)]))

        # Shadow
        self.canvas.create_oval(
            xs[0] + self.gem_sixth, ys[1],
            xs[3] + self.gem_sixth, ys[0] + self.gem_sixth,
            fill=Colors.brown_border,
            outline=""
        )

        # Full gem
        self.canvas.create_polygon(
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
        self.canvas.create_polygon(
            xs[1], ys[1],
            xs[1], ys[2],
            xs[2], ys[2],
            xs[2], ys[1],
            fill=color["main"],
            outline=color[1],
            width=2
        )

        # Shine
        self.canvas.create_polygon(
            xs[1], ys[1],
            xs[1], ys[1] - self.gem_sixth,
            xs[1] + self.gem_sixth, ys[2],
            xs[2], ys[2],
            fill=color[3],
            outline=""
        )

        # Color 1
        self.canvas.create_polygon(
            xs[2], ys[0],
            xs[1], ys[0],
            xs[1], ys[1],
            xs[2], ys[1],
            fill=color[1],
            outline=color[0],
            width=2
        )
        self.canvas.create_polygon(
            xs[2], ys[1],
            xs[2], ys[2],
            xs[3], ys[2],
            xs[3], ys[1],
            fill=color[1],
            outline=color[0],
            width=2
        )

        # Color 2
        self.canvas.create_polygon(
            xs[1], ys[0],
            xs[0], ys[1],
            xs[1], ys[1],
            fill=color[2],
            outline=color[1]
        )
        self.canvas.create_polygon(
            xs[2], ys[2],
            xs[2], ys[3],
            xs[3], ys[2],
            fill=color[2],
            outline=color[1],
            width=2
        )
        
        # Color 3
        self.canvas.create_polygon(
            xs[1], ys[1],
            xs[0], ys[1],
            xs[0], ys[2],
            xs[1], ys[2],
            fill=color[3],
            outline=color[1],
            width=2
        )

        # Color 4
        self.canvas.create_polygon(
            xs[1], ys[1],
            xs[0], ys[1],
            xs[0], ys[2],
            xs[1], ys[2],
            fill=color[3],
            outline=color[1],
            width=2
        )
        self.canvas.create_polygon(
            xs[1], ys[2],
            xs[1], ys[3],
            xs[2], ys[3],
            xs[2], ys[2],
            fill=color[3],
            outline=color[0],
            width=2
        )

        # Color 5
        self.canvas.create_polygon(
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
        max_height = self.cell_size // 2
        min_height = self.cell_size // 4

        # Random position in the cell (i, j)
        k, j = pos

        # Generate positions before drawing to potentially change drawing order
        base_positions = []
        for _ in range(num_grass):
            x = (j + self.offset_cols) * self.cell_size + random.randint(0, self.cell_size - num_blades * 2 * blade_width)
            y = (k + self.offset_rows) * self.cell_size + random.randint(0, self.cell_size)
            base_positions.append((x, y))
        
        # Order positions lexicographically by x, then y
        base_positions.sort(key=lambda pos: (pos[0], pos[1]))
        
        for (x, y) in base_positions:
            for k in range(num_blades):
                blade_height = random.randint(min_height, max_height)
                blade_x = x + k * 2 * blade_width
                
                # Shadow
                shadow_offset_x = min(blade_x + self.shadow_offset * blade_height / max_height, self.maze_extents[2]) - blade_x
                shadow_offset_y = min(y + self.shadow_offset * blade_height / max_height, self.maze_extents[3]) - y
                shadow_offset = min(shadow_offset_x, shadow_offset_y)
                self.canvas.create_line(
                    blade_x,
                    y,
                    # Make shadow offset proportional to blade height
                    blade_x + shadow_offset,
                    y + shadow_offset,
                    width=blade_width,
                    fill=Colors.green_border,
                    tag="grass_blade"
                )
                
                self.canvas.create_rectangle(
                    blade_x,
                    y,
                    blade_x + blade_width,
                    y - blade_height,
                    fill=Colors.grass_base,
                    outline="",
                    tag="grass_blade",
                )

                # Small highlight
                self.canvas.create_rectangle(
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
        for i in range(self.m):
            for j in range(self.n):
                if self.maze[(i, j)] != []:
                    continue
                off_i = i + self.offset_rows
                off_j = j + self.offset_cols
                self.canvas.create_rectangle(
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

    def draw_maze(self):
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

    def draw_player(self, pos):
        """
        Render the player using tkinter.
        """
        self.canvas.delete("player")
        self.canvas.create_oval(
            (pos[1] + self.offset_cols) * self.cell_size + self.cell_size // 4,
            (pos[0] + self.offset_rows) * self.cell_size + self.cell_size // 4,
            (pos[1] + self.offset_cols) * self.cell_size + 3 * self.cell_size // 4,
            (pos[0] + self.offset_rows) * self.cell_size + 3 * self.cell_size // 4,
            fill="green",
            tag="player",
        )
    
    def draw_pebble(self, pos):
        i, j = pos
        x = random.randint(j * self.cell_size, (j + 1) * self.cell_size)
        y = random.randint(i * self.cell_size, (i + 1) * self.cell_size)

        # Draw pebble.
        max_size = self.cell_size // 8
        min_size = self.cell_size // 16
        size = random.randint(min_size, max_size)

        # Base
        self.canvas.create_rectangle(
            x,
            y,
            x + size,
            y + size,
            fill=Colors.brown_border,
            outline="",
            tag="cell",
        )

        # Highlight
        self.canvas.create_rectangle(
            x + 2,
            y + 2,
            x + size // 3 * 2,
            y + size // 3 * 2,
            fill=Colors.brown_highlight,
            outline="",
            tag="cell",
        )
        

    def draw_cells(self, cell_color, pebble_count=10):
        """
        Render the cells using tkinter.
        """
        for i in range(self.m):
            for j in range(self.n):
                off_i = i + self.offset_rows
                off_j = j + self.offset_cols
                self.canvas.create_rectangle(
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

    def draw_gems(self, blue_gem_coords, red_gem_coords):
        """
        Render gems using tkinter.
        """
        self.canvas.delete("gem")  # delete old gems
        for i, j in blue_gem_coords:
            self.draw_gem((i, j), self.cell_size // 2, Colors.blues)
    
        for i, j in red_gem_coords:
            self.draw_gem((i, j), self.cell_size // 2, Colors.reds)

    def draw_minotaur(self):
        """
        Render minotaur using tkinter.
        """
        self.canvas.delete("minotaur")  # delete old minotaur
        i, j = self.minotaur_coords
        i += self.offset_rows
        j += self.offset_cols
        # Horns (base)
        self.canvas.create_oval(
            j * self.cell_size,
            i * self.cell_size,
            j * self.cell_size + self.cell_size,
            i * self.cell_size + self.cell_size // 2,
            fill="black",
            tag="minotaur",
            outline="lightgrey",
        )

        # Horns (mask)
        self.canvas.create_oval(
            j * self.cell_size + self.cell_size // 5,
            i * self.cell_size,
            j * self.cell_size + self.cell_size // 5 * 4,
            i * self.cell_size + self.cell_size // 4,
            fill="lightgrey",
            tag="minotaur",
            outline="",
        )

        # Body
        self.canvas.create_oval(
            j * self.cell_size + self.cell_size // 2 - self.minotaur_size // 2,
            i * self.cell_size + self.cell_size // 2 - self.minotaur_size // 2,
            j * self.cell_size + self.cell_size // 2 + self.minotaur_size // 2,
            i * self.cell_size + self.cell_size // 2 + self.minotaur_size // 2,
            fill="black",
            tag="minotaur",
        )

        # Eyes
        self.canvas.create_oval(
            j * self.cell_size + self.cell_size // 2 - self.minotaur_size // 3,
            i * self.cell_size + self.cell_size // 2 - self.minotaur_size // 4,
            j * self.cell_size + self.cell_size // 2 - self.minotaur_size // 8,
            i * self.cell_size + self.cell_size // 2,
            fill="red",
            tag="minotaur",
        )

        self.canvas.create_oval(
            j * self.cell_size + self.cell_size // 2 + self.minotaur_size // 8,
            i * self.cell_size + self.cell_size // 2 - self.minotaur_size // 4,
            j * self.cell_size + self.cell_size // 2 + self.minotaur_size // 3,
            i * self.cell_size + self.cell_size // 2,
            fill="red",
            tag="minotaur",
        )

    def draw_path_segment(self, source, target):
        """
        Render a path segment using tkinter.
        """
        self.canvas.create_line(
            (source[1] + self.offset_cols) * self.cell_size + self.cell_size // 2,
            (source[0] + self.offset_rows) * self.cell_size + self.cell_size // 2,
            (target[1] + self.offset_cols) * self.cell_size + self.cell_size // 2,
            (target[0] + self.offset_rows) * self.cell_size + self.cell_size // 2,
            fill="green",
            width=5,
            tag="path",
        )
    
    def draw_initial_row_col_numbers(self, font_size=None):
        """
        Render initial row and column numbers using tkinter.
        """
        if font_size is None:
            font_size = self.cell_size // 4
        for i in range(self.m):
            self.canvas.create_text(
                (self.offset_cols - 0.5) * self.cell_size,
                (i + self.offset_rows + 0.5) * self.cell_size,
                text=str(i),
                font=f"Arial {font_size} {'bold' if self.initial_pos[0] == i else ''}",
                fill=Colors.blues[1] if self.initial_pos[0] == i else "white",
                anchor="e",
                tag=f"row_number_{i}",
            )
        for j in range(self.n):
            self.canvas.create_text(
                (j + self.offset_cols + 0.5) * self.cell_size,
                (self.offset_rows - 2/3) * self.cell_size,
                text=str(j),
                font=f"Arial {font_size} {'bold' if self.initial_pos[1] == j else ''}",
                fill=Colors.blues[1] if self.initial_pos[1] == j else "white",
                anchor="n",
                tag=f"col_number_{j}",
            )

    def draw_row_col_numbers(self, old_pos, pos, font_size=None):
        """
        Render row and column numbers using tkinter.
        """
        if font_size is None:
            font_size = self.cell_size // 4
        self.canvas.delete("number")  # delete old numbers
        if old_pos[0] != pos[0]: # row number changed, update required
            self.canvas.delete(f"row_number_{old_pos[0]}")
            self.canvas.delete(f"row_number_{pos[0]}")
            self.canvas.create_text(
                (self.offset_cols - 0.5) * self.cell_size,
                (old_pos[0] + self.offset_rows + 0.5) * self.cell_size,
                text=str(old_pos[0]),
                font=f"Arial {font_size}",
                fill="white",
                anchor="e",
                tag=f"row_number_{old_pos[0]}"
            )
            self.canvas.create_text(
                (self.offset_cols - 0.5) * self.cell_size,
                (pos[0] + self.offset_rows + 0.5) * self.cell_size,
                text=str(pos[0]),
                font=f"Arial {font_size} bold",
                fill=Colors.blues[1],
                anchor="e",
                tag=f"row_number_{pos[0]}"
            )
        if old_pos[1] != pos[1]: # col number changed, update required
            self.canvas.delete(f"col_number_{old_pos[1]}")
            self.canvas.delete(f"col_number_{pos[1]}")
            self.canvas.create_text(
                (old_pos[1] + self.offset_cols + 0.5) * self.cell_size,
                (self.offset_rows - 2/3) * self.cell_size,
                text=str(old_pos[1]),
                font=f"Arial {font_size}",
                fill="white",
                anchor="n",
                tag=f"col_number_{old_pos[1]}"
            )
            self.canvas.create_text(
                (pos[1] + self.offset_cols + 0.5) * self.cell_size,
                (self.offset_rows - 2/3) * self.cell_size,
                text=str(pos[1]),
                font=f"Arial {font_size} bold",
                fill=Colors.blues[1],
                anchor="n",
                tag=f"col_number_{pos[1]}"
            )
    
    def push_blue_gem_buffer(self, pos):
        self.blue_gem_buffer.add(pos)
    
    def push_red_gem_buffer(self, pos):
        self.red_gem_buffer.add(pos)
