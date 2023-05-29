import pygame as py
from os import listdir
from os.path import isfile, join 
import basics


class Player(py.sprite.Sprite):
  COLOR = (255,0,0)
  P_VELOCITY = 5
  G_ACCELERATION = 1
  SPRITES = basics.load_sprite_sheets("MainCharacters","PinkMan",32,32,True)

  def __init__(self, x,y,width,height):
    self.rect = py.Rect(x,y,width,height)
    self.x_vel = 0
    self.y_vel = 0
    self.mask = None
    self.direction = "left"
    self.animation_count = 0
    self.gravity_count = 0

  def move(self,dx,dy):
    self.rect.x += dx
    self.rect.y += dy

  def move_left(self, vel):
    self.x_vel = -vel
    if self.direction != "left":
      self.direction = "left"
      self.animation_count = 0

  def slow_down(self):
    if (self.x_vel != 0):
      self.x_vel = self.x_vel / 10
      if (self.x_vel <= 0.5 ):
        self.x_vel = 0    

  def move_right(self, vel):
    self.x_vel = vel
    if self.direction != "right":
      self.direction = "right"
      self.animation_count = 0

  def loop(self, fps):
    keys = py.key.get_pressed()
    if keys[py.K_d]:
      self.move_right(self.P_VELOCITY)
    elif keys[py.K_a]:
      self.move_left(self.P_VELOCITY)
    else:
      self.slow_down()

    self.y_vel += min (1, (self.gravity_count / fps ) * self.G_ACCELERATION)
    self.gravity_count += 1 

    self.move(self.x_vel, self.y_vel)
  
    

  def draw(self, window):
    self.sprite = self.SPRITES['idle_' + self.direction][0]
    window.blit(self.sprite, (self.rect.x, self.rect.y))
