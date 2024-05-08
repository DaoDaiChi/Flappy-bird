import pygame , sys
class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.bg = pygame.transform.scale2x(pygame.image.load("assets/background-night.png").convert())
        # Nút "Start Game"
        self.start_button_image = pygame.transform.scale2x(pygame.image.load("assets/start_game_button.png").convert_alpha())
        self.start_button_rect = self.start_button_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        self.clock = pygame.time.Clock()  # Dùng để kiểm soát tốc độ khung hình
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button_rect.collidepoint(event.pos):
                        return  # Thoát khỏi vòng lặp để chuyển đến menu
            
            # Hiển thị giao diện khởi động và nút "Start Game"
            self.screen.blit(self.bg, (0, 0))  # Vẽ nền
            self.screen.blit(self.start_button_image, self.start_button_rect)  # Vẽ nút "Start Game"
            
            pygame.display.flip()  # Cập nhật màn hình
            self.clock.tick(60)  # Điều chỉnh tốc độ khung hình