import pygame
import json
from hackenbush import Game
from src.python.settings.config import RED, BLUE, CREAM, EDGE_WIDTH, GRAPHS_PATH, LIGHT_THEME, DARK_THEME, DARK_CREAM, \
    BUTTON_LONG_WIDTH
from src.python.ui.button import Button

class HackenbushGame:
    def __init__(self, surface, config, font, mode, index, graph_file=GRAPHS_PATH):
        self.surface = surface
        self.config = config
        self.font = font
        self.mode = mode
        self.index = index
        self.running = True
        self.total_turns = 0

        self.positions = {}
        graph_data = self.load_graph_from_json(graph_file, index)
        self.game = Game(len(self.positions))

        for edge in graph_data["edges"]:
            self.game.add_edge(edge["u"], edge["v"], edge["color"], is_root=edge["is_root"])

        self.turn = 0  # 0 - червоний, 1 - синій

        self.menu_button = Button(
            x=self.surface.get_width() - BUTTON_LONG_WIDTH - 20,
            y=self.surface.get_height() - 70,
            width=BUTTON_LONG_WIDTH,
            height=50,
            identifier="back_to_menu_button",
            text=self.config.translations['back_to_menu_button'],
            font_buttons=self.font,
            callback=self.return_to_menu,
            theme=self.get_theme_colors()
        )

    def get_theme_colors(self):
        current_theme = self.config.get_theme()
        if current_theme == "dark":
            return DARK_THEME
        elif current_theme == "light":
            return LIGHT_THEME
        else:
            raise ValueError(f"Unknown theme: {current_theme}")

    def load_graph_from_json(self, file_path, index):
        """Завантажує граф і позиції вузлів із JSON."""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {file_path} не знайдено.")
        except json.JSONDecodeError:
            raise ValueError("Файл JSON має помилковий формат.")

        graph_data = data[index]

        self.positions = {int(k): v for k, v in graph_data["positions"].items()}

        offset_x = (self.surface.get_width() - max(pos[0] for pos in self.positions.values())) // 2
        offset_y = (self.surface.get_height() - max(pos[1] for pos in self.positions.values())) // 2

        self.positions = {
            node: (pos[0] + offset_x, pos[1] + offset_y)
            for node, pos in self.positions.items()
        }

        return graph_data

    def return_to_menu(self):
        self.running = False

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_graph(self.game.get_graph())
            self.display_turn_indicator()

            self.menu_button.update()
            self.menu_button.draw(self.surface)

            pygame.display.flip()

            if self.check_game_over():
                break

            if self.mode == "computer" and self.turn == 1:
                self.computer_move()
                self.draw_graph(self.game.get_graph())
                if self.check_game_over():
                    break

    def check_game_over(self):
        if self.game.is_game_over(self.turn):
            self.display_winner()
            self.running = False
            return True
        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.menu_button.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.handle_click(mouse_pos)

    def update_game(self, u, v, color):
        self.game.update_after_move(u, v, color)
        self.turn = 1 - self.turn
        self.total_turns += 1

    def handle_click(self, mouse_pos):
        clicked_edge = self.get_clicked_edge(mouse_pos, self.game.get_graph())
        if clicked_edge:
            u, v, color = clicked_edge
            if self.turn == color:
                self.update_game(u, v, color)

    def computer_move(self):
        optimal_move = self.game.get_optimal_move()
        if optimal_move != (-1, -1):
            u, v = optimal_move
            pygame.time.delay(1000)
            self.update_game(u, v, 1)

    def display_turn_indicator(self):
        turn_text = self.config.translations['red'] if self.turn == 0 else self.config.translations['blue']
        turn_text += " " + self.config.translations['turn']
        text_surface = self.font.render(turn_text, True, RED if self.turn == 0 else BLUE)
        self.surface.blit(text_surface, (10, 10))

    def display_winner(self):
        self.surface.fill(CREAM)
        winner_color = RED if self.turn == 1 else BLUE  # Переможець - той, хто щойно зробив хід
        winner_text = self.config.translations['red'] if winner_color == RED else self.config.translations['blue']
        winner_text += " " + self.config.translations['victory'] + "!"

        turns_text = f"{self.config.translations['on_turn']} {self.total_turns}."

        text_surface = self.font.render(winner_text, True, winner_color)

        turns_surface = self.font.render(turns_text, True, winner_color)

        self.blit_text(text_surface, turns_surface)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.menu_button.handle_event(event)

            self.surface.fill(CREAM)
            self.blit_text(text_surface, turns_surface)

            self.menu_button.update()
            self.menu_button.draw(self.surface)
            pygame.display.flip()

    def blit_text(self, text_surface, turns_surface):
        self.surface.blit(
            text_surface,
            (
                (self.surface.get_width() - text_surface.get_width()) // 2,
                (self.surface.get_height() // 2) - 50
            )
        )

        self.surface.blit(
            turns_surface,
            (
                (self.surface.get_width() - turns_surface.get_width()) // 2,
                (self.surface.get_height() // 2) + 20
            )
        )

    def draw_graph(self, graph):
        self.surface.fill(CREAM)

        max_y = max(pos[1] for pos in self.positions.values())
        pygame.draw.rect(
            self.surface,
            DARK_CREAM,
            pygame.Rect(0, max_y, self.surface.get_width(), self.surface.get_height() - max_y)
        )

        for u, v, color in graph:
            if u not in self.positions or v not in self.positions:
                continue

            edge_color = RED if color == 0 else BLUE
            pygame.draw.line(self.surface, edge_color, self.positions[u], self.positions[v], EDGE_WIDTH)

    def get_clicked_edge(self, mouse_pos, graph):
        for u, v, color in graph:
            if u in self.positions and v in self.positions:
                pos_u = self.positions[u]
                pos_v = self.positions[v]
                if self.is_click_on_edge(mouse_pos, pos_u, pos_v):
                    return (u, v, color)
        return None

    @staticmethod
    def is_click_on_edge(mouse_pos, pos_u, pos_v):
        mx, my = mouse_pos
        x1, y1 = pos_u
        x2, y2 = pos_v

        edge_length_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
        if edge_length_sq == 0:
            return False

        t = ((mx - x1) * (x2 - x1) + (my - y1) * (y2 - y1)) / edge_length_sq
        t = max(0, min(1, t))

        px = x1 + t * (x2 - x1)
        py = y1 + t * (y2 - y1)
        distance = ((mx - px) ** 2 + (my - py) ** 2) ** 0.5

        return distance <= EDGE_WIDTH