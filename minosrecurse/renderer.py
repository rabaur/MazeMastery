import tkinter as tk
import random
from minosrecurse.maze import create_maze
from minosrecurse.maze_utils import get_maze_size


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
        cell_size=100,
        wall_width=None,
        grid_width=None,
        gem_size=None,
        minotauros_size=None,
        delay=100,
        offset_rows=1,
        offset_cols=1,
    ):
        self.maze = maze
        self.cell_size = cell_size
        self.wall_width = wall_width if wall_width else cell_size // 10
        self.grid_width = grid_width if grid_width else cell_size // 20
        self.minotauros_size = minotauros_size if minotauros_size else cell_size // 2
        self.offset_rows = offset_rows
        self.offset_cols = offset_cols
        self.gem_size = gem_size if gem_size else cell_size // 2
        self.delay = delay
        self.m, self.n = get_maze_size(maze)

        # Some sizes
        self.gem_size = self.cell_size // 2
        self.gem_third = self.gem_size // 3
        self.gem_sixth = self.gem_size // 6
        self.third = self.cell_size // 3
        self.shadow_offset = self.cell_size // 3

        # Canvas to draw on
        root = tk.Tk()
        root.title("Maze")
        self.canvas = tk.Canvas(
            root, width=(self.n + 2) * cell_size, height=(self.m + 2) * cell_size
        )
        self.canvas.pack()

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
    
    def draw_grass_blades(self, pos, num_blades=4, blade_width=4):
        """
        Draws some weeds at a random position in the cell (i, j).
        """
        max_height = self.cell_size // 2

        # Random position in the cell (i, j)
        i, j = pos
        x = (j + self.offset_cols) * self.cell_size + random.randint(0, self.cell_size)
        y = (i + self.offset_rows) * self.cell_size + random.randint(0, self.cell_size)
        for i in range(num_blades):
            blade_height = random.randint(0, max_height)
            blade_x = x + i * 2 * blade_width
            self.canvas.create_rectangle(
                blade_x,
                y,
                blade_x + blade_width,
                y - blade_height,
                fill=Colors.grass_base,
                outline="",
                tag="grass_blade",
            )
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
                for _ in range(3):
                    self.draw_grass_blades((i, j))

    def draw_maze(self):
        """
        Render a maze using tkinter.
        """
        self.draw_row_col_numbers()
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
        max_size = min(self.cell_size // 8, 15)
        min_size = 3
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

    def draw_minotaurus(self, minotaurus_coords):
        """
        Render minotaurus using tkinter.
        """
        self.canvas.delete("minotaurus")  # delete old minotaurus
        i, j = minotaurus_coords
        i += self.offset_rows
        j += self.offset_cols
        # Horns (base)
        self.canvas.create_oval(
            j * self.cell_size,
            i * self.cell_size,
            j * self.cell_size + self.cell_size,
            i * self.cell_size + self.cell_size // 2,
            fill="black",
            tag="minotaurus",
            outline="lightgrey",
        )

        # Horns (mask)
        self.canvas.create_oval(
            j * self.cell_size + self.cell_size // 5,
            i * self.cell_size,
            j * self.cell_size + self.cell_size // 5 * 4,
            i * self.cell_size + self.cell_size // 4,
            fill="lightgrey",
            tag="minotaurus",
            outline="",
        )

        # Body
        self.canvas.create_oval(
            j * self.cell_size + self.cell_size // 2 - self.minotauros_size // 2,
            i * self.cell_size + self.cell_size // 2 - self.minotauros_size // 2,
            j * self.cell_size + self.cell_size // 2 + self.minotauros_size // 2,
            i * self.cell_size + self.cell_size // 2 + self.minotauros_size // 2,
            fill="black",
            tag="minotaurus",
        )

        # Eyes
        self.canvas.create_oval(
            j * self.cell_size + self.cell_size // 2 - self.minotauros_size // 3,
            i * self.cell_size + self.cell_size // 2 - self.minotauros_size // 4,
            j * self.cell_size + self.cell_size // 2 - self.minotauros_size // 8,
            i * self.cell_size + self.cell_size // 2,
            fill="red",
            tag="minotaurus",
        )

        self.canvas.create_oval(
            j * self.cell_size + self.cell_size // 2 + self.minotauros_size // 8,
            i * self.cell_size + self.cell_size // 2 - self.minotauros_size // 4,
            j * self.cell_size + self.cell_size // 2 + self.minotauros_size // 3,
            i * self.cell_size + self.cell_size // 2,
            fill="red",
            tag="minotaurus",
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

    def draw_row_col_numbers(self):
        """
        Render row and column numbers using tkinter.
        """
        for i in range(self.m):
            self.canvas.create_text(
                (self.offset_cols - 0.5) * self.cell_size,
                (i + self.offset_rows + 0.5) * self.cell_size,
                text=str(i),
                font="Arial 10",
                anchor="e",
            )
        for j in range(self.n):
            self.canvas.create_text(
                (j + self.offset_cols + 0.5) * self.cell_size,
                (self.offset_rows - 0.5) * self.cell_size,
                text=str(j),
                font="Arial 10",
                anchor="n",
            )

    def update(self):
        """
        Update the canvas.
        """
        self.canvas.update()

    def after(self):
        """
        Wait for a short time.
        """
        self.canvas.after(self.delay)
    
    def mainloop(self):
        """
        Start the tkinter mainloop.
        """
        self.canvas.mainloop()
