import pygame as pg
import math
from settings import *

# player bullets

class Bullet(pg.sprite.Sprite):
    def __init__(self, dt, pos, groups, speed, direction: pg.math.Vector2):
        super().__init__(groups)
        self.image = pg.Surface((8, 8)).convert_alpha()
        self.color = 'white'
        self.rect = self.image.get_rect(center=pos)   
        
        # time attributes
        self.dt = dt
        self.spawn_time = pg.time.get_ticks() * dt
        self.current_time_dummy = []
        self.current_time = 0
        
        # movement attributes
        self.direction = direction
        self.speed = speed
        self.pos = [self.rect.centerx, self.rect.centery]
        
        # attributes for move_path()
        self.path = None
        self.path_index = 0
                        
        # sprite groups
        self.groups = groups
        
        # time attributes
        self.dt = dt
        self.spawn_time = pg.time.get_ticks() * dt
        self.current_time_dummy = []
        self.current_time = 0
    
    def update_timestep(self, dt):
        self.dt = dt
    
    def update_current_time(self):
        self.current_time_dummy.append(self.dt)
        self.current_time = sum(self.current_time_dummy)

    # Linear movement of bullets
    def move(self, dt):
        self.direction = pg.math.Vector2(self.direction)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.pos[0] += self.direction[0] * self.speed * dt
        self.pos[1] += self.direction[1] * self.speed * dt
        self.rect.centerx = round(self.pos[0])
        self.rect.centery = round(self.pos[1])
        
    # Movement along path
    def move_path(self, dt):
        """Moves along a path. Loading path into bullet attributes is required."""
        if self.path != None:
            path_dict = self.path.create_dict()
            self.pos = path_dict[self.path_index]
            self.rect.centerx = round(self.pos[0])
            self.rect.centery = round(self.pos[1])
            self.path_index += 1
            if self.path_index >= len(path_dict):
                self.pos = [self.rect.centerx, self.rect.centery]
                self.path = None
                return 'Done'
            
            # Giving direction for animation
            destination = path_dict[self.path_index]
            directionx = (destination[0] - self.pos[0]) / math.sqrt(math.pow(destination[0] - self.pos[0], 2) + math.pow(destination[1] - self.pos[1], 2))
            directiony = (destination[1] - self.pos[1]) / math.sqrt(math.pow(destination[0] - self.pos[0], 2) + math.pow(destination[1] - self.pos[1], 2))
            self.direction = pg.math.Vector2(directionx, directiony)
        else:
            self.pos = [self.rect.center[0], self.rect.center[1]]
            return 'Done'

    # Used in ShotsFired to aim at a position.
    def aim_bullet(self, destination):
        distance = math.sqrt(pow((self.pos[0] - destination[0]), 2) + pow((self.pos[1] - destination[1]), 2))
        directionx = (destination[0] - self.pos[0])/distance
        directiony = (destination[1] - self.pos[1])/distance
        self.direction = pg.math.Vector2(directionx, directiony)
    
    def remove_bullet(self):
        if self.rect.centery <= -50 or self.rect.centery >= SCREEN_HEIGHT + 50 or self.rect.centerx <=BORDER_WIDTH - 50 or self.rect.centerx >= BORDER_WIDTH + GAME_WIDTH + 50:
            self.kill()

    # Abstracted colouring of bullet
    def color_bullet(self):
        self.image = pg.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)
    
    def update(self, dt):
        self.update_timestep(dt)
        self.update_current_time()
        self.remove_bullet()
        self.color_bullet()
        if self.path == None:
            self.move(dt)


class EnemyBullet(Bullet):
    def __init__(self, dt, pos, groups, speed, direction, type):
        super().__init__(dt, pos, groups, speed, direction)
        self.image = pg.image.load(f'graphics\sprites\enemy_bullets\{type}\enemy_bullet_sprite_0.png').convert_alpha()
        # self.rect = self.image.get_rect(center = pos)
        self.color = 'white'
        self.speed = speed
        self.direction = pg.math.Vector2(direction)
        self.dt = dt
        self.initial_position = pos
        
        # animation attributes
        self.animations = []
        self.frame_index = 0
        self.animation_speed = 0.1
        self.type = type
        self.sprite = self.select_sprite()
        
    def select_sprite(self):
        if self.type == 'type1':
            self.animations = [
                pg.image.load('graphics\sprites\enemy_bullets\\type1\enemy_bullet_sprite_0.png').convert_alpha(),
                pg.image.load('graphics\sprites\enemy_bullets\\type1\enemy_bullet_sprite_1.png').convert_alpha(),
                pg.image.load('graphics\sprites\enemy_bullets\\type1\enemy_bullet_sprite_2.png').convert_alpha(),
                pg.image.load('graphics\sprites\enemy_bullets\\type1\enemy_bullet_sprite_3.png').convert_alpha()
            ]
            
        if self.type == 'type2':
            self.animations = [
                pg.image.load('graphics\sprites\enemy_bullets\\type2\enemy_bullet_sprite_0.png').convert_alpha()
            ] 
            
    def animate_sprite(self):
        animation = self.animations	
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.pos)
        self.rect = self.rect.inflate((-10, -10))
        self.image = pg.transform.rotate(self.image, math.degrees(math.atan2(self.direction[0], self.direction[1])))

    def update(self, dt):
        self.update_timestep(dt)
        self.update_current_time()
        self.animate_sprite()
        self.remove_bullet()
        # self.color_bullet()
        if self.path == None:
            self.move(dt)
        

# multi-shot
class ShotsFired:
    def __init__(self, dt, pos, groups, speed, direction, number_of_bullets: int, spread: float, type: str):
        self.pos = pos
        self.groups = groups
        self.direction = direction
        self.speed = speed
        self.list_of_bullets = list(range(1, number_of_bullets + 1))
        self.shot_switch = True
        self.dt = dt
        self.type = type
        
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

    def update_timestep(self, dt):
        self.dt = dt

    # execute spawning of bullets as recorded in bullet_dict
    def shoot(self, dt):
        if self.shot_switch:
            for bullet in self.bullet_dict.items():
                direction = bullet[1]
                direction = pg.math.Vector2(direction).normalize()
                EnemyBullet(dt, self.pos, self.groups, self.speed, direction, self.type)
            self.shot_switch = False

    def update(self, dt):
        self.update_timestep(dt)
        self.shoot(dt)
