# PAINT

A basic paint in python + pygame zero.

Made for a child or someone who just wants to draw something quickly without worrying about anything.

You can

- toggle light/dark (light has only black colors, may change)
- toggle the random colors and use only white (for serious peoples...)
- Save a screenshot,
- Load a savefile,
- Undo (no redo lol)
- Clear the screen

## Example

![Screenshot](./img/screenshot_001.jpg)

## Installation:

Clone this repository and install the requirements:

```bash
$ pip install -r requirements.txt
```

## Help:

```sh
Usage: python paint.py [OPTIONS]

Options:

saves/save_004.paint            load the save file
-h, --help                      prints this help and exits

Keybindings:

- Q or Escape exits,
- Return: save a numbered screenshot in "./img"
- Space: erase the last line
- T: toggle the colors between fullwhite and random
- R: reverse the colors (black on white / white on black)
- S: save the current drawing to a file
- L: load the last saved drawing. See Options
- C: clear the screen
```

## TODO

- Erase button with right click...
- Interface
