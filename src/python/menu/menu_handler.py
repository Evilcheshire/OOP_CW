import os
import sys
import pygame

from src.python.menu.game_levels_menu import GameLevelsMenu
from src.python.menu.game_mode_menu import GameModeMenu
from src.python.menu.main_menu import MainMenu
from src.python.menu.settings_menu import SettingsMenu
from src.python.settings.config import DARK_THEME, LIGHT_THEME


class MenuHandler:
    def __init__(self, surface, config, font_title, font_buttons, font_text):
        self.config = config
        self.surface = surface
        self.font_title = font_title
        self.font_buttons = font_buttons
        self.font_text = font_text
        self.theme = LIGHT_THEME if self.config.get_theme() == "light" else DARK_THEME

        self.menus = {
            "main": MainMenu(self, 'logo', font_title, font_buttons, font_text),
            "settings": SettingsMenu(self, 'settings', font_title, font_buttons, font_text),
            "game_mode": GameModeMenu(self, 'game_mode', font_title, font_buttons, font_text),
            "game_levels": GameLevelsMenu(self, 'level_selection', font_title, font_buttons, font_text)
        }
        self.current_menu = self.menus["main"]
        self.previous_menu = None
        self.running = True

    def change_menu(self, menu_name):
        self.previous_menu = self.current_menu
        self.current_menu.stop()
        self.current_menu = self.menus.get(menu_name)
        self.current_menu.running = True
        self.current_menu.run()

    def change_language(self, new_language):
        self.config.set_language(new_language)

        for menu in self.menus.values():
            menu.update_texts()

        self.current_menu.draw()

    def change_resolution(self):
        width, height = self.config.screen_width, self.config.screen_height
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.surface = pygame.display.set_mode((width, height))

        for menu in self.menus.values():
            menu.update_positions()

        self.current_menu.update_positions()

    def update_theme(self):
        self.theme = DARK_THEME if self.config.get_theme() == "dark" else LIGHT_THEME

        for menu in self.menus.values():
            for button in menu.buttons:
                button.color = self.theme["button"]
                button.text_color = self.theme['button_text']
                button.hover_text_color = self.theme['button_hover_text']
                button.hover_color = self.theme["button_hover"]
                button.outline_color = self.theme["button_outline"]
                button.hover_text_color = self.theme["button_hover_text"]
                button.polygon_color = self.theme["polygon"]

        self.current_menu.draw()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while self.running:
            self.current_menu.run()