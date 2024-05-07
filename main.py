import pygame
import sys
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


