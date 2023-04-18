import tkinter as tk
import random
from minosrecurse.maze import create_maze
from minosrecurse.utils import get_maze_size

def draw_walls(maze, cell_size, wall_width, canvas):
    m, n = get_maze_size(maze)

    for i in range(m):
        for j in range(n):
            if not (i - 1, j) in maze[(i, j)]:  # Northern neighbor missing
                canvas.create_line(
                    j * cell_size,
                    i * cell_size,
                    (j + 1) * cell_size,
                    i * cell_size,
                    width=wall_width,
                    fill="black",
                    tag="wall"
                )
            if not (i, j - 1) in maze[(i, j)]:  # Western neighbor missing
                canvas.create_line(
                    j * cell_size,
                    i * cell_size,
                    j * cell_size,
                    (i + 1) * cell_size,
                    width=wall_width,
                    fill="black",
                    tag="wall"
                )
            if not (i, j + 1) in maze[(i, j)]:  # Eastern neighbor missing
                canvas.create_line(
                    (j + 1) * cell_size,
                    i * cell_size,
                    (j + 1) * cell_size,
                    (i + 1) * cell_size,
                    width=wall_width,
                    fill="black",
                    tag="wall"
                )
            if not (i + 1, j) in maze[(i, j)]:  # Southern neighbor missing
                canvas.create_line(
                    j * cell_size,
                    (i + 1) * cell_size,
                    (j + 1) * cell_size,
                    (i + 1) * cell_size,
                    width=wall_width,
                    fill="black",
                    tag="wall"
                )

def draw_grid(maze, cell_size, grid_width, canvas):
    m, n = get_maze_size(maze)
    for i in range(m):
        canvas.create_line(
            0,
            i * cell_size,
            n * cell_size,
            i * cell_size,
            width=grid_width,
            fill="grey",
            tag="grid"
        )
    for j in range(n):
        canvas.create_line(
            j * cell_size,
            0,
            j * cell_size,
            m * cell_size,
            width=grid_width,
            fill="grey",
            tag="grid"
        )


def draw_maze(maze, canvas, cell_size=50, wall_width=5, grid_width=1):
    """
    Render a maze using tkinter.
    """
    draw_grid(maze, cell_size, grid_width, canvas)
    draw_walls(maze, cell_size, wall_width, canvas)

def draw_gems(blue_gem_coords, red_gem_coords, canvas, gem_size, cell_size):
    """
    Render gems using tkinter.
    """
    canvas.delete("gem") # delete old gems
    for i, j in blue_gem_coords:
        canvas.create_oval(
            j * cell_size + cell_size // 2 - gem_size // 2,
            i * cell_size + cell_size // 2 - gem_size // 2,
            j * cell_size + cell_size // 2 + gem_size // 2,
            i * cell_size + cell_size // 2 + gem_size // 2,
            fill="blue",
            tag="gem"
        )
    for i, j in red_gem_coords:
        canvas.create_oval(
            j * cell_size + cell_size // 2 - gem_size // 2,
            i * cell_size + cell_size // 2 - gem_size // 2,
            j * cell_size + cell_size // 2 + gem_size // 2,
            i * cell_size + cell_size // 2 + gem_size // 2,
            fill="red",
            tag="gem"
        )

def draw_minotaurus(minotaurus_coords, canvas, minotaurus_size, cell_size):
    """
    Render minotaurus using tkinter.
    """
    canvas.delete("minotaurus") # delete old minotaurus
    i, j = minotaurus_coords

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
