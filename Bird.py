import pygame

class Bird:
    def __init__(self, screen):
        self.screen = screen
        self.gravity = 0.5
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
