import os
from random import randint
from copy import deepcopy

os.environ["SDL_VIDEO_CENTERED"] = "1"

import pgzrun
import pygame

WIDTH = 800
HEIGHT = 600
WIDTH = 1920
HEIGHT = 1080
TITLE = "PAINT"

HELP = """HELP :
    - Q or Escape exits,
    - Return: save a numbered screenshot in "./img"
    - Space: erase the last line
    - T: toggle the colors between fullwhite and random
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


def draw_line(line: list) -> None:
    """A "line" is a list with:
    - a color (tuple of 3 integers),
    - a bunch of points (list of 2 integers)
    We draw each point as a filled circle of radius 10 with color.
    """
    line_color = line[0] if color.is_white_on_black else Color.BLACK
    for point in line[1:]:
        screen.draw.filled_circle(point, 10, line_color)


def update():
    """Empty function, logic is made in on_mouse_something functions."""
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


lines = []
current_line = []
color = Color()

print(HELP)
pgzrun.go()
