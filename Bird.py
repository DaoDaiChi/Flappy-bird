import pygame

class Bird:
    def __init__(self, screen, initial_skin_index=0,gravity=0.7):
        """
        Khởi tạo Bird với màn hình Pygame, chỉ số skin ban đầu, và trọng lực.

        :param screen: Màn hình Pygame nơi chim được vẽ.
        :param initial_skin_index: Chỉ số của skin chim ban đầu.
        :param gravity: Trọng lực tác động lên chim, mặc định là 0.7.
        """
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
        """
        Xoay chim dựa trên chuyển động hiện tại.

        :return: Hình ảnh chim sau khi xoay.
        """
        new_bird = pygame.transform.rotozoom(self.bird, -self.bird_movement * 3, 1)
        return new_bird

    def bird_animation(self):
        """
        Thay đổi skin của chim theo skin hiện tại và giữ nguyên vị trí.
        """
        self.bird = self.bird_skins[self.current_skin_index]
        self.bird_rect = self.bird.get_rect(center=self.bird_rect.center)

    def update_movement(self):
        """
        Cập nhật chuyển động của chim dựa trên trọng lực.
        """
        self.bird_movement += self.gravity
        self.bird_rect.centery += self.bird_movement

    def draw(self):
        rotated_bird = self.rotate_bird()
        self.screen.blit(rotated_bird, self.bird_rect)

    def change_skin(self, new_skin_index):
        """
        Thay đổi skin của chim theo chỉ số mới.

        :param new_skin_index: Chỉ số của skin mới.
        """
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