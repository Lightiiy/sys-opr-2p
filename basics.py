import os
import random
import pygame as py
import time
from os import listdir
from os.path import isfile, join 

def get_image(type, name, areaWidth, areaHeight):
    image = py.image.load(join("assets",type,name))
    #first to variables recieved are X and Y cooridnates, which we don't need
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(areaWidth // width + 1):
        for j in range(areaHeight // height + 1):
            pos = (i * width, j*height)
            tiles.append(pos)
    return tiles, image

def draw(window, area, image):
    for tile in area:
        window.blit(image, tile)
        
    py.display.update()