import pygame

from src.python.settings.config import LIGHT_THEME, DARK_THEME, FPS
from src.python.ui.button import Button
from src.python.ui.circle_button import CircleButton
from src.python.ui.info_window import InfoWindow

class Menu:
    def __init__(self, handler, identifier, font_title, font_buttons, font_text):
        self.handler = handler
        self.running = True
        self.identifier = identifier
        self.title = self.handler.config.translations[identifier]
        self.title_font = font_title
        self.button_font = font_buttons
        self.text_font = font_text
        self.button_definitions = []
        self.buttons = []

        self.info_window = None

        self.update_theme("light" if self.handler.config.get("General", "theme", "light") == "light" else "dark")

        self.info_window = InfoWindow(
            self.handler.config.translations['info_window_text'],
            font_text, 620, 190,
            self.handler.config.screen_width,
            self.theme
        )

    def update_theme(self, theme_name):
        self.theme = LIGHT_THEME if theme_name == "light" else DARK_THEME
        self.background_color = self.theme['background']
        self.title_color = self.theme['title']
        for button in self.buttons:
            button.update_theme(self.theme)
        if self.info_window:
            self.info_window.update_theme(self.theme)

    def create_buttons(self):
        pass

    def update_texts(self):
        self.title = self.handler.config.translations[self.identifier]
        self.info_window.text = self.handler.config.translations['info_window_text']

        for button, definition in zip(self.buttons, self.button_definitions):
            if "numeric" in definition["identifier"]:
                continue
            button.text = self.handler.config.translations[definition["identifier"]]

    def update_positions(self):
        positions = self.calculate_positions(self.handler.config.screen_width, self.handler.config.screen_height)
        for i, definition in enumerate(self.button_definitions):
            self.buttons[i].original_rect.x = positions[i][0]
            self.buttons[i].original_rect.y = positions[i][1]
            self.buttons[i].rect = self.buttons[i].original_rect.copy()

        if isinstance(self.buttons[-1], CircleButton):
            circle_button = self.buttons[-1]
            circle_button.x = self.handler.config.screen_width - 50
            circle_button.y = 50

        self.info_window.update_coordinates(self.handler.config.screen_width, 80)

    def create_buttons_from_definitions(self, button_definitions):
        for i, definition in enumerate(button_definitions):
            button_type = definition.pop("button_type", "Button")
            if button_type == "Button":
                button = Button(font_buttons=self.button_font, **definition)
            elif button_type == "CircleButton":
                button = CircleButton(font_buttons=self.button_font, **definition, theme=self.theme)
            else:
                raise ValueError(f"Unsupported button type: {button_type}")
            self.buttons.append(button)

        self.buttons.append(
            CircleButton(x=self.handler.config.screen_width - 50, y=50, radius=20,
                         identifier="info_button", text="?", font_buttons=self.button_font,
                         callback=lambda: self.info_window.show(), theme=self.theme)
        )

    def calculate_positions(self, screen_width, screen_height):
        return []

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.handler.quit_game()
            for button in self.buttons:
                button.handle_event(event)
        self.info_window.update(events)

    def update(self):
        for button in self.buttons:
            button.update()

    def draw_title(self):
        if self.title:
            title_surf = self.title_font.render(self.title, True, self.handler.theme["title"])
            title_rect = title_surf.get_rect(center=(self.handler.config.screen_width // 2, 100))
            self.handler.surface.blit(title_surf, title_rect)

    def draw(self):
        self.handler.surface.fill(self.background_color)
        self.draw_title()
        for button in self.buttons:
            button.draw(self.handler.surface)
        self.info_window.draw(self.handler.surface)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)

    def stop(self):
        self.running = False
