import pygame
import sys
from Bird import Bird
from Pipe import Pipe
from Floor import Floor
import time
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.game_active = True
        self.score = 0
        self.high_score = 0
        self.prev_score = 0  # Khởi tạo điểm số trước đó
        self.floor = Floor(screen)
        self.bg = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())
        self.game_font = pygame.font.Font('04B_19.ttf', 35)

        self.bird = Bird(screen)
        self.pipe = Pipe(screen)

        self.flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
        self.hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
        self.score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

        self.game_over_surface = pygame.transform.scale2x(
            pygame.image.load('assets/message.png').convert_alpha()
        )
        self.game_over_rect = self.game_over_surface.get_rect(center=(216, 384))

        self.back_button_image = pygame.transform.scale2x(
            pygame.image.load('assets/backbutton.png').convert_alpha()
        )
        self.back_button_rect = self.back_button_image.get_rect(topleft=(10, 40))

        # Cài đặt thanh tiến trình
        self.PROGRESS_BAR_WIDTH = 300
        self.PROGRESS_BAR_HEIGHT = 20
        self.PROGRESS_BAR_X = (self.screen.get_width() - self.PROGRESS_BAR_WIDTH) // 2
        self.PROGRESS_BAR_Y = 50
        self.TOTAL_TIME = 30  # 30 giây đếm ngược
        self.start_time = time.time()

    def reset_game(self):
        self.game_active = True
        self.pipe.pipe_list.clear()
        self.bird.bird_rect.center = (100, 384)
        self.bird.bird_movement = 0
        self.score = 0
        self.prev_score = 0  # Đặt lại điểm số trước đó
        self.start_time = time.time()

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def play_collision_sound(self):
        self.hit_sound.play()
    
    def play_score_sound(self):
        self.score_sound.play()

    def score_display(self, game_active):
        # Hiển thị điểm cao nhất chỉ khi trò chơi không hoạt động (game over)
        if not game_active:
            score_surface = self.game_font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(216, 100))
            self.screen.blit(score_surface, score_rect)

            high_score_surface = self.game_font.render(f'High Score: {int(self.high_score)}', True, (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(216, 630))
            self.screen.blit(high_score_surface, high_score_rect)

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

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_button_rect.collidepoint(event.pos):
                        return  # Thoát khỏi vòng lặp game

                    if self.game_active:
                        self.bird.bird_movement = -11
                        self.flap_sound.play()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_active:
                            self.bird.bird_movement = -11
                            self.flap_sound.play()
                        else:
                            self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == self.pipe.spawnpipe_event:
                    self.pipe.pipe_list.extend(self.pipe.create_pipe())

            self.screen.blit(self.bg, (0, 0))  # Vẽ nền

            if self.game_active:
                self.bird.update_movement()
                self.bird.bird_animation()
                self.bird.draw()

                if self.check_collision():
                    self.play_collision_sound()
                    self.game_active = False  # Kết thúc trò chơi do va chạm

                self.pipe.move_pipe()
                self.pipe.draw()

                self.score += 0.01  # Tăng điểm từ từ

                # Phát âm thanh khi điểm số tăng
                if int(self.score) > self.prev_score:
                    self.play_score_sound()  # Phát âm thanh khi điểm số tăng
                    self.prev_score = int(self.score)  # Cập nhật điểm số trước đó

                self.score_display(True)  # Chỉ hiển thị điểm hiện tại

                # Cập nhật thanh tiến trình
                elapsed_time = time.time() - self.start_time
                progress_length = int(self.PROGRESS_BAR_WIDTH * (elapsed_time / self.TOTAL_TIME))
                pygame.draw.rect(
                    self.screen,
                    (200, 200, 200),  # Màu nền cho thanh tiến trình
                    (self.PROGRESS_BAR_X, self.PROGRESS_BAR_Y, self.PROGRESS_BAR_WIDTH, self.PROGRESS_BAR_HEIGHT),
                )
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),  # Phần đầy của thanh tiến trình
                    (self.PROGRESS_BAR_X, self.PROGRESS_BAR_Y, progress_length, self.PROGRESS_BAR_HEIGHT),
                )

                if elapsed_time >= self.TOTAL_TIME:
                    self.game_active = False  # Kết thúc trò chơi khi hết thời gian
                    
            else:  # Khi trò chơi không hoạt động, hiển thị màn hình game over
                self.screen.blit(self.game_over_surface, self.game_over_rect)
                self.update_high_score()  # Cập nhật điểm cao nhất nếu cần
                self.score_display(False)  # Hiển thị điểm hiện tại và điểm cao nhất
                self.screen.blit(self.back_button_image, self.back_button_rect)  # Nút quay lại
            
            self.floor.draw()  # Vẽ sàn
            self.floor.update_position()  # Cập nhật vị trí của sàn

            pygame.display.update()  # Cập nhật màn hình
            self.clock.tick(60)  # Duy trì tốc độ 60 FPS