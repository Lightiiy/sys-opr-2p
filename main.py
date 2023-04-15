import os
import pygame
import random
import pygame as py
import threading
import time
from os import listdir
from os.path import isfile, join 

# DEFINE functions used for threading
def DUPA_function():
    print("DUPA_1")
    time.sleep(3)
    print("DUPSKO 2")

def TEST_function():
    print("TEST_1")
    time.sleep(6)
    print("TESTING 2")


if __name__ == "__main__":
# DEFINE a list of threads to join
    all_threads = list()
    for x in range(5):
      print(x)
# CREATE a thread and append it to a variable
      dupa = threading.Thread(target=DUPA_function)
      test = threading.Thread(target=TEST_function)
# APEND variable to the list of threads
      all_threads.append(dupa)
      all_threads.append(test)
# STARTS the threads 
      dupa.start()
      test.start()
# END the threads at the end of MAIN thread (program's thread)
    for index, thread in enumerate(all_threads):
        thread.join()

