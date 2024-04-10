import pygame
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

    def play_hit_sound(self):
        self.hit_sound.play()
        
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