# Flappy-bird
def main():
    running = True
    play_button_img = pygame.image.load(r'image/playbutton.png')  # Load hình ảnh cho nút Play
    play_button_img = pygame.transform.scale(play_button_img, (300, 200))
    background = pygame.image.load(r'image/background.jpg')  # Icon và background
    background = pygame.transform.scale(background, (1000, 700))

    back_button_img = pygame.image.load(r'image/backbutton.png')  # Load hình ảnh cho nút Back
    back_button_img = pygame.transform.scale(back_button_img, (100, 50))
    back_button_rect = back_button_img.get_rect(topleft=(20, 20))

    show_back_button = False  # Biến để xác định xem nút Back có hiển thị hay không

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  #tạo để ấn vào được nút play
                mouse_pos = pygame.mouse.get_pos()
                if play_button_img is not None:  # Kiểm tra nút play có tồn tại không
                    button_rect = play_button_img.get_rect(topleft=(370, 170))
                    if button_rect.collidepoint(mouse_pos):
                        background_gp = pygame.image.load(r"image\\gp.jpg").convert()
                        background = pygame.transform.scale(background_gp, (1000, 700))
                        play_button_img = None  # Mất nút play
                        show_back_button = True  # Hiển thị nút Back khi chuyển đổi màn hình
                elif back_button_rect.collidepoint(mouse_pos):
                    # Xử lý sự kiện khi nhấn nút back và quay lại màn hình trước đó
                    background = pygame.image.load(r'image/background.jpg').convert()
                    background = pygame.transform.scale(background, (1000, 700))
                    play_button_img = pygame.image.load(r'image/playbutton.png')  # Tạo lại nút play
                    play_button_img = pygame.transform.scale(play_button_img, (300, 200))
                    show_back_button = False  # Ẩn nút Back khi quay lại background

        screen.blit(background, (0, 0))
        if play_button_img:  # Chỉ hiển thị nút play nếu play_button_img không phải None
            screen.blit(play_button_img, (370, 170))
        
        # Hiển thị nút "Back" nếu biến show_back_button là True
        if show_back_button:
            screen.blit(back_button_img, (20, 20))

        pygame.display.update()

if _name_ == "_main_":
    main()