import pygame
from src.python.settings.config import CREAM, DARK_BLUE, FONT_COLOR


class InfoWindow:
    def __init__(self, text, font_text, width, height, screen_width, theme):
        self.text = text
        self.width = width
        self.height = height
        self.is_visible = False
        self.font = font_text
        self.rect = pygame.Rect(
            (screen_width - self.width) - 20,
            80,
            self.width,
            self.height
        )
        self.ignore_next_click = False
        self.update_theme(theme)

    def update_theme(self, theme):
        self.bg_color = theme['info_window_bg']
        self.border_color = theme['info_window_border']
        self.text_color = theme['info_window_text']

    def show(self):
        self.is_visible = True
        self.ignore_next_click = True

    def hide(self):
        self.is_visible = False

    def toggle_visibility(self):
        if self.is_visible:
            self.hide()
        else:
            self.show()

    def update(self, events):
        if not self.is_visible:
            return
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ignore_next_click:
                    self.ignore_next_click = False
                    continue
                mouse_pos = pygame.mouse.get_pos()
                if not self.rect.collidepoint(mouse_pos):
                    self.hide()

    def draw(self, surface):
        if self.is_visible:
            pygame.draw.rect(surface, self.bg_color, self.rect)
            pygame.draw.rect(surface, self.border_color, self.rect, 2)
            text_lines = self.text.split("\\n")
            for i, line in enumerate(text_lines):
                text_surf = self.font.render(line, True, self.text_color)
                text_rect = text_surf.get_rect(
                    center=(self.rect.centerx, self.rect.y + 30 + i * 40)
                )
                surface.blit(text_surf, text_rect)

    def update_coordinates(self, x, y):
        self.rect.x = (x - self.width) - 20
        self.rect.y = y

    def set_text(self, text):
        self.text = text
