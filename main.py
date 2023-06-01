import pygame as py
import threading
import random
import pprint

import basics
import surface
from player import Player as PlayerObject


BG_COLOR = (255,255,255)
WIDTH, HEIGHT = 640, 640
FPS = 60
THREAD_DELAY = 25
bgFiles = [ "Blue.png","Pink.png","Purple.png","Yellow.png"]
run = True
player1 = PlayerObject(10, 10, 100, 100)

window = py.display.set_mode((WIDTH,HEIGHT))

THREADS = list()

lock = threading.Lock()
py.display.set_caption("Scalar")

def start_threads():
    for index, thread in enumerate(THREADS):
        thread.start()

def join_threads():
    for index, thread in enumerate(THREADS):
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
blocks_size = 96
max_segments = 8
min_segments = 4
max_height_diff = 2 * blocks_size
platform_speed = 1
max_platform_speed = 0


# def generate_platform():
#     global platforms

#     # Randomly determine the length of the platform
#     num_segments = random.randint(min_segments, max_segments)

#     # Determine the height of the platform based on the previous platform (if any)
#     prev_platform = platforms[-1] if platforms else None
#     if prev_platform:
#         min_height = prev_platform.y - max_height_diff
#         max_height = prev_platform.y + max_height_diff
#         platform_y = random.randint(min_height, max_height)
#     else:
#         platform_y = random.randint(0, WIDTH - blocks_size)

#     platform = [surface.Block(blocks_size* i,HEIGHT - blocks_size * platform_y, blocks_size) for i in range (num_segments)]
#     # py.Rect(WIDTH, platform_y, platform_width, blocks_size)
#     with lock:
#         platforms.append(platform)

# def handle_platforms():
#     global platforms, platform_speed

#     while True:
#         with lock:
#             for platform in platforms[0]:
#                 platform.x -= platform_speed

#             # Remove platforms that have moved out of view
#             # if platforms:
#                 # first_platform = platforms[0]
#                 # if first_platform.x + first_platform.width < 0:
#                     # platforms.pop(0)

#                     # # Generate a new platform when the first platform is removed
#                     # if len(platforms) == 1:
#                     #     generate_platform()
#                     #     generate_platform()
#                     # else:
#                     #     generate_platform()
#         py.time.delay(THREAD_DELAY)

#         # Increase the platform speed gradually up to the maximum speed
#         if platform_speed < max_platform_speed:
#             platform_speed += 0.01

        
def main(window):
    py.init()    
    global run
    clock =  py.time.Clock()

    # generate_platform()
    
    # global platforms
    # platforms = [surface.Block(i * blocks_size, HEIGHT - blocks_size, blocks_size) for i in range(-WIDTH // blocks_size, (WIDTH * 2) // blocks_size)]
    # platforms.append(surface.Block(blocks_size, HEIGHT - blocks_size* 2, blocks_size) )

    # PLATFORM_HANDLER = threading.Thread(target=handle_platforms,daemon=True)
    # THREADS.append(PLATFORM_HANDLER)

    PLAYER_HANDLER = threading.Thread(target=handle_movement)
    THREADS.append(PLAYER_HANDLER)

    start_threads()

    while run:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
        with lock:
            draw_scene()

    join_threads()            
    py.quit()
    quit()


if __name__ == "__main__":
    main(window)


