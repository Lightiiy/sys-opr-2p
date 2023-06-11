import pygame as py
import threading
import random
import basics
import surface
from player import Player as PlayerObject

WIDTH, HEIGHT = 820, 640
FPS = 60
THREAD_DELAY = 1
bgFiles = "Blue.png"
run = True
start = False

player1 = PlayerObject(10, 10, 100, 100)

window = py.display.set_mode((WIDTH,HEIGHT))
THREADS = list()
lock = threading.Lock()
py.display.set_caption("Scalar")

def start_threads(threads):
    for index, thread in enumerate(threads):
        thread.start()

def join_threads(threads):
    for index, thread in enumerate(threads):
        thread.join()

#MAIN THREAD - CANT BE A SEPERATE ONE, CAUSES ISSUES IN PYGAME
#Draw background
#Then invoke draw() function of all objects  
def draw_scene():
        bgArea, bgImage = basics.get_image("Background",bgFiles,WIDTH, HEIGHT)
        basics.draw(window,bgArea,bgImage) 
        player1.draw(window)
        for block in platforms:
                block.draw(window)
        py.display.flip()
        
#THREAD 1 - PLAYER MOVEMENT
# Thread wich registers players collisions and handles his movement
def handle_movement():
    collide_left=False
    collide_right=False
    while run:  
        clock.tick(FPS)
        with lock:
            player1.loop(FPS, collide_left, collide_right)
            collide_left = handle_horizontal_collision(-player1.P_VELOCITY)
            collide_right = handle_horizontal_collision(player1.P_VELOCITY)
            handle_vertical_collision()

#Vertical collision
#If player touches the top of a platform, Set his gravit and Y velocity to 0
#If player touches the bottom of a platfor, "bounce" him back
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
        
#Horizontal collision
# If player reaches the left/right side of the platform, he can't move into the platform
# He also shouldn't be moved to the top of the platform/bounced to the bottom
# (Behaviour based only on players Y speed at the moment of touching the platform)
def handle_horizontal_collision(player_dx_velocity):
    player1.move(player_dx_velocity, 0)
    collided_object = False
    for obj in platforms:
         if py.sprite.collide_mask(player1, obj):
              collided_object = True
              break
    player1.move(-player_dx_velocity, 0)
    return collided_object

#Platforms are generated with a random amounts of segments (Blocks)
#They can only generate in a given height difference from the last segment.
#Segments are appended to the main list after generatung
def generate_platform():
# Randomly determine the length of the platform
    num_segments = random.randint(surface.min_segments, surface.max_segments)
    prev_platform = platforms[-1] if platforms else None
    if prev_platform:
        min_height = prev_platform.y - surface.max_height_diff
        max_height = prev_platform.y + surface.max_height_diff
        platform_y = random.randint(min_height, max_height) % HEIGHT
    else:
        platform_y = random.randint(0, WIDTH//2)
    platform = [surface.Block(WIDTH + surface.blocks_size * i, platform_y, surface.blocks_size) for i in range (num_segments)]

    for block in platform:
        with lock:
            platforms.append(block)


#Generate the first platform where player can get familiar with speed and jump height of the character
def generate_start():
    platform = [surface.Block(i * surface.blocks_size, HEIGHT - surface.blocks_size, surface.blocks_size) for i in range(0, (WIDTH // surface.blocks_size ) + 1)]
    for block in platform:
        platforms.append(block)

#THREAD 2 - GENERATE PLATFORMS AT RANDOM HEIGHTS & MOVE THEM
#Decides when the new platform should be generated
#With new platform generation, the speed of the platforms is rised by 25%
def handle_platforms():
    global challenge
    challenge = 1
    generate_start()
    while run:
        clock.tick(FPS)
        if start:
            if(len(platforms)) <= 4: 
                    generate_platform()
                    challenge = challenge * 1.25 if challenge <= surface.max_platform_speed else challenge * 1
                    py.time.delay(THREAD_DELAY)
            move()

#Simple function with moves the platforms
#Removes the platforms from the list if they are outside the game window (only left side)
def move():
    for platform in platforms:
        if platform.x + surface.blocks_size < 0:
            platforms.pop(0)
            py.time.delay(THREAD_DELAY)
        platform.move_left(challenge)
        

#SUB THREADS - move assigned object to left
#IDEA DITCHED - this is so performance heavy it makes my pc look like Electronic Delay Storage Automatic Calculator from 1948
# def move_platform(block):
#     while run:
#         block.move_left(platforms_speed)
#         py.time.delay(THREAD_DELAY)
#
#  [surface.Block(i * surface.blocks_size, HEIGHT - surface.blocks_size, surface.blocks_size) for i in range(-WIDTH // surface.blocks_size, (WIDTH * 2) // surface.blocks_size)  ] 

def main():
    py.init()
    py.mixer.init()
    deathsfx = py.mixer.Sound('assets/SoundEffects/Boo-womp.wav')

    global run
    global start
    global clock
    global platforms

    clock =  py.time.Clock()
    platforms = []

    #CREATE AND APPEND NEW THREAD TO THE LIST OF THREADS
    #PLATFORM HANDLER THREAD
    # It creates platforms and moves them to the left
    # Speed at which does platforms move slowly builds up until it reaches speed equal to the player
    # Where the platforms generate is random. New platforms are generated, when 
    # the length of the platforms array is equal or less than 4
    PLATFORM_HANDLER = threading.Thread(target=handle_platforms,daemon=True)
    THREADS.append(PLATFORM_HANDLER)

    #PLAYER HANDLER
    # It invokes players movement loop and checks collisions (both horizontal and vertical)
    # Each tick of the game collision handlers check if player is about to reach a platform side
    # And then locks players movement in the appropriate direction if it would
    # end up putting the player inside of the platform
    PLAYER_HANDLER = threading.Thread(target=handle_movement,daemon=True)
    THREADS.append(PLAYER_HANDLER)

    #START THREADS
    start_threads(THREADS)

    while run:
        clock.tick(FPS)
        for event in py.event.get():
            #Player starts in a "start area"
            #After pressing Enter, start the game
            if event.type == py.KEYDOWN:
                if event.key == py.K_RETURN:
                    start = True
            #run shouldn't be true if the QUIT event was emitted
            if event.type == py.QUIT:
                run = False
            #Join threads and run = false when player falls down
            #GAME OVER
            if player1.rect.top > HEIGHT:
                deathsfx.play()
                while py.mixer.get_busy():
                    py.time.Clock().tick(10)
                run = False
                join_threads(THREADS)
        # Draw the scene
        # with lock to ensure safety for drawing the scenes in pygame
        with lock:
            draw_scene()
    #Close the app
    join_threads(THREADS)
    py.quit()
    quit()


if __name__ == "__main__":
    main()


