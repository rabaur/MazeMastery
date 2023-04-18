import tkinter as tk
import random
from maze import create_maze
from utils import get_maze_size

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
                    fill="red"
                )
            if not (i, j - 1) in maze[(i, j)]:  # Western neighbor missing
                canvas.create_line(
                    j * cell_size,
                    i * cell_size,
                    j * cell_size,
                    (i + 1) * cell_size,
                    width=wall_width,
                    fill="green"
                )
            if not (i, j + 1) in maze[(i, j)]:  # Eastern neighbor missing
                canvas.create_line(
                    (j + 1) * cell_size,
                    i * cell_size,
                    (j + 1) * cell_size,
                    (i + 1) * cell_size,
                    width=wall_width,
                    fill="blue"
                )
            if not (i + 1, j) in maze[(i, j)]:  # Southern neighbor missing
                canvas.create_line(
                    j * cell_size,
                    (i + 1) * cell_size,
                    (j + 1) * cell_size,
                    (i + 1) * cell_size,
                    width=wall_width,
                    fill="yellow"
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
            fill="grey"
        )
    for j in range(n):
        canvas.create_line(
            j * cell_size,
            0,
            j * cell_size,
            m * cell_size,
            width=grid_width,
            fill="grey"
        )


def render_maze(maze, cell_size=50, wall_width=5, grid_width=1):
    """
    Render a maze using tkinter.
    """

    m, n = get_maze_size(maze)
    root = tk.Tk()
    root.title("Maze")
    canvas = tk.Canvas(root, width=n * cell_size, height=m * cell_size)
    canvas.pack()

    draw_grid(maze, cell_size, grid_width, canvas)
    draw_walls(maze, cell_size, wall_width, canvas)

    root.mainloop()


if __name__ == "__main__":
    random.seed(0)
    maze = create_maze(15, 10, (0, 0), 1.0)
    render_maze(maze, 50)
