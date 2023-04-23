import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, pos, dt, groups):
        # creating player sprite
        super().__init__(groups)
        self.image = pg.image.load('graphics/sprites/player/player_sprite.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(-60, -60)
        
        self.position = pos

        # grabbing timestep
        self.dt = dt

        # movement
        self.direction = pg.math.Vector2()
        self.speed = 400

    def update_timestep(self, dt):
        self.dt = dt

    def keylog(self):
        keys = pg.key.get_pressed()
      
        # movement over the y direction
        if keys[pg.K_UP] and self.position[1] >= 0:
            self.direction[1] = -1
        elif keys[pg.K_DOWN] and self.position[1] <= SCREEN_HEIGHT:
            self.direction[1] = 1
        else:
            self.direction[1] = 0

        # movement over the x direction
        if keys[pg.K_LEFT] and self.position[0] >= SCREEN_WIDTH - (GAME_WIDTH + BORDER_WIDTH):
            self.direction[0] = -1
        elif keys[pg.K_RIGHT] and self.position[0] <= GAME_WIDTH + BORDER_WIDTH:
            self.direction[0] = 1
        else:
            self.direction[0] = 0

    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        positionx = self.position[0]
        positionx += self.direction[0] * self.speed * dt
        positiony = self.position[1]
        positiony += self.direction[1] * self.speed * dt
        self.position = ((positionx, positiony))
        
        self.rect.centerx = round(self.position[0])
        self.rect.centery = round(self.position[1])

    def update(self, dt):
        self.update_timestep(dt)
        self.keylog()
        self.move(dt)