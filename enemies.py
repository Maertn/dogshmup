import pygame as pg
import math

from settings import *

class Enemy(pg.sprite.Sprite):
    """Class that spawns an enemy. 
    Sprite group should be visible_sprites and enemy_sprites. 
    Custom groups are possible. 
    Width and height are size of hitboxes.
    Movement switches are to be added manually with try-except blocks if more are needed."""
    def __init__(
                self, 
                pos: tuple, 
                dt: float, 
                groups: pg.sprite.Group, 
                width: int, 
                height: int, 
                speed: int, 
                direction: tuple, 
                spawn_time: float, 
                health: int, 
                **movement_switch):
        super().__init__(groups)

        # creating a hitbox
        self.image = pg.Surface((width, height)).convert_alpha()
        self.image.fill('red')
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect
        self.health = health

        # grabbing initial timestep and spawn time
        self.dt = dt
        self.spawn_time = spawn_time

        # creating motion attributes
        self.speed = speed
        self.direction = direction
        self.pos = [self.hitbox.centerx, self.hitbox.centery]

        # creating motion switches
        try:
            self.movement_switch1 = movement_switch["movement_switch1"]
        except:
            pass
        try:
            self.movement_switch2 = movement_switch["movement_switch2"]
        except:
            pass
        try:
            self.movement_switch3 = movement_switch["movement_switch3"]
        except:
            pass
        try:
            self.movement_switch4 = movement_switch["movement_switch4"]
        except:
            pass
        try:
            self.movement_switch5 = movement_switch["movement_switch5"]
        except:
            pass
    
    def update_timestep(self, dt):
        self.dt = dt

    def move(self, dt):
        direction = pg.math.Vector2(self.direction).normalize()
        self.pos[0] += direction[0] * self.speed * dt
        self.pos[1] += direction[1] * self.speed * dt
        self.rect.centerx = round(self.pos[0])
        self.rect.centery = round(self.pos[1])

    def move_to(self, dt, destination, speed):
        distance = math.sqrt(pow((self.rect.centerx - destination[0]),2) + pow((self.rect.centery - destination[1]),2))
        if distance != 0:
            direction = pg.math.Vector2(((destination[0] - self.rect.centerx)/distance), ((destination[1] - self.rect.centery)/distance))
            self.direction = direction.normalize()
        else:
            pass

        if self.rect.centerx - destination[0] <= 0:
            if self.rect.centery - destination[1] <= 0:
                x0 = self.rect.centerx + (self.direction[0] * speed * dt) 
                x1 = (destination[0] + 1) or (destination[0] - 1)
                y0 = self.rect.centery + (self.direction[1] * speed * dt)
                y1 = (destination[1] + 1) or (destination[1]-1)
                
                if not (self.rect.centerx >= destination[0] and self.rect.centery >= destination[1]):
                    self.pos[0] += self.direction[0] * speed * dt
                    self.pos[1] += self.direction[1] * speed * dt
                    self.rect.center = round(self.pos[0]), round(self.pos[1])
                    if x0 > x1 or y0 > y1:
                        self.rect.center = destination
            
            else:
                if not (self.rect.centerx >= destination[0] or self.rect.centery <= destination[1]):
                    self.pos[0] += self.direction[0] * speed * dt
                    self.pos[1] += self.direction[1] * speed * dt
                    self.rect.center = round(self.pos[0]), round(self.pos[1])
                else:
                    self.rect.center = destination
        
        else:
            if self.rect.centery - destination[1] <= 0:
                if not (self.pos.x <= destination[0] and self.pos.y >= destination[1]):
                    self.pos[0] += self.direction[0] * speed * dt
                    self.pos[1] += self.direction[1] * speed * dt
                    self.rect.center = round(self.pos[0]), round(self.pos[1])
                else:
                    self.rect.center = destination

            else:
                if not (self.pos.x <= destination[0] and self.pos.y <= destination[1]):
                    self.pos[0] += self.direction[0] * speed * dt
                    self.pos[1] += self.direction[1] * speed * dt
                    self.rect.center = round(self.pos[0]), round(self.pos[1])
                else:
                    self.rect.center = destination

    def kill_at_border(self):
        A = (self.rect.top >= SCREEN_HEIGHT)
        B = (self.rect.bottom <= 0)
        C = (self.rect.left >= GAME_WIDTH + BORDER_WIDTH)
        D = (self.rect.right <= BORDER_WIDTH)
        
        if A or B or C or D: self.kill()

    def update(self, dt):
        self.update_timestep(dt)
        self.kill_at_border()

        