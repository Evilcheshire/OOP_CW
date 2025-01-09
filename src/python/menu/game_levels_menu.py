from src.python.menu.menu import Menu
from src.python.settings.config import BLUE, DARK_BLUE, BUTTON_LONG_WIDTH, BUTTON_BASE_WIDTH, BUTTON_SHORT_WIDTH, BUTTON_HEIGHT
from src.python.game.game_handler import HackenbushGame

class GameLevelsMenu(Menu):
    def __init__(self, handler, identifier, font_title, font_buttons, font_text):
        super().__init__(handler, identifier, font_title, font_buttons, font_text)
        self.create_buttons()

    def create_buttons(self):
        self.button_definitions = [
            {"identifier": f"numeric", "text": str(i + 1),
             "callback": lambda level=i: self.start_game(level),
             "width": BUTTON_SHORT_WIDTH}
            for i in range(9)
        ]

        translations = self.handler.config.translations
        self.button_definitions += [
            {"identifier": "back_button", "text": translations["back_button"],
             "callback": lambda: self.handler.change_menu("game_mode"),
             "width": BUTTON_BASE_WIDTH},
            {"identifier": "back_to_menu_button", "text": translations["back_to_menu_button"],
             "callback": lambda: self.handler.change_menu("main"),
             "width": BUTTON_LONG_WIDTH},
        ]

        positions = self.calculate_positions(self.handler.config.screen_width, self.handler.config.screen_height)
        for i, definition in enumerate(self.button_definitions):
            definition.update({"x": positions[i][0], "y": positions[i][1],
                "height": BUTTON_HEIGHT, "theme": self.handler.theme}, )
        self.create_buttons_from_definitions(self.button_definitions)

    def calculate_positions(self, screen_width, screen_height):
        spacing_x, spacing_y = 30, 30
        start_x = (screen_width - 510) // 2
        start_y = screen_height // 3
        positions = []

        for i in range(9):
            row, col = divmod(i, 3)
            positions.append((start_x + col * (BUTTON_SHORT_WIDTH + spacing_x),
                              start_y + row * (BUTTON_HEIGHT + spacing_y)))

        back_button_y = start_y + 3 * (BUTTON_HEIGHT + spacing_y) + spacing_y
        center_x = (screen_width -  (BUTTON_BASE_WIDTH + BUTTON_LONG_WIDTH + spacing_x)) // 2

        positions.append((center_x, back_button_y))
        positions.append((center_x + BUTTON_BASE_WIDTH + spacing_x, back_button_y))

        return positions

    def start_game(self, level):
        mode = self.handler.previous_menu.selected_mode
        game_handler = HackenbushGame(self.handler.surface, self.handler.config, self.text_font, mode, level)
        game_handler.run()
        self.handler.change_menu("main")