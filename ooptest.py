import pygame
import sys
import random

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
        random_pipe_pos = random.choice(self.pipe_height)
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

class Game:
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()
        self.screen = pygame.display.set_mode((432, 768))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('04B_19.ttf', 35)
        self.bg = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())
        self.bird = Bird(self.screen)
        self.pipe = Pipe(self.screen)
        self.floor = Floor(self.screen)
        self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
        self.game_over_rect = self.game_over_surface.get_rect(center=(216, 384))
        self.flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
        self.hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
        self.score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
        self.score_sound_countdown = 100
        self.game_active = True
        self.score = 0
        self.high_score = 0

    def score_display(self):
        score_surface = self.game_font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        self.screen.blit(score_surface, score_rect)

        high_score_surface = self.game_font.render(f'High Score: {int(self.high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        self.screen.blit(high_score_surface, high_score_rect)

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def play_collision_sound(self):
        self.hit_sound.play()

    def check_collision(self):
        # Kiểm tra va chạm giữa chim và ống nước
        for pipe in self.pipe.pipe_list:
            if self.bird.bird_rect.colliderect(pipe):
                return True
        return False

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active:
                        self.bird.bird_movement = 0
                        self.bird.bird_movement = -11
                        self.flap_sound.play()
                    if event.key == pygame.K_SPACE and not self.game_active:
                        self.game_active = True
                        self.pipe.pipe_list.clear()
                        self.bird.bird_rect.center = (100, 384)
                        self.bird.bird_movement = 0
                        self.score = 0
                if event.type == self.pipe.spawnpipe_event:
                    self.pipe.pipe_list.extend(self.pipe.create_pipe())

            self.screen.blit(self.bg, (0, 0))

            if self.game_active:
                self.bird.update_movement()
                self.bird.bird_animation()
                self.bird.draw()
                self.game_active = not self.check_collision()  # Kiểm tra va chạm
                self.pipe.move_pipe()
                self.pipe.draw()
                self.score += 0.01
                self.score_display()
                self.score_sound_countdown -= 1
                if self.score_sound_countdown <= 0:
                    self.score_sound.play()
                    self.score_sound_countdown = 100
                if not self.game_active:
                    self.play_collision_sound()  # Phát âm thanh khi có va chạm
                    pygame.time.delay(1000)  # Dừng trò chơi trong 1 giây để người chơi có thể nhìn thấy màn hình game over
        
            else:
                self.screen.blit(self.game_over_surface, self.game_over_rect)
                self.update_high_score()
                self.score_display()
        
            self.floor.draw()
            self.floor.update_position()

            pygame.display.update()
            self.clock.tick(75)
        def check_collision(self, bird_rect, pipe_list):
            for pipe in pipe_list:
                if bird_rect.colliderect(pipe):
                    self.bird.play_hit_sound()
                    self.pipe.play_hit_sound()
                    return True
            if bird_rect.top <= -75 or bird_rect.bottom >= 650:
                return True
            return False



def main():
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()
    screen = pygame.display.set_mode((432, 768))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    
    game = Game()  # Tạo đối tượng Game
    floor = Floor(screen)  # Tạo đối tượng Floor

    play_button_img = pygame.image.load('assets/playbutton.png')
    play_button_img = pygame.transform.scale(play_button_img, (250, 250))
    play_button_rect = play_button_img.get_rect()
    play_button_rect.center = (216, 384)  # Đặt vị trí của nút play ở giữa màn hình
    game_started = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game.game_active:
                    game.bird.bird_movement = 0
                    game.bird.bird_movement = -11
                    game.flap_sound.play()
                if event.key == pygame.K_SPACE and not game.game_active:
                    game_started = True  # Đánh dấu rằng trò chơi đã bắt đầu
                    game.game_active = True
                    game.pipe.pipe_list.clear()
                    game.bird.bird_rect.center = (100, 384)
                    game.bird.bird_movement = 0
                    game.score = 0
            if event.type == game.pipe.spawnpipe_event:
                game.pipe.pipe_list.extend(game.pipe.create_pipe())
            if event.type == pygame.MOUSEBUTTONDOWN:  # Kiểm tra sự kiện click chuột
                if event.button == 1:  # Kiểm tra xem có phải là click chuột trái không
                    if play_button_rect.collidepoint(event.pos):  # Kiểm tra xem chuột có được click vào nút play không
                        game_started = True  # Đánh dấu rằng trò chơi đã bắt đầu

        screen.blit(game.bg, (0, 0))

        if not game_started:  # Nếu trò chơi chưa bắt đầu
            # Hiển thị nút play và sàn
            screen.blit(play_button_img, play_button_rect)
            floor.draw()  # Vẽ sàn
        else:
            # Hiển thị các phần tử trong trò chơi (chim, ống nước, điểm số) ở đây
            game.bird.update_movement()
            game.bird.bird_animation()
            game.bird.draw()
            game.game_active = not Collision.check_collision(game.bird.bird_rect, game.pipe.pipe_list)
            if not game.game_active:  # Nếu game kết thúc
                game.update_high_score()  # Cập nhật điểm cao nhất
                game.score_display()  # Hiển thị điểm số và điểm cao nhất
                screen.blit(game.game_over_surface, game.game_over_rect)  # Hiển thị màn hình kết thúc
            else:
                game.pipe.move_pipe()
                game.pipe.draw()
                game.score += 0.01
                game.score_sound_countdown -= 1
                if game.score_sound_countdown <= 0:
                    game.score_sound.play()
                    game.score_sound_countdown = 100
                game.floor.update_position()  # Cập nhật vị trí của sàn
                game.floor.draw()  # Vẽ sàn

        pygame.display.update()  # Cập nhật màn hình

        clock.tick(75)  # Giữ cho game chạy ở tốc độ 75 khung hình mỗi giây

if __name__ == "__main__":
    main()




