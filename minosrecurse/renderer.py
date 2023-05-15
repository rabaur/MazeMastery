import tkinter as tk
import random
from minosrecurse.maze import create_maze
from minosrecurse.maze_utils import get_maze_size


class Colors:
    green_base = "#4b9a49"
    green_border = "#316e30"
    brown_base = "#8c7748"
    brown_border = "#776038"


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
            capstyle=tk.BUTT,
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

    def draw_grid(self):
        for i in range(self.m):
            self.canvas.create_line(
                self.offset_cols * self.cell_size,
                i * self.cell_size,
                (self.n + self.offset_cols) * self.cell_size,
                i * self.cell_size,
                width=self.grid_width,
                fill="grey",
                tag="grid",
            )
        for j in range(self.n):
            self.canvas.create_line(
                j * self.cell_size,
                self.offset_rows * self.cell_size,
                j * self.cell_size,
                (self.m + self.offset_cols) * self.cell_size,
                width=self.grid_width,
                fill="grey",
                tag="grid",
            )

    def draw_maze(self):
        """
        Render a maze using tkinter.
        """
        self.draw_row_col_numbers()
        self.draw_cells(Colors.brown_base)
        self.draw_grid()

        # Creating illusion of thick walls by overlaying multiple walls
        self.draw_walls(self.wall_width * 4, Colors.brown_border)
        self.draw_walls(self.wall_width * 3, Colors.brown_base)
        self.draw_walls(self.wall_width * 2, Colors.green_border)
        self.draw_walls(self.wall_width, Colors.green_base)

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
                    # Draw random pixel within cell.
                    x = random.randint(off_j * self.cell_size, (off_j + 1) * self.cell_size)
                    y = random.randint(off_i * self.cell_size, (off_i + 1) * self.cell_size)

                    # Draw pebble.
                    self.canvas.create_rectangle(
                        x,
                        y,
                        x + 4,
                        y + 4,
                        fill=Colors.brown_border,
                        outline="",
                        tag="cell",
                    )

    def draw_gems(self, blue_gem_coords, red_gem_coords):
        """
        Render gems using tkinter.
        """
        self.canvas.delete("gem")  # delete old gems
        for i, j in blue_gem_coords:
            i += self.offset_rows
            j += self.offset_cols
            self.canvas.create_oval(
                j * self.cell_size + self.cell_size // 2 - self.gem_size // 2,
                i * self.cell_size + self.cell_size // 2 - self.gem_size // 2,
                j * self.cell_size + self.cell_size // 2 + self.gem_size // 2,
                i * self.cell_size + self.cell_size // 2 + self.gem_size // 2,
                fill="blue",
                tag="gem",
            )
        for i, j in red_gem_coords:
            i += self.offset_rows
            j += self.offset_cols
            self.canvas.create_oval(
                j * self.cell_size + self.cell_size // 2 - self.gem_size // 2,
                i * self.cell_size + self.cell_size // 2 - self.gem_size // 2,
                j * self.cell_size + self.cell_size // 2 + self.gem_size // 2,
                i * self.cell_size + self.cell_size // 2 + self.gem_size // 2,
                fill="red",
                tag="gem",
            )

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
