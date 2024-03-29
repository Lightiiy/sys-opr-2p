import pygame as py
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

def get_sprite_block(type, name):
    return join("assets",type,name)

def draw(window, area, image):
    for tile in area:
        window.blit(image, tile)

def flip(sprites):
    return [py.transform.flip(sprite,True, False) for sprite in sprites]

def load_sprite_sheets(dir1,dir2,width,height,direction=False):
    path=join("assets",dir1,dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = py.image.load(join(path,image))
        sprites = []

        for i in range(sprite_sheet.get_width() // width):
            surface = py.Surface((width,height), py.SRCALPHA,32)
            rect = py.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet,(0,0),rect)
            sprites.append(py.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png","")+ "_right"] = sprites
            all_sprites[image.replace(".png","")+ "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png","")] = sprites
    return all_sprites

class Object(py.sprite.Sprite):
    def __init__(self, x,y,width,height,name=None):
        self.rect = py.Rect(x , y, width, height)
        self.image = py.Surface((width,height), py.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
  
    def draw(self, window):
        self.image.unlock()
        window.blit(self.image, (self.rect.x, self.rect.y))
        self.image.lock()
