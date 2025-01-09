from src.python.menu.menu import Menu
from src.python.settings.config import BUTTON_BASE_WIDTH, BUTTON_HEIGHT

class MainMenu(Menu):
    def __init__(self, handler, identifier, font_title, font_buttons, font_text):
        super().__init__(handler, identifier, font_title, font_buttons, font_text)
        self.create_buttons()

    def create_buttons(self):
        translations = self.handler.config.translations
        self.button_definitions = [
            {"identifier": "play_button", "text": translations['play_button'],
             "callback": lambda: self.handler.change_menu("game_mode")},
            {"identifier": "settings", "text": translations['settings'],
             "callback": lambda: self.handler.change_menu("settings")},
            {"identifier": "exit_button", "text": translations['exit_button'], "callback": self.handler.quit_game}
        ]
        positions = self.calculate_positions(self.handler.config.screen_width, self.handler.config.screen_height)
        for i, definition in enumerate(self.button_definitions):
            definition.update({
                "x": positions[i][0], "y": positions[i][1],
                "width": BUTTON_BASE_WIDTH, "height": BUTTON_HEIGHT,
                "theme": self.handler.theme
            })
        self.create_buttons_from_definitions(self.button_definitions)

    def calculate_positions(self, screen_width, screen_height):
        x_offset = (screen_width - BUTTON_BASE_WIDTH) // 2
        start_y = screen_height // 3
        spacing_y = 70
        return [(x_offset, start_y + i * spacing_y) for i in range(len(self.button_definitions))]

    def draw_title(self):
        if self.title:
            shadow_surf1 = self.title_font.render(self.title, True, self.handler.theme["title_shadow"])
            shadow_rect1 = shadow_surf1.get_rect(center=(self.handler.config.screen_width // 2 + 2, 102))
            self.handler.surface.blit(shadow_surf1, shadow_rect1)

            title_surf = self.title_font.render(self.title, True, self.handler.theme["title"])
            title_rect = title_surf.get_rect(center=(self.handler.config.screen_width // 2, 100))
            self.handler.surface.blit(title_surf, title_rect)