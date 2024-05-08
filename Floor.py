import pygame
class Floor:
    def __init__(self, screen):
        """
        Khởi tạo sàn với màn hình và tốc độ di chuyển.

        :param screen: Màn hình Pygame nơi sàn được vẽ.
        :param speed: Tốc độ di chuyển của sàn. Mặc định là 1.
        """
        self.screen = screen
        self.floor_surface = pygame.transform.scale2x(pygame.image.load('assets/floor.png').convert())
        self.floor_x_pos = 0

    def draw(self):
        self.screen.blit(self.floor_surface, (self.floor_x_pos, 650))
        self.screen.blit(self.floor_surface, (self.floor_x_pos + 432, 650))

    def update_position(self):
        """
        Cập nhật vị trí của sàn để tạo hiệu ứng chuyển động.
        """
        self.floor_x_pos -= 1
        if self.floor_x_pos <= -432:
            self.floor_x_pos = 0
