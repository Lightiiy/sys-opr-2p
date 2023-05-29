import pygame as py
import threading

import basics
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
        
#THREAD 1 - SCENE DRAW
def draw_scene():
     while run:
        bgArea, bgImage = basics.get_image("Background",bgFiles[0],WIDTH, HEIGHT)
        basics.draw(window,bgArea,bgImage);  
        player1.draw(window)
        py.display.flip()



#THREAD 2 - PLAYER MOVEMENT
def handle_movement():
    while run:
        player1.loop(FPS)
        py.time.delay(THREAD_DELAY)
        
def main(window):
    py.init()    
    global run
    clock =  py.time.Clock()
    DRAW_SCENE = threading.Thread(target=draw_scene, daemon=True)
    PLAYER_HANDLE = threading.Thread(target=handle_movement)
    THREADS.append(DRAW_SCENE)
    THREADS.append(PLAYER_HANDLE)
    start_threads()

    while run:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                join_threads()        
                py.quit()
                exit()
            
    py.quit()
    quit()


if __name__ == "__main__":
    main(window)


