import pygame as py
import basics

blocks_size = 96
max_segments = 6
min_segments = 1
max_height_diff = 2 * blocks_size
max_platform_speed = 0
platform_speed = 1

class Block(basics.Object):

    def __init__(self,x, y, size):
      super().__init__(x,y,size,size)
      block = self.get_block(size)
      self.image.blit(block, (0,0))
      self.mask = py.mask.from_surface(self.image)
      self.x = x
      self.y = y
      self.isLast = False

    def get_block(self, size):
       path = basics.get_sprite_block("Terrain", "Terrain.png")
       image = py.image.load(path)
       surface = py.Surface((size, size), py.SRCALPHA, 32)
       rect = py.Rect(96, 0, size, size)
       surface.blit(image, (0,0), rect)
       return py.transform.scale2x(surface)
    
    def update(self):
       self.rect.x = self.x
       self.rect.y = self.y
    
    def move_left(self, dx):
       self.x -= dx
       self.update()

