import pygame as py
import threading

import basics
import surface
from player import Player as PlayerObject


BG_COLOR = (255,255,255)
WIDTH, HEIGHT = 640, 640
FPS = 30
THREAD_DELAY = 30
bgFiles = [ "Blue.png","Pink.png","Purple.png","Yellow.png"]
run = True
player1 = PlayerObject(10, 10, 100, 100)

window = py.display.set_mode((WIDTH,HEIGHT))

THREADS = list()
py.display.set_caption("Scalar")

def start_threads():
    for index, thread in enumerate(THREADS):
        thread.start()

def join_threads():
    for index, thread in enumerate(THREADS):
        thread.join()
        
#THREAD 2 - PLAYER MOVEMENT
def handle_movement():
    while run:
        player1.loop(FPS)
        py.time.delay(THREAD_DELAY)




#THREAD 3 - GENERATE PLATFORMS AT RANDOM HEIGHTS & MOVE THEM?
def handle_vertical_collision():
    collided_surface=[]
    for obj in floor:
        if py.sprite.collide_mask(player1, obj):
            if player1.y_vel > 0:
                player1.rect.bottom = obj.rect.top
                player1.landed()
            elif player1.y_vel < 0:
                player1.rect.top = obj.rect.bottom
                player1.hit_head()

        collided_surface.append(obj)
    return collided_surface
            
        
def main(window):
    py.init()    
    global run
    clock =  py.time.Clock()

    blocks_size = 96
    global floor
    floor = [surface.Block(i*blocks_size, HEIGHT - blocks_size, blocks_size) for i in range(-WIDTH // blocks_size, (WIDTH *2) //blocks_size)]

    PLAYER_HANDLE = threading.Thread(target=handle_movement)
    SURFACE_COLLISION = threading.Thread(target=handle_vertical_collision)
    THREADS.append(PLAYER_HANDLE)
    THREADS.append(SURFACE_COLLISION)
    start_threads()

    while run:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                join_threads()        
                py.quit()
                exit()
        bgArea, bgImage = basics.get_image("Background",bgFiles[0],WIDTH, HEIGHT)
        basics.draw(window,bgArea,bgImage);  
        player1.draw(window)
        for block in floor:
            block.draw(window)
        py.display.flip()
            
    py.quit()
    quit()


if __name__ == "__main__":
    main(window)


