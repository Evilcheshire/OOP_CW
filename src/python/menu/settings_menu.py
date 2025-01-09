from src.python.menu.menu import Menu
from src.python.settings.config import DARK_BLUE, BLUE, BUTTON_BASE_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING, DARK_THEME, \
    LIGHT_THEME


class SettingsMenu(Menu):
    def __init__(self, handler, identifier, font_title, font_buttons, font_text):
        super().__init__(handler, identifier, font_title, font_buttons, font_text)
        self.create_buttons()

    def create_buttons(self):
        translations = self.handler.config.translations
        self.button_definitions = [
            {"identifier": "numeric", "text": "800x600",
             "callback": lambda: self.change_screen_size(800, 600)},
            {"identifier": "numeric", "text": "1024x768",
             "callback": lambda: self.change_screen_size(1024, 768)},
            {"identifier": "theme", "text": translations['theme'], "callback": self.toggle_theme},
            {"identifier": "language", "text": translations['language'], "callback": self.toggle_language},
            {"identifier": "back_button", "text": translations['back_button'],
             "callback": lambda: self.handler.change_menu("main")}
        ]
        positions = self.calculate_positions(self.handler.config.screen_width, self.handler.config.screen_height)
        for i, definition in enumerate(self.button_definitions):
            definition.update({"x": positions[i][0], "y": positions[i][1],
                               "width": BUTTON_BASE_WIDTH, "height": BUTTON_HEIGHT,
                                "theme": self.handler.theme})
        self.create_buttons_from_definitions(self.button_definitions)

    def calculate_positions(self, screen_width, screen_height):
        x_offset = (screen_width - BUTTON_BASE_WIDTH) // 2
        start_y = screen_height // 3
        spacing_y = 70
        return [(x_offset, start_y + i * spacing_y) for i in range(len(self.button_definitions))]

    def change_screen_size(self, width, height):
        self.handler.config.set_screen_size(width, height)
        self.handler.change_resolution()

    def toggle_language(self):
        current_language = self.handler.config.get('General', 'language', 'en')
        new_language = 'uk' if current_language == 'en' else 'en'
        self.handler.config.set_language(new_language)
        self.handler.change_language(new_language)

    def toggle_theme(self):
        current_theme = self.handler.config.get_theme()
        new_theme = "dark" if current_theme == "light" else "light"
        self.handler.config.set_theme(new_theme)
        self.handler.theme = DARK_THEME if new_theme == "dark" else LIGHT_THEME
        self.handler.update_theme()
        self.handler.current_menu.draw()