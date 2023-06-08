import pygame as py
import threading
import random

import basics
import surface
from player import Player as PlayerObject


BG_COLOR = (255,255,255)
WIDTH, HEIGHT = 1080, 640
FPS = 60
THREAD_DELAY = 5
bgFiles = [ "Blue.png","Pink.png","Purple.png","Yellow.png"]
run = True
start = False
player1 = PlayerObject(10, 10, 100, 100)

window = py.display.set_mode((WIDTH,HEIGHT))
lock = threading.Lock()

THREADS = list()

PLATFORM_THREADS = list()

lock = threading.Lock()
py.display.set_caption("Scalar")

def start_threads(threads):
    for index, thread in enumerate(threads):
        thread.start()

def join_threads(threads):
    for index, thread in enumerate(threads):
        thread.join()
        


#MAIN THREAD - CANT BE A SEPERATE ONE, CAUSES ISSUES IN PYGAME 
def draw_scene():
        bgArea, bgImage = basics.get_image("Background",bgFiles[0],WIDTH, HEIGHT)
        basics.draw(window,bgArea,bgImage) 
        player1.draw(window)
        for block in platforms:
                block.draw(window)
        py.display.flip()
        
#THREAD 1 - PLAYER MOVEMENT
def handle_movement():
    collide_left=False
    collide_right=False
    while run:  
        with lock:
            player1.loop(FPS, collide_left, collide_right)
            collide_left = handle_horizontal_collision(-player1.P_VELOCITY)
            collide_right = handle_horizontal_collision(player1.P_VELOCITY)
            handle_vertical_collision()
        py.time.delay(THREAD_DELAY)


def handle_vertical_collision():
    collided_platforms = []
    for obj in platforms:
        if py.sprite.collide_mask(player1, obj):
            if player1.y_vel > 0:
                player1.rect.bottom = obj.rect.top
                player1.landed()
            elif player1.y_vel < 0:
                player1.rect.top = obj.rect.bottom
                player1.hit_head()
        
        collided_platforms.append(obj)
        
    
def handle_horizontal_collision(player_dx_velocity):
    player1.move(player_dx_velocity, 0)
    collided_object = False
    for obj in platforms:
         if py.sprite.collide_mask(player1, obj):
              collided_object = True
              break
    player1.move(-player_dx_velocity, 0)
    return collided_object

#THREAD 2 - GENERATE PLATFORMS AT RANDOM HEIGHTS & MOVE THEM?

def generate_platform():
# Randomly determine the length of the platform
    num_segments = random.randint(surface.min_segments, surface.max_segments)
    # # Determine the height of the platform based on the previous platform (if any)
    prev_platform = platforms[-1] if platforms else None
    if prev_platform:
        min_height = prev_platform.y - surface.max_height_diff
        max_height = prev_platform.y + surface.max_height_diff
        platform_y = random.randint(min_height, max_height)
    else:
        platform_y = random.randint(0, WIDTH - surface.blocks_size)
    platform = [surface.Block(WIDTH + surface.blocks_size * i, platform_y, surface.blocks_size) for i in range (num_segments)]
    platform[num_segments-1].isLast = True

    for block in platform:
        with lock:
            platforms.append(block)

def generate_start():
    platform = [surface.Block(i * surface.blocks_size, HEIGHT - surface.blocks_size, surface.blocks_size) for i in range(0, WIDTH // surface.blocks_size)]
    platform[4].isLast = True
    for block in platform:
        platforms.append(block)


def handle_platforms():
    while run:
        if platforms:
            if platforms[-1].x + platforms[-1].width < 0:
                print(platforms[-1].isLast)
                with lock:
                    first_platform = platforms.pop()
                    if first_platform.isLast:
                        generate_platform()
        else:
            generate_start()

        for block in platforms:
            if start:
                block.move_left(surface.platform_speed)
            
        py.time.delay(THREAD_DELAY)


#SUB THREADS - move assigned object to left
#IDEA DITCHED - this is so performance heavy it makes my pc look like Electronic Delay Storage Automatic Calculator from 1948
# def move_platform(block):
#     while run:
#         block.move_left(platforms_speed)
#         py.time.delay(THREAD_DELAY)
#
#  [surface.Block(i * surface.blocks_size, HEIGHT - surface.blocks_size, surface.blocks_size) for i in range(-WIDTH // surface.blocks_size, (WIDTH * 2) // surface.blocks_size)  ] 

def main(window):
    py.init()    
    global run
    global start
    clock =  py.time.Clock()

    global platforms
    platforms = []

    PLATFORM_HANDLER = threading.Thread(target=handle_platforms,daemon=True)
    THREADS.append(PLATFORM_HANDLER)

    PLAYER_HANDLER = threading.Thread(target=handle_movement,daemon=True)
    THREADS.append(PLAYER_HANDLER)

    start_threads(THREADS)

    while run:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_RETURN:
                    start = True
            if event.type == py.QUIT:
                run = False
        with lock:
            draw_scene()

    join_threads(THREADS)
    join_threads(PLATFORM_THREADS)            
    py.quit()
    quit()


if __name__ == "__main__":
    main(window)


