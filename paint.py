import sys
import os
import pickle

from random import randint
from copy import deepcopy

os.environ["SDL_VIDEO_CENTERED"] = "1"

import pgzrun
import pygame
import subprocess

DEFAULT_SIZE = (800, 600)


def get_primary_screen_resolution() -> tuple[int, int]:
    """
    Read the primary screen resolution from xrandr and returns it as a tuple.
    If the "xrandr" command fails, returns a default pair (800, 600)
    It's used to set the window to full resolution.
    """
    try:
        # Run the xrandr command and capture the output
        result = subprocess.run(
            ["xrandr"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        # Check for errors
        if result.returncode != 0:
            print(f"xrandr command failed: {result.stderr}")
            return DEFAULT_SIZE

        # Parse the output to find the primary screen resolution
        for line in result.stdout.splitlines():
            if "primary" in line:
                parts = line.split()
                for part in parts:
                    if "x" in part and part.replace("x", "")[0].isdigit():
                        width, height = part.split("x")
                        height = height.split("+")[0]
                        width = int(width)
                        height = int(height)
                        return width, height

        raise ValueError("Primary screen resolution not found in xrandr output.")
    except Exception as error:
        print(f"Error reading the screen resolution: {error}")
        return DEFAULT_SIZE


WIDTH, HEIGHT = get_primary_screen_resolution()
TITLE = "PAINT"
HELP = """PAINT: a basic paint in python + pygame zero.

Usage: python paint.py [OPTIONS]

Options:

saves/save_004.paint        load the save file 
-h, --help                  prints this help and exits

Keybindings:
    - Q or Escape exits,
    - Return: save a numbered screenshot in "./img"
    - Space: erase the last line
    - T: toggle the colors between fullwhite and random
    - R: reverse the colors (black on white / white on black)
    - S: save the current drawing to a file 
    - L: load the last saved drawing. See Options 
    - C: clear the screen
    """


class Color:
    """
    Generate random or White colors.
    It's useful to toggle the colors between full white and random.
    """

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self):
        self.is_random = True
        self.is_white_on_black = True

    def toggle_random(self):
        self.is_random = not self.is_random

    def get(self) -> tuple[int, int, int]:
        if self.is_random:
            return self.random_color()
        else:
            return self.WHITE

    def reverse(self):
        """
        Reverse all colors and display every line in black.
        Useful to take printable screenshots.
        """
        self.is_white_on_black = not self.is_white_on_black

    @staticmethod
    def random_color():
        return (
            randint(100, 255),
            randint(100, 255),
            randint(100, 255),
        )


def init_lines() -> list[list]:
    """
    Initialise the lines.
    - empty if no filename were provided
    - from the given filename otherwize.
    """
    if len(sys.argv) == 1:
        return []
    elif sys.argv[1] in ("-h", "--help"):
        print(HELP)
        exit()
    else:
        savefile = sys.argv[1]
        try:
            return load(savefile)
        except Exception as error:
            print(f"Error loading {savefile}: {error}")
            return []


def save() -> None:
    """
    Save the current drawing in ./saves/save_{xyz}.paint
    where {xyz} is a 3 digits number. Should always save to a new file.
    """
    index = get_last_save_index() + 1
    savefile = f"./saves/save_{index:03d}.paint"
    with open(savefile, "wb") as f:
        pickle.dump(lines, f)
        print(f"Saved {savefile}")


def load_last_save() -> None:
    """
    Load the last drawing in ./saves/
    """
    index = get_last_save_index()
    savefile = f"./saves/save_{index:03d}.paint"
    saved_lines = load(savefile)
    lines.clear()
    lines.extend(saved_lines)


def load(savefile: str) -> list[list]:
    """Read and returns the content of a savefile."""
    with open(savefile, "rb") as f:
        content = pickle.load(f)
        if not isinstance(content, list):
            raise ValueError("Invalid savefile ", savefile)
        print(f"Loaded {savefile}")
        return content


def save_screenshot() -> None:
    """Save a numbered screenshot in ./img"""
    index = get_last_screenshot_index() + 1
    screenshot_filename = f"img/screenshot_{index:03d}.jpg"
    pygame.image.save(screen.surface, screenshot_filename)
    print(f"Screenshot {screenshot_filename}")


def get_last_screenshot_index() -> int:
    """
    Returns the last used index of screenshots.
    Screenshots are saved in "./img/" and their filenames are "screenshot_{xyz}.jpg"
    where xyz is a 3 digits integer: screenshot_000.jpg, screenshot_001.jpg etc.
    It returns the last index as an integer.
    """
    numbers = (
        int(filename.removeprefix("screenshot_").removesuffix(".jpg"))
        for filename in os.listdir("./img/")
        if filename.startswith("screenshot_") and filename.endswith(".jpg")
    )

    return max(numbers)


def get_last_save_index() -> int:
    """
    Returns the last used index of save.
    Save files are saved in "./saves/" and their filenames are "save_{xyz}.jpg"
    where xyz is a 3 digits integer: save_000.jpg, save_001.jpg etc.
    It returns the last index as an integer.
    """
    numbers = (
        int(filename.removeprefix("save_").removesuffix(".paint"))
        for filename in os.listdir("./saves/")
        if filename.startswith("save_") and filename.endswith(".paint")
    )

    return max(numbers)


def draw_line(line: list) -> None:
    """A "line" is a list with:
    - a color (tuple of 3 integers),
    - a bunch of points (list of 2 integers)
    We draw each point as a filled circle of radius 10 with color.
    """
    line_color = line[0] if color.is_white_on_black else Color.BLACK
    for point in line[1:]:
        screen.draw.filled_circle(point, 8, line_color)


def update():
    """Empty function, logic is done in on_mouse_something functions."""
    pass


def draw():
    """Clear the screen and draw every line"""
    screen.fill(Color.BLACK if color.is_white_on_black else Color.WHITE)
    for line in lines:
        draw_line(line)
    if current_line:
        draw_line(current_line)


def on_key_down(key):
    on_key_down.__doc__ = HELP

    if key == keys.Q or key == keys.ESCAPE:
        exit()
    if key == keys.RETURN:
        save_screenshot()
    if key == keys.T:
        color.toggle_random()
    if key == keys.C:
        lines.clear()
    if key == keys.R:
        color.reverse()
    if key == keys.S:
        save()
    if key == keys.L:
        load_last_save()
    if key == keys.SPACE:
        if lines:
            lines.pop()


def on_mouse_down(pos):
    """When mouse button is pressed, a new randomly colored line is created at current position"""
    current_line.append(color.get())
    current_line.append(pos)


def on_mouse_move(pos):
    """
    When mouse is moved, if a current line
    is created (aka if mouse is pressed),
    we push the current position to the line.
    """
    if current_line:
        current_line.append(pos)


def on_mouse_up(pos):
    """
    When mouse button is released, we end the current line and copy its elements in the lines.
    Current line is cleared.
    """
    lines.append(deepcopy(current_line))
    current_line.clear()


lines = init_lines()
current_line = []
color = Color()
print(HELP)

pgzrun.go()
