import pygame
import sys

pygame.init()

# Định nghĩa kích thước màn hình
screen = pygame.display.set_mode((432, 768))
pygame.display.set_caption("My Game")

#Background insert
background_imagine = pygame.image.load('assets/background-night.png')
background_imagine = pygame.transform.scale2x(background_imagine)

#Floor insert
floor = pygame.image.load('assets/floor.png')
floor = pygame.transform.scale2x(floor)
def fake_floor() :
    screen.blit(floor,(floor_x_pos,600))
    screen.blit(floor,(floor_x_pos+432,600))
# Load hình ảnh và thay đổi kích thước của nút play
play_button_img = pygame.image.load('assets/playbutton.png')
play_button_img = pygame.transform.scale(play_button_img, (250, 250))
play_button_rect = play_button_img.get_rect()
play_button_rect.center = (216, 384)  # Đặt vị trí của nút play ở giữa màn hình

# Biến để kiểm soát vòng lặp
running = True
game_started = False
floor_x_pos = 0
floor_speed = 1

clock = pygame.time.Clock()  # Tạo một đối tượng Clock để kiểm soát tốc độ của game

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Kiểm tra sự kiện click chuột
            if event.button == 1:  # Kiểm tra xem có phải là click chuột trái không
                if play_button_rect.collidepoint(event.pos):  # Kiểm tra xem chuột có được click vào nút play không
                    game_started = True  # Đánh dấu rằng trò chơi đã bắt đầu

    screen.blit(background_imagine, (0, 0))

    if not game_started:  # Nếu trò chơi chưa bắt đầu
        # Hiển thị nút play và sàn
        screen.blit(play_button_img, play_button_rect)
        screen.blit(floor, (0, 600))
    else:
        # Hiển thị sàn di chuyển và ẩn nút play
        floor_x_pos -= 1
        fake_floor()
        if floor_x_pos <= -432:  # Khi sàn di chuyển hết ra khỏi màn hình
            floor_x_pos = 0  # Đặt lại vị trí của sàn

    pygame.display.update()  # Cập nhật màn hình

    clock.tick(60)  # Giữ cho game chạy ở tốc độ 60 khung hình mỗi giây

pygame.quit()
sys.exit()
