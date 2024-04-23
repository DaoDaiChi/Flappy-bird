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

    menu = Menu(screen)  # Giả định bạn có lớp Menu
    game = None
    selected_skin_index = 0  # Chỉ số skin được chọn mặc định

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Thoát chương trình nếu người dùng muốn đóng cửa sổ

        choice = menu.run()  # Giả định phương thức run() của Menu trả về một lựa chọn

        if choice == "start":  # Nếu người dùng chọn bắt đầu trò chơi
            if game is None:
                game = Game(screen)  # Tạo một đối tượng Game mới nếu chưa có
            game.bird.change_skin(selected_skin_index)  # Đảm bảo skin đã chọn được áp dụng trước khi chạy trò chơi
            game.reset_game()  # Đặt lại trò chơi
            game.run_game()  # Chạy trò chơi

        elif isinstance(choice, tuple) and choice[0] == "skins":  # Nếu người dùng chọn thay đổi skin
            selected_skin_index = choice[1]  # Lấy chỉ số của skin được chọn
            if game:
                game.bird.change_skin(selected_skin_index)  # Áp dụng skin mới cho chim nếu trò chơi đã được tạo

        elif choice == "quit":  # Nếu người dùng chọn thoát
            pygame.quit()
            sys.exit()  # Thoát chương trình nếu người dùng muốn dừng hẳn

if __name__ == "__main__":
    main()


