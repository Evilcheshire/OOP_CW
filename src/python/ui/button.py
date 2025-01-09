import pygame

from src.python.ui.base_button import BaseButton

class Button(BaseButton):
    def __init__(self, x, y, width, height, identifier, text, font_buttons, callback, theme):
        super().__init__(identifier, text, callback, font_buttons, theme["text"], theme["button"])
        self.original_rect = pygame.Rect(x, y, width, height)
        self.rect = self.original_rect.copy()

        self.color = theme["button"]
        self.hover_color = theme["button_hover"]
        self.outline_color = theme["button_outline"]
        self.hover_text_color = theme["button_hover_text"]
        self.polygon_color = theme["polygon"]
        self.animation_progress = 0
        self.grow_pixels = 3

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.original_rect.collidepoint(mouse_pos)
        if self.is_hovered:
            self.animation_progress = min(self.animation_progress + 10, self.original_rect.width // 2)
            self.rect = pygame.Rect(
                self.original_rect.x - self.grow_pixels,
                self.original_rect.y - self.grow_pixels,
                self.original_rect.width + self.grow_pixels * 2,
                self.original_rect.height + self.grow_pixels * 2
            )
        else:
            self.animation_progress = max(self.animation_progress - 10, 0)
            self.rect = self.original_rect.copy()

    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.color
        current_text_color = self.hover_text_color if self.is_hovered else self.text_color

        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, self.outline_color, self.rect, 2)

        if self.is_hovered and self.animation_progress > 0:
            points = [
                (self.rect.x, self.rect.y),
                (self.rect.x + self.animation_progress - 30, self.rect.y),
                (self.rect.x + self.animation_progress, self.rect.bottom),
                (self.rect.x, self.rect.bottom)
            ]
            pygame.draw.polygon(surface, self.polygon_color, points)

        text_surf = self.font.render(self.text, True, current_text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)



