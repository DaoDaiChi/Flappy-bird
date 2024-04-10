import pygame
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