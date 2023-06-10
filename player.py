import pygame as py
import basics


class Player(py.sprite.Sprite):
  COLOR = (255,0,0)
  P_VELOCITY = 5
  PD_VELOCITY = 16
  G_ACCELERATION = 1
  SPRITES = basics.load_sprite_sheets("MainCharacters","PinkMan",32,32,True)
  ANIMATION_DELAY = 5

  def __init__(self, x,y,width,height):
    super().__init__()
    self.rect = py.Rect(x,y,width,height)
    self.x_vel = 0
    self.y_vel = 0
    self.image = self.SPRITES
    self.surface = self.image
    self.mask = None
    self.direction = "right"
    self.animation_count = 0
    self.gravity_count = 0
    self.jump_count = 0
    self.sprite = self.SPRITES['idle_' + self.direction][0]

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
    
  def jump(self):
    if (self.jump_count != 0):
      self.fall_count = 0
      return 
    self.y_vel = -self.G_ACCELERATION * 16
    self.animation_count = 0
    self.jump_count += 1


  def loop(self, fps, collide_left, collide_right):
    keys = py.key.get_pressed()
    if keys[py.K_d] and not collide_right:
      self.move_right(self.P_VELOCITY)
    elif keys[py.K_a] and not collide_left:
      self.move_left(self.P_VELOCITY)
    else:
      self.slow_down()

    if keys[py.K_SPACE]:
      self.jump()

    self.y_vel += min (1, (self.gravity_count / fps ) * self.G_ACCELERATION)
    self.gravity_count += 1 
    self.update_sprite()

    self.move(self.x_vel, self.y_vel)

  def update_sprite(self):
    sprite_sheet = "idle"
    if (self.x_vel != 0):
      sprite_sheet = "run"
    elif self.y_vel < 0:
      if self.jump_count == 1:
        sprite_sheet = "jump"
    elif self.y_vel > 1:
      sprite_sheet = "fall"
    sprite_sheet_name = sprite_sheet + "_" + self.direction

    sprites = self.SPRITES[sprite_sheet_name]
    sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
    self.sprite = sprites[sprite_index]
    self.animation_count += 1
    self.update()


  def update(self):
    self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
    self.mask = py.mask.from_surface(self.sprite)

  def landed(self):
    self.gravity_count = 0
    self.y_vel = 0
    self.jump_count = 0

  def hit_head(self):
    self.y_vel *= -1


  def draw(self, window):
    window.blit(self.sprite, (self.rect.x, self.rect.y))

