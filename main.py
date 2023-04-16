import os
import random
import pygame as py
import threading
import time
from os import listdir
from os.path import isfile, join 

import basics

BG_COLOR = (255,255,255)
WIDTH, HEIGHT = 640, 640
FPS = 60
P_VELOCITY = 5
bgFiles = [ "Blue.png","Pink.png","Purple.png","Yellow.png"]


THREADS = list()
py.init()    
py.display.set_caption("Scalar")
window = py.display.set_mode((WIDTH,HEIGHT))

def background():
    pass

def joinThreads():
    for index, thread in enumerate(THREADS):
        thread.join()

def drawBackground():
    for i in range(5): 
        print(i)
        i = i%4
        image = bgFiles[i] 
        bgArea, bgImage = basics.get_image("Background",image,WIDTH, HEIGHT)
        basics.draw(window,bgArea,bgImage);  
        time.sleep(2)      

def main(window):
    clock =  py.time.Clock()
    run = True
    DRAW_BACKGROUND = threading.Thread(target=drawBackground)
    THREADS.append(DRAW_BACKGROUND)
    DRAW_BACKGROUND.start()

    while run:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                break
    joinThreads()      
    py.quit()
    quit()


if __name__ == "__main__":
    main(window)


# # DEFINE a list of threads to join
#     all_threads = list()
#     for x in range(5):
#       print(x)
# # CREATE a thread and append it to a variable
#       test = threading.Thread(target=TEST_function)
# # APEND variable to the list of threads
#       all_threads.append(test)
# # STARTS the threads 
s#       test.start()
# # END the threads at the end of MAIN thread (program's thread)
#     for index, thread in enumerate(all_threads):
#         thread.join()
