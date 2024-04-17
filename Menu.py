import pygame
import sys

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.BG = pygame.transform.scale2x(pygame.image.load(r'assets/background-night.png').convert())
        self.WHITE = (255, 255, 255)
        self.FONT = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()
        self.options = [
            {"text": "Start Game", "action": "start"},
            {"text": "Bird Skins", "action": "skins"},
            {"text": "Exit", "action": "exit"}
        ]
        option_height = (screen.get_height() - len(self.options) * 50) / 2
        self.option_rects = [pygame.Rect(91, option_height + i * 50, 250, 40) for i in range(len(self.options))]

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        while running:
            self.screen.blit(self.BG, (0, 0))  # Draw the background
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for option_rect, option in zip(self.option_rects, self.options):
                        if option_rect.collidepoint(x, y):
                            if option["action"] == "start":
                                return "start"
                            elif option["action"] == "skins":
                                selected_skin_index = self.choose_bird_skin(self.WHITE)  # Pass WHITE as argument
                                if selected_skin_index is not None:
                                    return "skins", selected_skin_index
                            elif option["action"] == "exit":
                                pygame.quit()
                                sys.exit()

            for option_rect, option in zip(self.option_rects, self.options):
                self.draw_text(option["text"], self.FONT, self.WHITE, option_rect.x, option_rect.y)

            pygame.display.flip()
            self.clock.tick(60)

    def choose_bird_skin(self, BLACK):
        selected_skin_index = 0  # Default selected skin index
        skins = [
            pygame.transform.scale2x(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("assets/purplebird_downflap.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("assets/redbird_downflap.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("assets/greenbird_downflap.png").convert_alpha())
        ]
        font = pygame.font.Font(None, 36)
        WHITE = (255, 255, 255)
        GRAY = (150, 150, 150)

        # Load background image
        BG = pygame.transform.scale2x(pygame.image.load(r'assets/background-night.png').convert())

        # Set positions for each bird image
        bird_positions = [
            (70, 200),
            (280, 200),
            (70, 300 + 50),
            (280, 350)
        ]

        # Set rectangle sizes
        rect_width = 34 * 2  # Width of yellow bird image
        rect_heights = [24*2, 23 * 2, 24 * 2, 21 * 2]  # Heights of each bird image

        running = True
        while running:
            self.screen.blit(BG, (0, 0))  # Draw the background

            # Display title
            title_text = font.render("Choose Bird Skin", True, BLACK)
            self.screen.blit(title_text, (150, 50))

            # Display skins
            for i, skin in enumerate(skins):
                self.screen.blit(skin, bird_positions[i])

            # Highlight selected skin
            pygame.draw.rect(self.screen, WHITE, (bird_positions[selected_skin_index][0], bird_positions[selected_skin_index][1], rect_width, rect_heights[selected_skin_index]), 2)

            # Display OK button
            ok_button_rect = pygame.Rect(165, 480, 100, 40)
            pygame.draw.rect(self.screen, GRAY, ok_button_rect)
            ok_text = font.render("OK", True, BLACK)
            self.screen.blit(ok_text, (195, 490))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if a skin is selected
                    for i, _ in enumerate(skins):
                        if pygame.Rect(bird_positions[i][0], bird_positions[i][1], rect_width, rect_heights[i]).collidepoint(mouse_pos):
                            selected_skin_index = i
                            print("Selected skin:", i + 1)  # Print the index of the selected skin
                            # Perform action based on selected skin (e.g., change character appearance)
                    # Check if OK button is clicked
                    if ok_button_rect.collidepoint(mouse_pos):
                        return selected_skin_index  # Return the selected skin index when OK is clicked