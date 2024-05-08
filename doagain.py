import pygame
import sys
import random
import time
class Bird:
    def __init__(self, screen, initial_skin_index=0,gravity=0.7):
        self.screen = screen
        self.gravity = gravity
        self.bird_movement = 0
        self.bird_skins = [
            pygame.transform.scale2x(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("assets/purplebird_downflap.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("assets/redbird_downflap.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("assets/greenbird_downflap.png").convert_alpha())
        ]
        self.current_skin_index = initial_skin_index  # Store the initial skin index
        self.bird = self.bird_skins[self.current_skin_index]
        self.bird_rect = self.bird.get_rect(center=(100, 384))
        self.birdflap_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.birdflap_event, 200)
        self.hit_sound = pygame.mixer.Sound("sound/sfx_hit.wav")

        # Debug output to confirm initialization
        print("Bird initialized with skin index:", self.current_skin_index)

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
        print("Changing skin to index:", new_skin_index)  # Debug output to check incoming index
        if 0 <= new_skin_index < len(self.bird_skins):
            self.current_skin_index = new_skin_index
            self.bird = self.bird_skins[self.current_skin_index]

            # Debug output to confirm change
            print("Skin changed to index:", self.current_skin_index)  
            
            # Keep the bird's position after changing the skin
            center = self.bird_rect.center
            self.bird_rect = self.bird.get_rect(center=center)
        else:
            raise ValueError("Invalid skin index")

class Pipe:
    def __init__(self, screen):
        self.screen = screen
        self.pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png').convert())
        self.pipe_list = []
        self.pipe_height = [300, 400, 350]
        self.spawnpipe_event = pygame.USEREVENT
        pygame.time.set_timer(self.spawnpipe_event, 1200)
        self.hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')

    def play_hit_sound(self):
        self.hit_sound.play()
        
    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(455, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midtop=(455, random_pipe_pos - 750))
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

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.BG = pygame.transform.scale2x(pygame.image.load(r'assets/background-night.png').convert())
        self.WHITE = (255, 255, 255)
        self.FONT = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()
        self.options = [
            {"text": "Level 1", "action": "level1"},
            {"text": "Level 2", "action": "level2"},
            {"text": "Level 3", "action": "level3"},
            {"text": "Level 4", "action": "level4"},
            {"text": "Level 5", "action": "level5"},
            {"text": "Bird Skins", "action": "skins"},
            {"text": "Auto-Play", "action": "autoplay"},
            {"text": "Exit", "action": "exit"}
        ]
        option_height = (screen.get_height() - len(self.options) * 50) / 2
        self.option_rects = [pygame.Rect(91, option_height + i * 50, 250, 40) for i in range(len(self.options))]

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)

    def choose_bird_skin(self, BLACK = (0,0,0)):
        selected_skin_index = 0  # Default selected skin index
        skins = [
            pygame.transform.scale2x(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("assets/purplebird_downflap.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("assets/redbird_downflap.png").convert_alpha()),
            pygame.transform.scale2x(pygame.image.load("assets/greenbird_downflap.png").convert_alpha())
        ]
        font = pygame.font.Font(None, 36)
        WHITE = (255, 255, 255)
        GRAY = (150, 150, 150)

        # Load background image
        BG = pygame.transform.scale2x(pygame.image.load(r'assets/background-night.png').convert())

        # Set positions for each bird image
        bird_positions = [
            (70, 200),
            (280, 200),
            (70, 300 + 50),
            (280, 350)
        ]

        # Set rectangle sizes
        rect_width = 34 * 2  # Width of yellow bird image
        rect_heights = [24*2, 23 * 2, 24 * 2, 21 * 2]  # Heights of each bird image

        running = True
        while running:
            self.screen.blit(BG, (0, 0))  # Draw the background

            # Display title
            title_text = font.render("Choose Bird Skin", True, BLACK)
            self.screen.blit(title_text, (150, 50))

            # Display skins
            for i, skin in enumerate(skins):
                self.screen.blit(skin, bird_positions[i])

            # Highlight selected skin
            pygame.draw.rect(self.screen, WHITE, (bird_positions[selected_skin_index][0], bird_positions[selected_skin_index][1], rect_width, rect_heights[selected_skin_index]), 2)

            # Display OK button
            ok_button_rect = pygame.Rect(165, 480, 100, 40)
            pygame.draw.rect(self.screen, GRAY, ok_button_rect)
            ok_text = font.render("OK", True, BLACK)
            self.screen.blit(ok_text, (195, 490))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if a skin is selected
                    for i, _ in enumerate(skins):
                        if pygame.Rect(bird_positions[i][0], bird_positions[i][1], rect_width, rect_heights[i]).collidepoint(mouse_pos):
                            selected_skin_index = i
                            print("Selected skin:", i + 1)  # Print the index of the selected skin
                            # Perform action based on selected skin (e.g., change character appearance)
                    # Check if OK button is clicked
                    if ok_button_rect.collidepoint(mouse_pos):
                        return selected_skin_index  # Return the selected skin index when OK is clicked
    def run(self):
        while True:
            self.screen.blit(self.BG, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for option_rect, option in zip(self.option_rects, self.options):
                        if option_rect.collidepoint(x, y):
                            # Check which option is clicked and return the appropriate action
                            if "level" in option["action"]:
                                # If it is a level option, return the level number
                                return option["action"]  # E.g., "level1"
                            elif option["action"] == "autoplay":
                                return "autoplay"
                            elif option["action"] == "skins":
                                selected_skin_index = self.choose_bird_skin()
                                if selected_skin_index is not None:
                                    return "skins", selected_skin_index
                            elif option["action"] == "exit":
                                pygame.quit()
                                sys.exit()

            # Draw the option text
            for option_rect, option in zip(self.option_rects, self.options):
                self.draw_text(option["text"], self.FONT, self.WHITE, option_rect.x, option_rect.y)

            pygame.display.flip()
            self.clock.tick(60)

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
                pipe_gap_center = (bottom_pipe_center + top_pipe_center - 250) / 2

                # Khoảng cách an toàn
                gap_margin = 85  # Tăng khoảng cách an toàn để tránh va chạm

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
            
def main():
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()
    screen = pygame.display.set_mode((432, 768))
    pygame.display.set_caption("Flappy Bird")

    # Khởi tạo menu
    menu = Menu(screen)
    selected_skin_index = 0  # Chỉ số da chim mặc định
    
    # Khởi tạo biến game trước khi vòng lặp bắt đầu
    game = None  # Đảm bảo biến được khởi tạo
     # Giao diện khởi động
    start_screen = StartScreen(screen)
    start_screen.run()  # Chạy giao diện khởi động

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        choice = menu.run()  # Lấy lựa chọn từ menu

        if isinstance(choice, str) and choice.startswith("level"):
            level_number = int(choice[-1])  # Lấy số cấp độ từ chuỗi
            game = Game(screen, level_number)  # Khởi tạo game với cấp độ hiện tại
            game.bird.change_skin(selected_skin_index)  # Đổi da chim
            game.reset_game()  # Đặt lại trò chơi
            game.set_auto_play(False)  # Đảm bảo chế độ tự động chơi đã tắt
            game.run_game()  # Bắt đầu trò chơi

        elif choice == "autoplay":
            if game is None:
                game = Game(screen, 1)  # Khởi tạo với cấp độ mặc định
            game.bird.change_skin(selected_skin_index)
            game.reset_game()
            game.set_auto_play(True)  # Bật chế độ tự động chơi
            game.run_game()  # Bắt đầu trò chơi trong chế độ tự động chơi

        elif isinstance(choice, tuple) and choice[0] == "skins":
            selected_skin_index = choice[1]
            if game:
                game.bird.change_skin(selected_skin_index)  # Đổi da chim nếu cần

        elif choice == "exit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()

