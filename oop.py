import pygame
import sys
import random

class Bird:
    def __init__(self, screen):
        self.screen = screen
        self.gravity = 0.5
        self.bird_movement = 0
        self.bird_list = [pygame.transform.scale2x(pygame.image.load(f'assets/yellowbird-{i}flap.png').convert_alpha()) for i in ['down', 'mid', 'up']]
        self.bird_index = 0
        self.bird = self.bird_list[self.bird_index]
        self.bird_rect = self.bird.get_rect(center=(100, 384))
        self.birdflap_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.birdflap_event, 200)
        self.hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')

    def rotate_bird(self):
        new_bird = pygame.transform.rotozoom(self.bird, -self.bird_movement * 3, 1)
        return new_bird

    def bird_animation(self):
        self.bird = self.bird_list[self.bird_index]
        self.bird_rect = self.bird.get_rect(center=self.bird_rect.center)

    def update_movement(self):
        self.bird_movement += self.gravity
        self.bird_rect.centery += self.bird_movement

    def draw(self):
        rotated_bird = self.rotate_bird()
        self.screen.blit(rotated_bird, self.bird_rect)

    def play_hit_sound(self):
        self.hit_sound.play()

class Pipe:
    def __init__(self, screen):
        self.screen = screen
        self.pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())
        self.pipe_list = []
        self.pipe_height = [200, 300, 400]
        self.spawnpipe_event = pygame.USEREVENT
        pygame.time.set_timer(self.spawnpipe_event, 1200)
        self.hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')

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

    def play_hit_sound(self):
        self.hit_sound.play()

class Game:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()
        self.screen = pygame.display.set_mode((432, 768))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.bg = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())
        self.bird = Bird(self.screen)
        self.pipe = Pipe(self.screen)
        self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
        self.game_over_rect = self.game_over_surface.get_rect(center=(216, 384))
        self.game_active = True

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active:
                        self.bird.bird_movement = 0
                        self.bird.bird_movement = -11
                    if event.key == pygame.K_SPACE and not self.game_active:
                        self.game_active = True
                        self.pipe.pipe_list.clear()
                        self.bird.bird_rect.center = (100, 384)
                        self.bird.bird_movement = 0
                if event.type == self.pipe.spawnpipe_event:
                    self.pipe.pipe_list.extend(self.pipe.create_pipe())

            self.screen.blit(self.bg, (0, 0))

            if self.game_active:
                self.bird.update_movement()
                self.bird.bird_animation()
                self.bird.draw()
                self.game_active = not self.check_collision(self.bird.bird_rect, self.pipe.pipe_list)
                self.pipe.move_pipe()
                self.pipe.draw()
            else:
                self.screen.blit(self.game_over_surface, self.game_over_rect)

            pygame.display.update()
            self.clock.tick(75)

    def check_collision(self, bird_rect, pipe_list):
        for pipe in pipe_list:
            if bird_rect.colliderect(pipe):
                self.bird.play_hit_sound()
                self.pipe.play_hit_sound()
                return True
        if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            return True
        return False

if __name__ == "__main__":
    game = Game()
    game.run_game()
