import tkinter as tk


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


class Styles:
    @staticmethod
    def active_button_style(cell_size):
        return {
            "font": f"Courier {cell_size // 4}",
            "height": 1,
            "background": Colors.green_base,
            "activebackground": Colors.green_border,
            "foreground": "white",
            "activeforeground": "white",
            "borderwidth": 10,
            "justify": tk.LEFT,
            "anchor": tk.W,
            "relief": tk.RAISED,
            "padx": 5,
            "pady": 5,
        }

    @staticmethod
    def nav_button_style(cell_size):
        return {
            "font": f"Courier {cell_size // 4}",
            "height": 1,
            "background": Colors.green_base,
            "activebackground": Colors.green_border,
            "foreground": "white",
            "activeforeground": "white",
            "borderwidth": 10,
            "relief": tk.RAISED,
        }

    @staticmethod
    def label_style(cell_size):
        return {
            "font": f"Courier {cell_size // 4}",
            "height": 1,
            "background": Colors.brown_highlight,
            "fg": Colors.brown_border,
            "justify": tk.LEFT,
            "anchor": tk.W,
        }

    @staticmethod
    def debug_button_style(cell_size):
        return {
            "font": f"Arial {cell_size // 4}",
            "height": 1,
            "borderwidth": 10,
            "anchor": tk.CENTER,
        }
