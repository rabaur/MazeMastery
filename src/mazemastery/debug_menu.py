import tkinter as tk
from typing import TYPE_CHECKING

import mazemastery.api as api
from mazemastery.state import State
from mazemastery.styles import Styles
from mazemastery.types import Renderer


class DebugMenu:
    def __init__(self, renderer: Renderer):
        # These buttons are used to modify the maze state in debug mode
        self.api_buttons = {
            "put_red_gem": tk.Button(
                renderer.root,
                text="put_red_gem(pos)",
                command=self.handle_put_red_gem_button,
            ),
            "put_blue_gem": tk.Button(
                renderer.root,
                text="put_blue_gem(pos)",
                command=self.handle_put_blue_gem_button,
            ),
            "found_minotaur": tk.Button(renderer.root, text="stop()"),
        }

        # These buttons are used to navigate the maze in debug mode
        self.nav_buttons = {
            "up": tk.Button(
                renderer.root, text="↑", command=lambda: self.handle_nav_button((-1, 0))
            ),
            "left": tk.Button(
                renderer.root, text="←", command=lambda: self.handle_nav_button((0, -1))
            ),
            "right": tk.Button(
                renderer.root, text="→", command=lambda: self.handle_nav_button((0, 1))
            ),
            "down": tk.Button(
                renderer.root, text="↓", command=lambda: self.handle_nav_button((1, 0))
            ),
            "info": tk.Button(renderer.root, text="set_pos", state=tk.DISABLED),
        }

        # These labels are used to display the current state of the maze
        self.state_labels = {
            "has_red_gem": tk.Label(renderer.root, text="has_red_gem(pos)"),
            "has_blue_gem": tk.Label(renderer.root, text="has_blue_gem(pos)"),
            "was_found": tk.Label(renderer.root, text="is_searching()"),
        }
        self.max_button_width = max(
            [len(button["text"]) for button in self.api_buttons.values()]
            + [len(label["text"]) for label in self.state_labels.values()]
        )

        # Pressing this button transfers the user into debug mode.
        self.debug_button = tk.Button(
            renderer.root, text="Debug", command=self.handle_debug_button
        )
        self.debug_button.configure(**Styles.debug_button_style(renderer.cell_size))

        row_idx = 1
        self.debug_button.grid(
            row=row_idx, column=1, columnspan=3, sticky="nswe", padx=5, pady=5
        )
        row_idx += 1
        for button in self.api_buttons.values():
            # Configure common attributes
            button.configure(**Styles.active_button_style(renderer.cell_size))
            button.grid(
                row=row_idx, column=1, columnspan=3, sticky="nswe", padx=5, pady=5
            )
            row_idx += 1

        # Styling for the navigation buttons
        for button in self.nav_buttons.values():
            button.configure(**Styles.nav_button_style(renderer.cell_size))

        # Positioning navigation buttons
        self.nav_buttons["up"].grid(row=row_idx, column=2, sticky="nswe")
        row_idx += 1
        self.nav_buttons["left"].grid(row=row_idx, column=1, sticky="nswe")
        self.nav_buttons["info"].grid(row=row_idx, column=2, sticky="nswe")
        self.nav_buttons["right"].grid(row=row_idx, column=3, sticky="nswe")
        row_idx += 1
        self.nav_buttons["down"].grid(row=row_idx, column=2, sticky="nswe")
        row_idx += 1

        for label in self.state_labels.values():
            label.configure(**Styles.label_style(renderer.cell_size))
            label.grid(row=row_idx, column=1, columnspan=3, sticky=tk.W)
            row_idx += 1

        self.renderer = renderer

    def update_menu(self) -> None:
        """
        Beware - this can only be called after initialization of the renderer
        due to an ugly circular dependency between the renderer and the api.
        TODO: Fix this.
        """
        if not self:
            return
        if self.renderer.debug:
            self.debug_button.configure(text="Exit Debug Mode")
            for key, button in {**self.api_buttons, **self.nav_buttons}.items():
                # If there is already a blue gem or a red gem, putting another blue gem is not valid.
                if key == "put_blue_gem" and (
                    api.has_blue_gem(api.get_pos()) or api.has_red_gem(api.get_pos())
                ):
                    print(
                        "disabling put_blue_gem(pos) since there is already a blue gem or a red gem at pos"
                    )
                    button.configure(state=tk.DISABLED, relief=tk.FLAT)
                elif key == "put_red_gem" and (api.has_red_gem(api.get_pos())):
                    button.configure(state=tk.DISABLED, relief=tk.FLAT)
                elif key == "info":
                    button.configure(state=tk.NORMAL, relief=tk.FLAT)
                else:
                    button.configure(state=tk.NORMAL, relief=tk.RAISED)
        else:
            self.debug_button.configure(text="Debug")
            for key, button in {**self.api_buttons, **self.nav_buttons}.items():
                button.configure(state=tk.DISABLED, relief=tk.FLAT)

    def handle_put_red_gem_button(self) -> None:
        api.put_red_gem()
        self.renderer.draw_gems()
        self.update_menu()

    def handle_put_blue_gem_button(self) -> None:
        api.put_blue_gem()
        self.renderer.draw_gems()
        self.update_menu()

    def handle_debug_button(self) -> None:
        self.renderer.debug = not self.renderer.debug
        state = State()
        if self.renderer.debug:
            self.renderer.draw_cloud(api.get_pos())
            self.renderer.draw_hearts(num=state.initial_lives, filled=state.lives)
        else:
            self.renderer.canvas.delete("cloud")
        self.update_menu()

    def handle_nav_button(self, dir: tuple[int, int]) -> None:
        """
        We cannot use the api call 'set_pos' here because if otherwise the current
        thread will run into the while loop that only resolves once we leave
        debug mode. Leaving debug mode will not possible anymore because the
        current thread is blocked.
        """
        state = State()
        if state.dead:
            return
        old_pos = api.get_pos()
        new_pos = (old_pos[0] + dir[0], old_pos[1] + dir[1])
        if new_pos not in state.maze[old_pos]:
            state.lives -= 1
            new_pos = old_pos
        if state.lives == 0:
            state.renderer.draw_popup("You died!")
            state.dead = True
        state.pos = new_pos
        self.renderer.draw_row_col_numbers(old_pos, api.get_pos())
        self.renderer.draw_player(curr_pos=api.get_pos(), prev_pos=old_pos)
        self.renderer.draw_cloud(api.get_pos())
        self.renderer.draw_hearts(num=state.initial_lives, filled=state.lives)
        self.update_menu()
