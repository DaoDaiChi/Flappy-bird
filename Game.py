import pygame
import sys
from Bird import Bird
from Pipe import Pipe
from Floor import Floor

class Game:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()
        self.screen = pygame.display.set_mode((432, 768))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('04B_19.ttf', 35)
        self.bg = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())
        self.bird = Bird(self.screen)
        self.pipe = Pipe(self.screen)
        self.floor = Floor(self.screen)
        self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
        self.game_over_rect = self.game_over_surface.get_rect(center=(216, 384))
        self.flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
        self.hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
        self.score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
        self.score_sound_countdown = 100
        self.game_active = True
        self.score = 0
        self.high_score = 0
        self.back_button_image = pygame.transform.scale2x(pygame.image.load('assets/backbutton.png').convert_alpha())
        self.back_button_rect = self.back_button_image.get_rect(topleft=(10, 40))

    def play_collision_sound(self):
        self.hit_sound.play()

    def score_display(self):
        score_surface = self.game_font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        self.screen.blit(score_surface, score_rect)

        high_score_surface = self.game_font.render(f'High Score: {int(self.high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        self.screen.blit(high_score_surface, high_score_rect)

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button_rect.collidepoint(event.pos):
                        self.game_active = True
                        self.pipe.pipe_list.clear()
                        self.bird.bird_rect.center = (100, 384)
                        self.bird.bird_movement = 0
                        self.score = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active:
                        self.bird.bird_movement = 0
                        self.bird.bird_movement = -11
                        self.flap_sound.play()
                    if event.key == pygame.K_SPACE and not self.game_active:
                        self.game_active = True
                        self.pipe.pipe_list.clear()
                        self.bird.bird_rect.center = (100, 384)
                        self.bird.bird_movement = 0
                        self.score = 0
                if event.type == self.pipe.spawnpipe_event:
                    self.pipe.pipe_list.extend(self.pipe.create_pipe())

            self.screen.blit(self.bg, (0, 0))

            if self.game_active:
                self.bird.update_movement()
                self.bird.bird_animation()
                self.bird.draw()
                self.game_active = not self.check_collision()
                self.pipe.move_pipe()
                self.pipe.draw()
                self.score += 0.01
                self.score_display()
                self.score_sound_countdown -= 1
                if self.score_sound_countdown <= 0:
                    self.score_sound.play()
                    self.score_sound_countdown = 100
                if not self.game_active:
                    self.play_collision_sound()
                    pygame.time.delay(1000)

            else:
                self.screen.blit(self.game_over_surface, self.game_over_rect)
                self.update_high_score()
                self.score_display()

            self.floor.draw()
            self.floor.update_position()

            self.screen.blit(self.back_button_image, self.back_button_rect)

            pygame.display.update()
            self.clock.tick(75)