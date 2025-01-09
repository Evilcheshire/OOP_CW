import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CREAM = (253, 246, 236)
DARK_CREAM = (222, 203, 175)
BLUE = (50, 175, 194)
RED = (146, 5, 5)
DARK_BLUE = (21, 72, 81)
DARK_RED = (79, 3, 3)

LIGHT_THEME = {
    "background": CREAM,
    "title": BLUE,
    "title_shadow": DARK_BLUE,
    "text": DARK_BLUE,
    "button": WHITE,
    "button_text": DARK_BLUE,
    "button_hover": BLUE,
    "button_outline": DARK_BLUE,
    "button_hover_text": CREAM,
    "polygon": DARK_BLUE,
    "red": RED,
    "blue": BLUE,
    "info_window_bg": WHITE,
    "info_window_border": BLUE,
    "info_window_text": DARK_BLUE,
}

DARK_THEME = {
    "background": CREAM,
    "title": RED,
    "title_shadow": DARK_RED,
    "text": DARK_RED,
    "button": WHITE,
    "button_text": DARK_RED,
    "button_hover": RED,
    "button_outline": DARK_RED,
    "button_hover_text": CREAM,
    "polygon": DARK_RED,
    "red": RED,
    "blue": BLUE,
    "info_window_bg": WHITE,
    "info_window_border": RED,
    "info_window_text": DARK_RED,
}

BUTTON_SHORT_WIDTH = 150
BUTTON_BASE_WIDTH = 250
BUTTON_LONG_WIDTH = 390
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20

EDGE_WIDTH = 5

FONT_COLOR = DARK_BLUE
FONT_BASE = os.path.join(BASE_DIR, 'lib', 'assets', 'OffBit-Bold.ttf')

GRAPHS_PATH = os.path.join(BASE_DIR, 'lib', 'graphs', 'graphs.json')
INI_PATH = os.path.join(BASE_DIR, 'settings.ini')
