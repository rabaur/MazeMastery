import tkinter as tk
import random
from minosrecurse.maze import create_maze
from minosrecurse.maze_utils import get_maze_size

class Colors:
    green_base='#4b9a49'
    green_border='#316e30'
    brown_base='#8c7748'
    brown_border='#776038'

def draw_wall(canvas, start_x, start_y, end_x, end_y, ligatures, wall_width, wall_color):
    canvas.create_line(
        start_x,
        start_y,
        end_x,
        end_y,
        width=wall_width,
        fill=wall_color,
        tag="wall"
    )
    if ligatures:
        canvas.create_oval(
            start_x - wall_width / 2,
            start_y - wall_width / 2,
            start_x + wall_width / 2,
            start_y + wall_width / 2,
            fill=wall_color,
            outline="",
            tag="wall"
        )
        canvas.create_oval(
            end_x - wall_width / 2,
            end_y - wall_width / 2,
            end_x + wall_width / 2,
            end_y + wall_width / 2,
            fill=wall_color,
            outline="",
            tag="wall"
        )

def draw_walls(
        maze,
        cell_size,
        wall_width,
        canvas,
        wall_color,
        offset_rows=1,
        offset_cols=1,
        ligatures=True
    ):
    m, n = get_maze_size(maze)

    for i in range(m):
        for j in range(n):
            off_i = i + offset_rows
            off_j = j + offset_cols
            if not (i - 1, j) in maze[(i, j)]:  # Northern neighbor missing
                draw_wall(
                    canvas,
                    off_j * cell_size,
                    off_i * cell_size,
                    (off_j + 1) * cell_size,
                    off_i * cell_size,
                    ligatures,
                    wall_width,
                    wall_color
                )
            if not (i, j - 1) in maze[(i, j)]:  # Western neighbor missing
                canvas.create_line(
                    off_j * cell_size,
                    off_i * cell_size,
                    off_j * cell_size,
                    (off_i + 1) * cell_size,
                    width=wall_width,
                    fill=wall_color,
                    tag="wall"
                )
            if not (i, j + 1) in maze[(i, j)]:  # Eastern neighbor missing
                canvas.create_line(
                    (off_j + 1) * cell_size,
                    off_i * cell_size,
                    (off_j + 1) * cell_size,
                    (off_i + 1) * cell_size,
                    width=wall_width,
                    fill="black",
                    tag="wall"
                )
            if not (i + 1, j) in maze[(i, j)]:  # Southern neighbor missing
                canvas.create_line(
                    off_j * cell_size,
                    (off_i + 1) * cell_size,
                    (off_j + 1) * cell_size,
                    (off_i + 1) * cell_size,
                    width=wall_width,
                    fill="black",
                    tag="wall"
                )

def draw_grid(maze, cell_size, grid_width, canvas, offset_rows=1, offset_cols=1):
    m, n = get_maze_size(maze)
    for i in range(m):
        canvas.create_line(
            offset_cols * cell_size,
            i * cell_size,
            (n + offset_cols) * cell_size,
            i * cell_size,
            width=grid_width,
            fill="grey",
            tag="grid"
        )
    for j in range(n):
        canvas.create_line(
            j * cell_size,
            offset_rows * cell_size,
            j * cell_size,
            (m + offset_cols) * cell_size,
            width=grid_width,
            fill="grey",
            tag="grid"
        )


def draw_maze(maze, canvas, cell_size=50, wall_width=10, grid_width=1):
    """
    Render a maze using tkinter.
    """
    draw_row_col_numbers(maze, canvas, cell_size)
    draw_cells(canvas, maze, Colors.brown_base, cell_size)
    draw_grid(maze, cell_size, grid_width, canvas)
    draw_walls(maze, cell_size, wall_width * 4, canvas, Colors.brown_border)
    draw_walls(maze, cell_size, wall_width * 3, canvas, Colors.brown_base)
    draw_walls(maze, cell_size, wall_width * 2, canvas, Colors.green_border)
    draw_walls(maze, cell_size, wall_width, canvas, Colors.green_base)

def draw_player(canvas, pos, cell_size=50, offset_rows=1, offset_cols=1):
    """
    Render the player using tkinter.
    """
    canvas.delete("player")
    canvas.create_oval(
        (pos[1] + offset_cols) * cell_size + cell_size // 4,
        (pos[0] + offset_rows) * cell_size + cell_size // 4,
        (pos[1] + offset_cols) * cell_size + 3 * cell_size // 4,
        (pos[0] + offset_rows) * cell_size + 3 * cell_size // 4,
        fill="green",
        tag="player"
    )

def draw_cells(
        canvas,
        maze,
        cell_color,
        cell_size=50,
        pebble_count=10,
        offset_rows=1,
        offset_cols=1
    ):
    """
    Render the cells using tkinter.
    """
    m, n = get_maze_size(maze)
    for i in range(m):
        for j in range(n):
            off_i = i + offset_rows
            off_j = j + offset_cols
            canvas.create_rectangle(
                off_j * cell_size,
                off_i * cell_size,
                (off_j + 1) * cell_size,
                (off_i + 1) * cell_size,
                fill=cell_color,
                outline="",
                tag="cell"
            )
            # Draw random pebbles
            for _ in range(pebble_count):

                # Draw random pixel within cell.
                x = random.randint(off_j * cell_size, (off_j + 1) * cell_size)
                y = random.randint(off_i * cell_size, (off_i + 1) * cell_size)

                # Draw pebble.
                canvas.create_rectangle(
                    x,
                    y,
                    x + 4,
                    y + 4,
                    fill=Colors.brown_border,
                    outline="",
                    tag="cell"
                )

def draw_gems(blue_gem_coords, red_gem_coords, canvas, gem_size, cell_size, offset_rows=1, offset_cols=1):
    """
    Render gems using tkinter.
    """
    canvas.delete("gem") # delete old gems
    for i, j in blue_gem_coords:
        i += offset_rows
        j += offset_cols
        canvas.create_oval(
            j * cell_size + cell_size // 2 - gem_size // 2,
            i * cell_size + cell_size // 2 - gem_size // 2,
            j * cell_size + cell_size // 2 + gem_size // 2,
            i * cell_size + cell_size // 2 + gem_size // 2,
            fill="blue",
            tag="gem"
        )
    for i, j in red_gem_coords:
        i += offset_rows
        j += offset_cols
        canvas.create_oval(
            j * cell_size + cell_size // 2 - gem_size // 2,
            i * cell_size + cell_size // 2 - gem_size // 2,
            j * cell_size + cell_size // 2 + gem_size // 2,
            i * cell_size + cell_size // 2 + gem_size // 2,
            fill="red",
            tag="gem"
        )

def draw_minotaurus(minotaurus_coords, canvas, minotaurus_size, cell_size, offset_rows=1, offset_cols=1):
    """
    Render minotaurus using tkinter.
    """
    canvas.delete("minotaurus") # delete old minotaurus
    i, j = minotaurus_coords
    i += offset_rows
    j += offset_cols
    # Horns (base)
    canvas.create_oval(
        j * cell_size,
        i * cell_size,
        j * cell_size + cell_size,
        i * cell_size + cell_size // 2,
        fill="black",
        tag="minotaurus",
        outline="lightgrey"
    )

    # Horns (mask)
    canvas.create_oval(
        j * cell_size + cell_size // 5,
        i * cell_size,
        j * cell_size + cell_size // 5 * 4,
        i * cell_size + cell_size // 4,
        fill="lightgrey",
        tag="minotaurus",
        outline=""
    )

    # Body
    canvas.create_oval(
        j * cell_size + cell_size // 2 - minotaurus_size // 2,
        i * cell_size + cell_size // 2 - minotaurus_size // 2,
        j * cell_size + cell_size // 2 + minotaurus_size // 2,
        i * cell_size + cell_size // 2 + minotaurus_size // 2,
        fill="black",
        tag="minotaurus"
    )

    # Eyes
    canvas.create_oval(
        j * cell_size + cell_size // 2 - minotaurus_size // 3,
        i * cell_size + cell_size // 2 - minotaurus_size // 4,
        j * cell_size + cell_size // 2 - minotaurus_size // 8,
        i * cell_size + cell_size // 2,
        fill="red",
        tag="minotaurus"
    )

    canvas.create_oval(
        j * cell_size + cell_size // 2 + minotaurus_size // 8,
        i * cell_size + cell_size // 2 - minotaurus_size // 4,
        j * cell_size + cell_size // 2 + minotaurus_size // 3,
        i * cell_size + cell_size // 2,
        fill="red",
        tag="minotaurus"
    )

def draw_path_segment(source, target, canvas, cell_size, offset_rows=1, offset_cols=1):
    """
    Render a path segment using tkinter.
    """
    canvas.create_line(
        (source[1] + offset_cols) * cell_size + cell_size // 2,
        (source[0] + offset_rows) * cell_size + cell_size // 2,
        (target[1] + offset_cols) * cell_size + cell_size // 2,
        (target[0] + offset_rows) * cell_size + cell_size // 2,
        fill="green",
        width=5,
        tag="path"
    )

def draw_row_col_numbers(maze, canvas, cell_size, offset_rows=1, offset_cols=1):
    """
    Render row and column numbers using tkinter.
    """
    rows, cols = get_maze_size(maze)
    for i in range(rows):
        canvas.create_text(
            (offset_cols - 0.5) * cell_size,
            (i + offset_rows + 0.5) * cell_size,
            text=str(i),
            font="Arial 10",
            anchor="e"
        )
    for j in range(cols):
        canvas.create_text(
            (j + offset_cols + 0.5) * cell_size,
            (offset_rows - 0.5) * cell_size,
            text=str(j),
            font="Arial 10",
            anchor="n"
        )


if __name__ == "__main__":
    random.seed(0)
    rows, cols = 15, 10
    cell_size = 50
    red_gem_count = 5
    blue_gem_count = 5
    blue_gem_coords = random.sample([(i, j) for i in range(rows) for j in range(cols)], blue_gem_count)
    red_gem_coords = random.sample([(i, j) for i in range(rows) for j in range(cols)], red_gem_count)
    maze = create_maze(rows, cols, (0, 0), 0.2)

    # Create a window
    root = tk.Tk()
    root.title("Maze")

    # Create a canvas
    canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size)
    canvas.pack()

    draw_maze(maze, canvas=canvas, cell_size=cell_size)
    draw_gems(blue_gem_coords, red_gem_coords, canvas, cell_size // 2, cell_size)

    # Run the main loop
    root.mainloop()
