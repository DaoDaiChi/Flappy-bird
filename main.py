import pygame
import sys
import random
from Bird import *
from Pipe import *
from Floor import *
from Game import *
from Menu import *

def main():
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()
    screen = pygame.display.set_mode((432, 768))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    menu = Menu(screen)
    game = None
    bird = Bird(screen)  # Create Bird instance
    
    BLACK = (0, 0, 0)  # Define the BLACK color
    selected_skin_index = 0  # Default selected skin index

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        choice = menu.run()

        if choice == "start":
            if game is None:
                game = Game()  # Create Game instance
                floor = Floor(screen)

            bird.change_skin(selected_skin_index)  # Change bird's skin
            
            game_started = True  # Set game_started to True directly
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and game.game_active:
                            bird.bird_movement = 0
                            bird.bird_movement = -11
                            game.flap_sound.play()
                        if event.key == pygame.K_SPACE and not game.game_active:
                            game_started = True
                            game.game_active = True
                            game.pipe.pipe_list.clear()
                            bird.bird_rect.center = (100, 384)
                            bird.bird_movement = 0
                            game.score = 0
                    if event.type == game.pipe.spawnpipe_event:
                        game.pipe.pipe_list.extend(game.pipe.create_pipe())
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return  # Return to main menu on ESC key press

                screen.blit(game.bg, (0, 0))

                bird.update_movement()
                bird.bird_animation()
                bird.draw()
                game.game_active = not Collision.check_collision(bird.bird_rect, game.pipe.pipe_list)
                if not game.game_active:
                    game.update_high_score()
                    game.score_display()
                    screen.blit(game.game_over_surface, game.game_over_rect)
                    # Hiển thị nút back và xử lý sự kiện click chuột
                    back_button_rect = pygame.Rect(10, 10, 50, 50)
                    screen.blit(game.back_button_image, game.back_button_rect)  # Vẽ nút back
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
                            game = None  # Reset game instance
                            break  # Thoát khỏi vòng lặp hiện tại để trở về main menu

                else:
                    game.pipe.move_pipe()
                    game.pipe.draw()
                    game.score += 0.01
                    game.score_sound_countdown -= 1
                    if game.score_sound_countdown <= 0:
                        game.score_sound.play()
                        game.score_sound_countdown = 100
                    game.floor.update_position()
                    game.floor.draw()

                pygame.display.update()

                clock.tick(75)

        elif choice[0] == "skins":  # Xử lý lựa chọn "skins" trả về từ Menu.run()
            selected_skin_index = choice[1]  # Lấy chỉ số skin được chọn
            print("Selected skin:", selected_skin_index)  # In ra chỉ số của skin được chọn
            bird.change_skin(selected_skin_index)  # Thay đổi skin của bird

if __name__ == "__main__":
    main()




