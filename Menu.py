import pygame
import sys

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.BG_COLOR = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.FONT = pygame.font.Font(None, 36)
        self.levels = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]  # Danh sách các cấp độ

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            self.screen.fill(self.BG_COLOR)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for i, level in enumerate(self.levels, start=1):
                        text_width, text_height = self.FONT.size(level)
                        level_rect = pygame.Rect(self.WIDTH // 2 - text_width // 2, 100 + 50 * i, text_width, text_height)
                        if level_rect.collidepoint(x, y):
                            print(f"Selected Level {i}")  # In ra cấp độ đã chọn
                            running = False
                            break
            
            for i, level in enumerate(self.levels, start=1):
                self.draw_text(level, self.FONT, self.WHITE, self.WIDTH // 2, 100 + 50 * i)

            pygame.display.flip()

