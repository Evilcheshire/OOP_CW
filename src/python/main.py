import pygame
from src.python.settings.config import FONT_BASE, INI_PATH
from src.python.menu.menu_handler import MenuHandler
from src.python.settings.config_manager import ConfigManager

def main():
    pygame.init()

    config = ConfigManager(INI_PATH)
    screen = pygame.display.set_mode((config.screen_width, config.screen_height))
    pygame.display.set_caption("Hackenbush")

    font_buttons = pygame.font.Font(FONT_BASE, 30)
    font_text = pygame.font.Font(FONT_BASE, 20)
    font_title = pygame.font.Font(FONT_BASE, 45)

    menu_handler = MenuHandler(screen, config, font_title, font_buttons, font_text)

    menu_handler.run()

if __name__ == "__main__":
    main()