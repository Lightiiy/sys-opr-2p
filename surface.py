import pygame as py
import basics


class Block(basics.Object):
    def __init__(self,x, y, size):
      super().__init__(x,y,size,size)
      block = self.get_block(size)
      self.image.blit(block, (0,0))
      self.mask = py.mask.from_surface(self.image)

    def get_block(self, size):
       path = basics.get_sprite_block("Terrain", "Terrain.png")
       image = py.image.load(path)
       surface = py.Surface((size, size), py.SRCALPHA, 32)
       rect = py.Rect(96, 0, size, size)
       surface.blit(image, (0,0), rect)
       return py.transform.scale2x(surface)
    
    