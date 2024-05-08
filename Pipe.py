import pygame
import random as rd
class Pipe:
    def __init__(self, screen):
        """
        Khởi tạo Pipe với màn hình Pygame và tốc độ di chuyển của đường ống.

        :param screen: Màn hình Pygame nơi các đường ống được vẽ.
        :param pipe_speed: Tốc độ di chuyển của đường ống. Mặc định là 5.
        """
        self.screen = screen
        self.pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())
        self.pipe_list = []
        self.pipe_height = [300, 400, 350]
        self.spawnpipe_event = pygame.USEREVENT
        pygame.time.set_timer(self.spawnpipe_event, 1200)
        self.hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')

    def play_hit_sound(self):
        """
        Phát âm thanh va chạm khi chim chạm vào đường ống.
        """
        self.hit_sound.play()
        
    def create_pipe(self):
        """
        Tạo một cặp đường ống với vị trí ngẫu nhiên.

        :return: Một cặp đường ống (top pipe và bottom pipe).
        """
        random_pipe_pos = rd.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(455, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midtop=(455, random_pipe_pos - 750))# Khoảng cách giữa ống trên và ống dưới sẽ là random_pipe_pos - 750
        return bottom_pipe, top_pipe

    def move_pipe(self):
        """
        Di chuyển các đường ống sang trái dựa trên tốc độ di chuyển.
        """
        for pipe in self.pipe_list:
            pipe.centerx -= 5
        self.pipe_list = [pipe for pipe in self.pipe_list if pipe.right > 0] # Loại bỏ các đường ống đã đi ra ngoài màn hình

    def draw(self):
        """
        Vẽ các đường ống lên màn hình.
        """
        for pipe in self.pipe_list:
            if pipe.bottom >= 600:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)
