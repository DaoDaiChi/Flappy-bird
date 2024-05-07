import pygame
import sys
from Bird import Bird
from Pipe import Pipe
from Floor import Floor
import time

class Game:
    def __init__(self, screen,level_number):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.game_active = True
        self.current_level = level_number
        self.score = 0
        self.high_score = 0
        self.prev_score = 0  # Khởi tạo điểm số trước đó
        self.floor = Floor(screen)
        self.bg = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())
        self.game_font = pygame.font.Font('04B_19.ttf', 35)
        self.auto_play_mode = False

        self.bird = Bird(screen)
        self.pipe = Pipe(screen)
        
        # Nút "Start Game"
        self.start_button_image = pygame.transform.scale2x(
            pygame.image.load("assets/start_game_button.png").convert_alpha()
        )
        self.start_button_rect = self.start_button_image.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2)
        )
        
        # Trạng thái giao diện khởi động
        self.show_start_screen = True  # Ban đầu, hiển thị giao diện khởi động
        
        # Các giá trị trọng lực cho mỗi cấp độ từ 1 đến 5
        gravity_levels = [0.7, 0.9, 1.1, 1.3, 1.5]
        
        # Sử dụng giá trị trọng lực cho cấp độ hiện tại
        self.gravity = gravity_levels[self.current_level - 1]

        self.bird = Bird(screen, gravity=self.gravity)  # Khởi tạo chim với trọng lực thích hợp
        self.game_active = True
        self.clock = pygame.time.Clock()
        
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

    def set_auto_play(self, enable):
        """Enable or disable auto-play mode."""
        self.auto_play_mode = enable
    
    def auto_play(self):
        """Logic tự động chơi game."""
        if self.pipe.pipe_list:
            # Tìm cột gần nhất
            closest_pipe = min(
                (pipe for pipe in self.pipe.pipe_list if pipe.centerx > self.bird.bird_rect.centerx),
                key=lambda p: p.centerx - self.bird.bird_rect.centerx,
                default=None,
            )

            if closest_pipe:
                # Xác định vị trí cột dưới và cột trên
                if closest_pipe.bottom >= 600:  # Nếu là cột dưới
                    bottom_pipe_center = closest_pipe.centery
                    top_pipe_center = bottom_pipe_center - 650  # Vị trí của cột trên
                else:  # Nếu là cột trên
                    top_pipe_center = closest_pipe.centery
                    bottom_pipe_center = top_pipe_center + 650  # Vị trí của cột dưới

                # Tính vị trí trung tâm giữa cột trên và cột dưới
                pipe_gap_center = (bottom_pipe_center + top_pipe_center - 200) / 2

                # Khoảng cách an toàn
                gap_margin = 80  # Tăng khoảng cách an toàn để tránh va chạm

                # Giới hạn dưới và trên để chim bay
                min_y = pipe_gap_center - gap_margin
                max_y = pipe_gap_center + gap_margin

                # Vị trí của chim
                bird_center_y = self.bird.bird_rect.centery

                # Kiểm tra vị trí của chim và điều chỉnh nếu cần
                if bird_center_y > max_y:  # Nếu chim quá thấp, cần vỗ cánh
                    self.bird.bird_movement = -7  # Tăng sức vỗ cánh
                elif bird_center_y < min_y:  # Nếu quá cao, điều chỉnh trọng lực
                    self.bird.gravity = 1  # Giảm trọng lực
                else:  # Nếu trong khoảng cách an toàn, trọng lực bình thường
                    self.bird.gravity = 0.7

        else:
            # Nếu không có cột, vỗ cánh định kỳ
            if self.bird.bird_rect.centery > 384:
                self.bird.bird_movement = -15  # Tăng sức vỗ cánh để giữ chim không rơi quá thấp

    
    def update_movement(self):
        """Cập nhật chuyển động của chim."""
        self.bird.bird_movement += self.gravity  # Trọng lực kéo chim xuống
        self.bird.bird_rect.centery += self.bird.bird_movement  # Cập nhật vị trí của chim
    
    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.back_button_rect.collidepoint(event.pos):
                        return  # Exit the game loop
                    
                    if self.game_active and not self.auto_play_mode:
                        self.bird.bird_movement = -11
                        self.flap_sound.play()
                        
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_active and not self.auto_play_mode:
                            self.bird.bird_movement = -11
                            self.flap_sound.play()
                        else:
                            self.reset_game()

                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == self.pipe.spawnpipe_event:
                    self.pipe.pipe_list.extend(self.pipe.create_pipe())

            self.screen.blit(self.bg, (0, 0))  # Background rendering

            if self.game_active:
                if self.auto_play_mode:
                    self.auto_play()  # Auto-play logic

                self.bird.update_movement()
                self.bird.bird_animation()
                self.bird.draw()

                if self.check_collision():
                    self.play_collision_sound()
                    self.game_active = False

                self.pipe.move_pipe()
                self.pipe.draw()

                self.score += 0.01

                if int(self.score) > self.prev_score:
                    self.play_score_sound()
                    self.prev_score = int(self.score)

                self.score_display(True)

                elapsed_time = time.time() - self.start_time
                progress_length = int(self.PROGRESS_BAR_WIDTH * (elapsed_time / self.TOTAL_TIME))
                pygame.draw.rect(
                    self.screen,
                    (200, 200, 200),
                    (self.PROGRESS_BAR_X, self.PROGRESS_BAR_Y, self.PROGRESS_BAR_WIDTH, self.PROGRESS_BAR_HEIGHT),
                )
                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),
                    (self.PROGRESS_BAR_X, self.PROGRESS_BAR_Y, progress_length, self.PROGRESS_BAR_HEIGHT),
                )

                if elapsed_time >= self.TOTAL_TIME:
                    self.game_active = False
                    
            else:
                self.screen.blit(self.game_over_surface, self.game_over_rect)
                self.update_high_score()
                self.score_display(False)
                self.screen.blit(self.back_button_image, self.back_button_rect)
            
            self.floor.draw()
            self.floor.update_position()

            pygame.display.update()
            self.clock.tick(60)
            
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