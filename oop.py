import pygame
import sys
import random

class FlappyBird:
    def __init__(self):
        pygame.init()

        # Screen setup
        self.screen_width = 432
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Flappy Bird")

        # Clock setup
        self.clock = pygame.time.Clock()

        # Game font
        self.game_font = pygame.font.Font('04B_19.ttf', 35)

        # Game variables
        self.gravity = 0.25
        self.bird_movement = 0
        self.game_active = True
        self.score = 0
        self.high_score = 0

        # Background
        self.bg = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())

        # Floor
        self.floor = pygame.transform.scale2x(pygame.image.load('assets/floor.png').convert())
        self.floor_x_pos = 0

        # Bird setup
        self.bird_images = [pygame.transform.scale2x(pygame.image.load(f'assets/yellowbird-{i}flap.png').convert_alpha()) for i in ['down', 'mid', 'up']]
        self.bird_index = 0
        self.bird = self.bird_images[self.bird_index]
        self.bird_rect = self.bird.get_rect(center=(100, 384))

        # Event setup
        self.birdflap_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.birdflap_event, 200)

        self.spawnpipe_event = pygame.USEREVENT
        pygame.time.set_timer(self.spawnpipe_event, 1200)

        # Pipes setup
        self.pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())
        self.pipe_list = []

        # Game over setup
        self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
        self.game_over_rect = self.game_over_surface.get_rect(center=(216, 384))

        # Sounds
        self.flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
        self.hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
        self.score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
        self.score_sound_countdown = 100

    def draw_floor(self):
        self.screen.blit(self.floor, (self.floor_x_pos, 650))
        self.screen.blit(self.floor, (self.floor_x_pos + 432, 650))

    def create_pipe(self):
        random_pipe_pos = random.choice([200, 300, 400])
        bottom_pipe = self.pipe_surface.get_rect(midtop=(500, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midtop=(500, random_pipe_pos - 650))
        return bottom_pipe, top_pipe

    def move_pipe(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 5

    def draw_pipe(self):
        for pipe in self.pipe_list:
            if pipe.bottom >= 600:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)

    def check_collision(self):
        for pipe in self.pipe_list:
            if self.bird_rect.colliderect(pipe):
                self.hit_sound.play()
                return False
        if self.bird_rect.top <= -75 or self.bird_rect.bottom >= 650:
            return False
        return True

    def rotate_bird(self):
        new_bird = pygame.transform.rotozoom(self.bird, -self.bird_movement * 3, 1)
        return new_bird

    def bird_animation(self):
        new_bird = self.bird_images[self.bird_index]
        new_bird_rect = new_bird.get_rect(center=self.bird_rect.center)
        return new_bird, new_bird_rect

    def score_display(self, game_state):
        if game_state == 'main game':
            score_surface = self.game_font.render(str(int(self.score)), True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(216, 100))
            self.screen.blit(score_surface, score_rect)
        if game_state == 'game_over':
            score_surface = self.game_font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(216, 100))
            self.screen.blit(score_surface, score_rect)

            high_score_surface = self.game_font.render(f'High Score: {int(self.high_score)}', True, (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(216, 630))
            self.screen.blit(high_score_surface, high_score_rect)

    def update_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active:
                        self.bird_movement = 0
                        self.bird_movement = -11
                        self.flap_sound.play()
                    if event.key == pygame.K_SPACE and not self.game_active:
                        self.game_active = True
                        self.pipe_list.clear()
                        self.bird_rect.center = (100, 384)
                        self.bird_movement = 0
                        self.score = 0
                if event.type == self.spawnpipe_event:
                    self.pipe_list.extend(self.create_pipe())
                if event.type == self.birdflap_event:
                    if self.bird_index < 2:
                        self.bird_index += 1
                    else:
                        self.bird_index = 0

            self.screen.blit(self.bg, (0, 0))
            if self.game_active:
                self.bird_movement += self.gravity
                rotated_bird = self.rotate_bird()
                self.bird_rect.centery += self.bird_movement
                self.screen.blit(rotated_bird, self.bird_rect)
                self.game_active = self.check_collision()
                self.move_pipe()
                self.draw_pipe()
                self.score += 0.01
                self.score_display('main game')
                self.score_sound_countdown -= 1
                if self.score_sound_countdown <= 0:
                    self.score_sound.play()
                    self.score_sound_countdown = 100
            else:
                self.screen.blit(self.game_over_surface, self.game_over_rect)
                self.update_score()
                self.score_display('game_over')

            self.floor_x_pos -= 1
            self.draw_floor()
            if self.floor_x_pos <= -432:
                self.floor_x_pos = 0

            pygame.display.update()
            self.clock.tick(120)

if __name__ == "__main__":
    game = FlappyBird()
    game.run_game
