import pygame, sys
import numpy as np

pygame.init()
screen = pygame.display.set_mode((432,768))
speed =pygame.time.Clock()# Setup fps
#Background insert
background = pygame.image.load('assets/background-night.png')
background = pygame.transform.scale2x(background)
#Floor insert
floor = pygame.image.load('assets/floor.png')
floor = pygame.transform.scale2x(floor)
#Flappy bird insert
bird = pygame.image.load('assets/yellowbird-midflap.png')
bird = pygame.transform.scale2x(bird)
bird_box_cover = bird.get_rect(center = (100,384))

#Movemet 
game_active = True   
gravity = 1
bird_movement = 0
#pipe insert
pipe_layout = pygame.image.load('assets/pipe-green.png')
pipe_layout = pygame.transform.scale2x(pipe_layout)
pipe_list = []
pipe_height = [400,550,500,300,290]
# spawn_timing
spawn = pygame.USEREVENT
pygame.time.set_timer(spawn,1200)
# FUNCTION
##Create_pipe
def create_pipe():
    random_pipe_pos = np.random.choice(pipe_height)
    bottom_pipe = pipe_layout.get_rect(midtop =(400,random_pipe_pos))
    top_pipe = pipe_layout.get_rect(midtop =(400,random_pipe_pos-700))
    return bottom_pipe, top_pipe
## Move pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
## Draw pipe
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 768 :
            screen.blit(pipe_layout,pipe)
        else:
            flip_pipe = pygame. transform. flip(pipe_layout,False, True)
            screen.blit(flip_pipe,pipe)
# Create one more floors
def fake_floor() :
    screen.blit(floor,(floor_left_moving,600))
    screen.blit(floor,(floor_left_moving+432,600))
#Collisions
def collisions(pipes):
    for pipe in pipes:
        if bird_box_cover.colliderect(pipe):
            return False 
    if bird_box_cover.top <= -75 or bird_box_cover.bottom >= 650:
            return False
    return True
floor_left_moving = 0 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_SPACE :
                bird_movement = 0
                bird_movement -= 11  
        if event.type == spawn:
            pipe_list.extend(create_pipe())
    screen.blit(background,(0,0))
    if game_active:
        #bird details
        bird_movement += gravity
        bird_box_cover.centery += bird_movement
        screen.blit(bird,bird_box_cover)
        game_active = collisions(pipe_list) 
        #pipe details
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
    
    #floor details
    floor_left_moving -= 1 #Left moving constantly
    fake_floor()
    if floor_left_moving <= -432: #khi chạy hết 2 sàn thì đổi chổ lân phiên để chạy tiếp
        floor_left_moving = 0
    
    pygame.display.update() 
    speed.tick(50) #120 fps