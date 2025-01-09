class BaseButton:
    def __init__(self, identifier, text, callback, font, text_color, hover_text_color):
        self.identifier = identifier
        self.text = text
        self.callback = callback
        self.font = font
        self.text_color = text_color
        self.hover_text_color = hover_text_color
        self.is_hovered = False

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

    def set_text(self, text):
        self.text = text