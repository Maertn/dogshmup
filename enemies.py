import pygame as pg
import math

from settings import *
from bullets import ShotsFired

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
        self.spawn_time = pg.time.get_ticks() * dt
        self.current_time = 0

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

    def update_current_time(self, dt, spawn_time):
        self.current_time = (pg.time.get_ticks() * dt) - spawn_time 

    def move(self, dt):
        direction = pg.math.Vector2(self.direction).normalize()
        self.pos[0] += direction[0] * self.speed * dt
        self.pos[1] += direction[1] * self.speed * dt
        self.rect.centerx = round(self.pos[0])
        self.rect.centery = round(self.pos[1])

    def move_to(self, dt, destination, speed):
        distance = math.sqrt(pow((self.pos[0] - destination[0]),2) + pow((self.pos[1] - destination[1]),2))
        if distance != 0:
            self.direction = pg.math.Vector2(((destination[0] - self.rect.centerx)/distance), ((destination[1] - self.rect.centery)/distance))
            if not (self.direction[0] == 0 or self.direction[1] == 1): 
                self.direction = self.direction.normalize()
        else:
            pass

        if self.rect.centerx - destination[0] <= 0:
            if self.rect.centery - destination[1] <= 0:
                if not (self.rect.centerx >= destination[0] and self.rect.centery >= destination[1]):
                    self.pos[0] += self.direction[0] * speed * dt
                    self.pos[1] += self.direction[1] * speed * dt
                    self.rect.center = round(self.pos[0]), round(self.pos[1])
            
            else:
                if not (self.pos[0] >= destination[0] and self.pos[1] <= destination[1]):
                    self.pos[0] += self.direction[0] * speed * dt
                    self.pos[1] += self.direction[1] * speed * dt
                    self.rect.center = round(self.pos[0]), round(self.pos[1])
                    print('ok')
        
        else:
            if self.rect.centery - destination[1] <= 0:
                if not (self.pos[0] <= destination[0] and self.pos[1] >= destination[1]):
                    self.pos[0] += self.direction[0] * speed * dt
                    self.pos[1] += self.direction[1] * speed * dt
                    self.rect.center = round(self.pos[0]), round(self.pos[1])

            else:
                if not (self.pos[0] <= destination[0] and self.pos[1] <= destination[1]):
                    self.pos[0] += self.direction[0] * speed * dt
                    self.pos[1] += self.direction[1] * speed * dt
                    self.rect.center = round(self.pos[0]), round(self.pos[1])
                    print('yes')

    def kill_at_border(self):
        A = (self.rect.top >= SCREEN_HEIGHT)
        B = (self.rect.bottom <= 0)
        C = (self.rect.left >= GAME_WIDTH + BORDER_WIDTH)
        D = (self.rect.right <= BORDER_WIDTH)
        
        if A or B or C or D: self.kill()

    def ai(self, dt, groups):
        pass

    def aim_bullet(self, destination):
        distance = math.sqrt(pow((self.pos[0] - destination[0]), 2) + pow((self.pos[1] - destination[1]), 2))
        directionx = (destination[0] - self.pos[0])/distance
        directiony = (destination[1] - self.pos[1])/distance
        direction = pg.math.Vector2(directionx, directiony)
        return direction

    def create_cooldown(self, dt, call_time, cooldown):
        # print(self.current_time - call_time)
        if self.current_time - call_time >= cooldown * dt:
            return True

    def update(self, dt):
        self.update_current_time(dt, self.spawn_time)
        self.update_timestep(dt)
        self.kill_at_border()
    
class PopcornBunny(Enemy):
    def __init__(
        self, 
        pos: tuple, 
        dt: float, 
        groups: pg.sprite.Group, 
        **movement_switch):
        super().__init__(
                pos,
                dt,
                groups,
                width =10,
                height=10,
                speed=50,
                direction=(0,1),
                health=5,
                **movement_switch)
        
        # spawn dummies
        self.shot_dict = []
        self.bullet_dummy = []
        self.bullet_spawn = []

        self.movement_dict = []

    def ai_test(self, dt, groups):
        """This AI accelerates into the screen untill 1/4th. 
        After 1/4th it scrolls downwards, while slowly moving towards the player untill the y position is greater than the player.
        Between 1/4 and 2/3rd of the screen it shoots bursts of three aimed at the player.
        After 2/3rd of the screen it shoots single shots aimed at the player."""
        
        destination = (self.rect.centerx, round(SCREEN_HEIGHT * (1/4)))
        player_position = groups[0].sprites()[0].position

        # movement
        if self.pos[1] <= destination[1] - (self.speed * dt):
            speed = 200 - (dt * self.current_time * 3)
            self.move_to(dt, destination, speed)
        else:
            self.direction = (0,1)
            self.move(dt)
            if player_position[1] >= self.pos[1]:
                self.move_to(dt, player_position, 10)

        # bullets
        if self.pos[1] >= destination[1] - (self.speed * dt) and (0 not in self.bullet_dummy) and self.pos[1] <= SCREEN_HEIGHT*(2/3):
            shot = ShotsFired(
                dt = self.dt,
                pos = (self.rect.centerx, self.rect.bottom),
                groups = [groups[0], groups[2]],
                speed = 200,
                direction = self.aim_bullet(player_position),
                number_of_bullets = 3,
                spread = 1/10
                )
            self.shot_dict.append(shot)
            self.bullet_spawn.append(self.current_time)
            self.bullet_dummy.append(0)

        if self.pos[1] >= SCREEN_HEIGHT * (2/3) and (0 not in self.bullet_dummy):
            shot = ShotsFired(
                dt = self.dt,
                pos = (self.rect.centerx, self.rect.bottom),
                groups = [groups[0], groups[2]],
                speed = 200,
                direction = self.aim_bullet(player_position),
                number_of_bullets = 1,
                spread = 1/10
                )
            self.shot_dict.append(shot)
            self.bullet_spawn.append(self.current_time)
            self.bullet_dummy.append(0)

        if 0 in self.bullet_dummy:
            cooldown =  self.create_cooldown(self.dt, self.bullet_spawn[0], 2000)
            if cooldown:
                self.bullet_spawn.pop()
                self.bullet_dummy = []

        for shot in self.shot_dict:
            shot.update(self.dt)

    def ai0(self, dt, groups, movement_switch1, movement_switch2):
        """Requires two movement switches.
        This AI moves the enemy downwards, slightly towards the player.
        It hovers at 1/2 of the screen, and runs off after a short period towards the upper edge of the screen.
        After it reaches 1/3 of the screen, it starts shooting single shots aimed at the player."""

        destination = (self.pos[0], SCREEN_HEIGHT * (1/2))
        player_position = groups[0].sprites()[0].position

        # movement
        if self.pos[1] <= destination[1] and self.movement_switch1 == True:
            self.move_to(dt, destination, 100)
            if self.pos[1] + (self.direction[1] * self.speed * dt) >= destination[1] - (self.direction[1] * self.speed * dt):
                self.movement_dict.append(self.current_time)
                self.movement_switch1 = False
        elif self.movement_switch1 == False and self.movement_switch2 == True:
            cooldown = self.create_cooldown(self.dt, self.movement_dict[0], 1500)
            if cooldown:
                self.movement_switch2 = False
        elif self.movement_switch1 == False and self.movement_switch2 == False:
            self.move_to(dt, (self.pos[0], -100), 100)

        self.move_to(dt, player_position, 20)

        # bullets
        if self.pos[1] >= SCREEN_HEIGHT * (1/3) and (0 not in self.bullet_dummy):
            self.bullet_dummy.append(0)
        
        if (0 in self.bullet_dummy) and (1 not in self.bullet_dummy):
            shot = ShotsFired(
                dt = self.dt,
                pos = (self.rect.centerx, self.rect.bottom),
                groups = [groups[0], groups[2]],
                speed = 200,
                direction = self.aim_bullet(player_position),
                number_of_bullets = 1,
                spread = 1/10
                )
            self.shot_dict.append(shot)
            self.bullet_spawn.append(self.current_time)
            self.bullet_dummy.append(1)

        if 1 in self.bullet_dummy:
            cooldown =  self.create_cooldown(self.dt, self.bullet_spawn[0], 2000)
            if cooldown:
                self.bullet_spawn.pop()
                self.bullet_dummy.pop()

        for shot in self.shot_dict:
            shot.update(self.dt)
            print(self.bullet_dummy)
            