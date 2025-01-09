import pygame
from src.python.ui.base_button import BaseButton

class CircleButton(BaseButton):
    def __init__(self, x, y, radius, identifier, text, font_buttons, callback, theme):
        super().__init__(identifier, text, callback, font_buttons, theme['button_text'], theme['button_text'])
        self.x = x
        self.y = y
        self.radius = radius
        self.outline_width = 2
        self.update_theme(theme)

    def update_theme(self, theme):
        self.color = theme['button']
        self.text_color = theme['button_text']
        self.hover_text_color = theme['button_hover_text']
        self.hover_color = theme['button_hover']
        self.outline_color = theme['button_outline']

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            distance = ((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2) ** 0.5
            if distance <= self.radius:
                self.callback()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        distance = ((self.x - mouse_pos[0]) ** 2 + (self.y - mouse_pos[1]) ** 2) ** 0.5
        self.is_hovered = distance <= self.radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.outline_color, (self.x, self.y), self.radius + self.outline_width)
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.circle(surface, current_color, (self.x, self.y), self.radius)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.x, self.y))
        surface.blit(text_surf, text_rect)
