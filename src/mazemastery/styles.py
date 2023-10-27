import tkinter as tk

from mazemastery.types import ColorDict


class Colors:
    green_base = "#4b9a49"
    green_border = "#316e30"
    grass_base = "#64b663"
    grass_top = "#a6d5a5"
    brown_base = "#81755a"
    brown_highlight = "#b4a993"
    brown_border = "#544d3b"
    cloud = "#eff4f5"
    blues: ColorDict = {
        0: "#0069aa",
        1: "#0098dc",
        2: "#00cdf9",
        3: "#94fdff",
        4: "#ffffff",
        "main": "#0cf1ff",
    }
    reds: ColorDict = {
        -1: "#421a1e",
        0: "#9d2231",
        1: "#e12937",
        2: "#ff5858",
        3: "#ff9ba2",
        4: "#ffffff",
        "main": "#ff616b",
    }


class Styles:
    @staticmethod
    def active_button_style(cell_size: int) -> dict:
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
    def nav_button_style(cell_size: int) -> dict:
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
    def label_style(cell_size: int) -> dict:
        return {
            "font": f"Courier {cell_size // 4}",
            "height": 1,
            "background": Colors.brown_highlight,
            "fg": Colors.brown_border,
            "justify": tk.LEFT,
            "anchor": tk.W,
        }

    @staticmethod
    def debug_button_style(cell_size: int) -> dict:
        return {
            "font": f"Arial {cell_size // 4}",
            "height": 1,
            "borderwidth": 10,
            "anchor": tk.CENTER,
        }
