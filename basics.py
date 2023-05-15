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

# def load_sprite_sheets(dir1,dir2,width,height,direction=False):
#     path=join("assets",dir1,dir2)
#     images = [f for f in listdir(path) if isfile(join(path,f))]

#     all_sprites = {}

#     for image in images:
#         sprite_sheet = py.image.load(join(path,image)).convert_alpha()
#         sprites = []

#         for i in range(sprite_sheet.get_width() // width):
#             surface = py.Surface((width,height), py.SRCALPHA,32)
#             rect = py.Rect(i * width, 0, width, height)
#             surface.blit(sprite_sheet,(0,0),rect)
#             sprites.append(py.transform.scale2x(surface))

#         if direction:
#             all_sprites[image.replace(".png","")+ "_right"] = sprites
#         else:
#             all_sprites[image.replace(".png","")] = sprites
#     return all_sprites