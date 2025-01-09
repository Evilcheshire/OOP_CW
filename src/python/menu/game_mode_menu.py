from src.python.menu.menu import Menu
from src.python.settings.config import BUTTON_LONG_WIDTH, BUTTON_BASE_WIDTH, BUTTON_HEIGHT


class GameModeMenu(Menu):
    def __init__(self, handler, identifier, font_title, font_buttons, font_text):
        super().__init__(handler, identifier, font_title, font_buttons, font_text)
        self.create_buttons()

    def create_buttons(self):
        translations = self.handler.config.translations
        self.button_definitions = [
            {"identifier": "game_mode1_button", "text": translations['game_mode1_button'],
             "callback": self.select_computer_mode,
             "width": BUTTON_LONG_WIDTH, "height": BUTTON_HEIGHT},
            {"identifier": "game_mode2_button", "text": translations['game_mode2_button'],
             "callback": self.select_player_mode,
             "width": BUTTON_LONG_WIDTH, "height": BUTTON_HEIGHT},
            {"identifier": "back_button", "text": translations['back_button'],
             "callback": lambda: self.handler.change_menu("main"),
             "width": BUTTON_BASE_WIDTH, "height": BUTTON_HEIGHT}
        ]
        positions = self.calculate_positions(self.handler.config.screen_width, self.handler.config.screen_height)
        for i, definition in enumerate(self.button_definitions):
            definition.update({"x": positions[i][0], "y": positions[i][1], "height": BUTTON_HEIGHT,
                "theme": self.handler.theme
            })
        self.create_buttons_from_definitions(self.button_definitions)

    def calculate_positions(self, screen_width, screen_height):
        start_y = screen_height // 3
        spacing_y = 70
        positions = []

        for i, button_params in enumerate(self.button_definitions):
            button_width = button_params["width"]
            x_offset = (screen_width - button_width) // 2
            positions.append((x_offset, start_y + i * spacing_y))

        return positions

    def select_computer_mode(self):
        self.selected_mode = "computer"
        self.handler.change_menu("game_levels")

    def select_player_mode(self):
        self.selected_mode = "player"
        self.handler.change_menu("game_levels")
