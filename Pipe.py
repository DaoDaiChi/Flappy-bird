import pygame
import random as rd
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
        random_pipe_pos = rd.choice(self.pipe_height)
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