import pygame
import sys
import random
from Bird import *
from Pipe import *
from Floor import *
from Game import *

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




