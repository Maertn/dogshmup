import pygame as pg
import math
from settings import *

# player bullets

class Bullet(pg.sprite.Sprite):
    def __init__(self, dt, spawn_time, pos, groups, speed, direction: pg.math.Vector2):
        super().__init__(groups)
        self.image = pg.Surface((8, 8)).convert_alpha()
        self.color = 'white'
        self.rect = self.image.get_rect(center = pos)   
        self.direction = direction
        self.speed = speed
        self.pos = pg.math.Vector2(self.rect.center)
        
        # time attributes
        self.dt = dt
        self.spawn_time = spawn_time
        self.current_time = 0

    def update_timestep(self, dt):
        self.dt = dt

    def update_current_time(self):
        self.current_time = pg.time.get_ticks() - self.spawn_time

    def trajectory(self, dt):
        self.direction = pg.math.Vector2(self.direction)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.centerx += self.direction[0] * self.speed * dt
        self.rect.centery += self.direction[1] * self.speed * dt

    def remove_bullet(self):
        if self.rect.centery <= 0 or self.rect.centery >= SCREEN_HEIGHT or self.rect.centerx <=BORDER_WIDTH or self.rect.centerx >= BORDER_WIDTH + GAME_WIDTH:
            self.kill()

    def color_bullet(self):
        self.image.fill(self.color)

    def update(self, dt):
        self.update_timestep(dt)
        self.update_current_time()
        self.trajectory(dt)
        self.remove_bullet()
        self.color_bullet()


class EnemyBullet(Bullet):
    def __init__(self, pos, groups, speed, direction):
        super().__init__(pos, groups, speed, direction)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.direction = direction
        

    def trajectory(self, dt):
        self.pos.x += self.direction[0] * self.speed * dt
        self.pos.y += self.direction[1] * self.speed * dt
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)

    def update(self, dt):
        self.trajectory(dt)
        self.remove_bullet()
        

# multi-shot
class ShotsFired:
    def __init__(self, pos, groups, speed, direction, number_of_bullets: int, spread: float):
        self.pos = pos
        self.groups = groups
        self.direction = direction
        self.speed = speed
        self.list_of_bullets = list(range(1, number_of_bullets + 1))
        self.shot_switch = True
        
        # creating spread over unit circle
        self.spread = math.pi*2*(spread)
        self.angle = 0
        if number_of_bullets > 1:
            self.angle = self.spread / number_of_bullets
        
        # create a dict for holding information of bullet spawns
        self.bullet_dict = {}
        
        # if the number of bullets is odd, bullet1.direction = self.direction.
        if number_of_bullets % 2 == 1: 
            for bullet in self.list_of_bullets:
                if bullet > 1:
                    rotation_index = divmod(bullet,2)
                    k = rotation_index[0]
                    if rotation_index[1] == 0: 
                        direction = pg.math.Vector2(self.direction)
                        direction = direction.rotate_rad(k * self.angle)
                        direction = (direction[0], direction[1])
                        self.bullet_dict[bullet] = direction
                    else:
                        direction = pg.math.Vector2(self.direction)
                        direction = direction.rotate_rad(k * -self.angle)
                        direction = (direction[0], direction[1])
                        self.bullet_dict[bullet] = direction
                else: 
                    direction = self.direction
                    self.bullet_dict[bullet] = direction
        
        # if the number of bullets is even, bullet1.direction = self.direction + (angle / 2 ).
        if number_of_bullets % 2 == 0: 
            for bullet in self.list_of_bullets:
                rotation_index = divmod(bullet,2)
                k = rotation_index[0]
                if rotation_index[1] == 0: 
                    direction = pg.math.Vector2(self.direction)
                    direction = direction.rotate_rad((k * self.angle) - (self.angle / 2))
                    direction = (direction[0], direction[1])
                    self.bullet_dict[bullet] = direction
                else:
                    direction = pg.math.Vector2(self.direction)
                    direction = direction.rotate_rad((k * -self.angle) - (self.angle / 2))
                    direction = (direction[0], direction[1])
                    self.bullet_dict[bullet] = direction   

    # execute spawning of bullets as recorded in bullet_dict
    def shoot(self):
        if self.shot_switch:
            for bullet in self.bullet_dict.items():
                direction = bullet[1]
                print(direction)
                direction = pg.math.Vector2(direction).normalize()
                EnemyBullet(self.pos, self.groups, self.speed, direction)
            self.shot_switch = False 

    def update(self):
        self.shoot()
