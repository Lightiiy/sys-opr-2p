import os
import pygame
import random
import pygame as py
import threading
import time
from os import listdir
from os.path import isfile, join 

BG_COLOR = (255,255,255)
WIDTH, HEIGHT = 640, 640
FPS = 60
P_VELOCITY = 5

# DEFINE functions used for threading
py.init()    
py.display.set_caption("Scalar")
window = py.display.set_mode((WIDTH,HEIGHT))

def DUPA_function():
    print("DUPA_1")
    time.sleep(3)
    print("DUPSKO 2")

def TEST_function():
    print("TEST_1")
    time.sleep(6)
    print("TESTING 2")

def main(window):
    clock =  py.time.Clock()

    run = True
    while run:
      clock.tick(FPS)

      for event in py.event.get():
          if event.type == py.QUIT:
              run = False
              break
          
    py.quit()
    quit()


if __name__ == "__main__":
    main(window)


# # DEFINE a list of threads to join
#     all_threads = list()
#     for x in range(5):
#       print(x)
# # CREATE a thread and append it to a variable
#       dupa = threading.Thread(target=DUPA_function)
#       test = threading.Thread(target=TEST_function)
# # APEND variable to the list of threads
#       all_threads.append(dupa)
#       all_threads.append(test)
# # STARTS the threads 
#       dupa.start()
#       test.start()
# # END the threads at the end of MAIN thread (program's thread)
#     for index, thread in enumerate(all_threads):
#         thread.join()
