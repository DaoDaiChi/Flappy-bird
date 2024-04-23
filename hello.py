import pygame
import sys
import random
from Bird import *
from Pipe import *
from Floor import *
from Game import *
import time
class Bird:
    def __init__(self, screen):
        self.screen = screen
        self.gravity = 0.7
        self.bird_movement = 0
        self.bird_skins = [
            pygame.transform.scale2x(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("assets/purplebird_downflap.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("assets/redbird_downflap.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("assets/greenbird_downflap.png").convert_alpha())
        ]
        self.current_skin_index = 0
        self.bird = self.bird_skins[self.current_skin_index]
        self.bird_rect = self.bird.get_rect(center=(100, 384))
        self.birdflap_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.birdflap_event, 200)
        self.hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')

    def play_hit_sound(self):
        self.hit_sound.play()
        
    def rotate_bird(self):
        new_bird = pygame.transform.rotozoom(self.bird, -self.bird_movement * 3, 1)
        return new_bird

    def bird_animation(self):
        self.bird = self.bird_skins[self.current_skin_index]
        self.bird_rect = self.bird.get_rect(center=self.bird_rect.center)

    def update_movement(self):
        self.bird_movement += self.gravity
        self.bird_rect.centery += self.bird_movement

    def draw(self):
        rotated_bird = self.rotate_bird()
        self.screen.blit(rotated_bird, self.bird_rect)

    def change_skin(self, new_skin_index):
        if 0 <= new_skin_index < len(self.bird_skins):
            self.current_skin_index = new_skin_index
            self.bird = self.bird_skins[self.current_skin_index]

class Pipe:
    def __init__(self, screen):
        self.screen = screen
        self.pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())
        self.pipe_list = []
        self.pipe_height = [200, 300, 400]
        self.spawnpipe_event = pygame.USEREVENT
        pygame.time.set_timer(self.spawnpipe_event, 1200)
        self.hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')

    def play_hit_sound(self):
        self.hit_sound.play()
        
    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(500, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midtop=(500, random_pipe_pos - 650))
        return bottom_pipe, top_pipe

    def move_pipe(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 5
        self.pipe_list = [pipe for pipe in self.pipe_list if pipe.right > 0]

    def draw(self):
        for pipe in self.pipe_list:
            if pipe.bottom >= 600:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)

class Floor:
    def __init__(self, screen):
        self.screen = screen
        self.floor_surface = pygame.transform.scale2x(pygame.image.load('assets/floor.png').convert())
        self.floor_x_pos = 0

    def draw(self):
        self.screen.blit(self.floor_surface, (self.floor_x_pos, 650))
        self.screen.blit(self.floor_surface, (self.floor_x_pos + 432, 650))

    def update_position(self):
        self.floor_x_pos -= 1
        if self.floor_x_pos <= -432:
            self.floor_x_pos = 0

class Collision:
    @staticmethod
    def check_collision(bird_rect, pipe_list):
        for pipe in pipe_list:
            if bird_rect.colliderect(pipe):
                return True
        if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            return True
        return False

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

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.floor = Floor(self.screen)
        # Game state
        self.game_active = True
        self.score = 0
        self.high_score = 0
        
        # Load assets
        self.bg = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())
        self.game_font = pygame.font.Font('04B_19.ttf', 35)
        
        self.bird = Bird(screen)
        self.pipe = Pipe(screen)
        self.floor = Floor(screen)

        self.flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
        self.hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
        self.score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
        
        self.game_over_surface = pygame.transform.scale2x(
            pygame.image.load('assets/message.png').convert_alpha()
        )
        self.game_over_rect = self.game_over_surface.get_rect(center=(216, 384))
        
        self.back_button_image = pygame.transform.scale2x(
            pygame.image.load('assets/backbutton.png').convert_alpha()
        )
        self.back_button_rect = self.back_button_image.get_rect(topleft=(10, 40))

        # Progress bar settings
        self.PROGRESS_BAR_WIDTH = 300
        self.PROGRESS_BAR_HEIGHT = 20
        self.PROGRESS_BAR_X = (self.screen.get_width() - self.PROGRESS_BAR_WIDTH) // 2
        self.PROGRESS_BAR_Y = 50
        self.TOTAL_TIME = 30  # 30-second countdown
        self.start_time = time.time()  # Start time for progress bar

    def reset_game(self):
        self.game_active = True
        self.pipe.pipe_list.clear()
        self.bird.bird_rect.center = (100, 384)
        self.bird.bird_movement = 0
        self.score = 0
        self.score_sound_countdown = 100
        self.start_time = time.time()  # Reset progress bar
    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score  # Update high score

    def play_collision_sound(self):
        self.hit_sound.play()

    def score_display(self):
        score_surface = self.game_font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        self.screen.blit(score_surface, score_rect)

        high_score_surface = self.game_font.render(f'High Score: {int(self.high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        self.screen.blit(high_score_surface, high_score_rect)

    def check_collision(self):
        for pipe in self.pipe.pipe_list:
            if self.bird.bird_rect.colliderect(pipe):
                return True
        if self.bird.bird_rect.top <= -75 or self.bird.bird_rect.bottom >= 650:
            return True
        return False

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_button_rect.collidepoint(event.pos):
                        return  # Exit the game loop, returning to main()
                    
                    if self.game_active:
                        self.bird.bird_movement = -11
                        self.flap_sound.play()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_active:
                            self.bird.bird_movement = -11
                            self.flap_sound.play()
                        else:
                            self.reset_game()  # Reset game on spacebar when inactive
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == self.pipe.spawnpipe_event:
                    self.pipe.pipe_list.extend(self.pipe.create_pipe())

            # Background and game logic
            self.screen.blit(self.bg, (0, 0))

            if self.game_active:
                self.bird.update_movement()
                self.bird.bird_animation()
                self.bird.draw()

                if self.check_collision():
                    self.play_collision_sound()
                    self.game_active = False  # Game over

                self.pipe.move_pipe()
                self.pipe.draw()

                self.score += 0.01  # Increment score gradually
                self.score_sound_countdown -= 1
                if self.score_sound_countdown <= 0:
                    self.score_sound.play()
                    self.score_sound_countdown = 100
                
                self.score_display()  # Display the current and high score
                
                # Progress bar update
                elapsed_time = time.time() - self.start_time
                progress_length = int(self.PROGRESS_BAR_WIDTH * (elapsed_time / self.TOTAL_TIME))
                pygame.draw.rect(
                    self.screen,
                    (200, 200, 200),  # Progress bar background
                    (self.PROGRESS_BAR_X, self.PROGRESS_BAR_Y, self.PROGRESS_BAR_WIDTH, self.PROGRESS_BAR_HEIGHT),
                )
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),  # Filled portion of progress bar
                    (self.PROGRESS_BAR_X, self.PROGRESS_BAR_Y, progress_length, self.PROGRESS_BAR_HEIGHT),
                )

            else:  # Game-over screen
                self.screen.blit(self.game_over_surface, self.game_over_rect)
                self.update_high_score()  # Update high score if needed
                self.score_display()  # Display current and high scores
                self.screen.blit(self.back_button_image, self.back_button_rect)
            self.floor.draw()
            self.floor.update_position()
            pygame.display.update()
            self.clock.tick(60)


def main():
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()
    screen = pygame.display.set_mode((432, 768))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    menu = Menu(screen)
    selected_skin_index = 0  # Default selected skin index
    game = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Run the menu and get a choice
        choice = menu.run()

        if choice == "start":
            if game is None:
                game = Game(screen)  # Create a new Game instance
            game.reset_game()  # Reset game attributes
            game.run_game()  # Run the game

        elif isinstance(choice, tuple) and choice[0] == "skins":  # Handle skin selection
            selected_skin_index = choice[1]
            if game:
                game.bird.change_skin(selected_skin_index)  # Apply selected skin

if __name__ == "__main__":
    main()