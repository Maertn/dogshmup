import pygame as pg
import time

from settings import *
from player import Player
from enemies import Enemy

class Level():
    def __init__(self, dt):
        
        # import timestep from main
        self.dt = dt
        
        # get display
        self.display_surface = pg.display.get_surface()

        # setting up sprite groups
        self.visible_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()

        self.list_of_sprite_groups = [
            self.visible_sprites,
            self.enemy_sprites
        ]
        
        # spawn player
        self.spawn_player(self.dt)

        # enemy spawning mechanics
        self.enemy_spawn_switch1 = True
        self.enemy_spawn_switch2 = True
        self.enemy_spawn_switch3 = True
        self.enemy_spawn_switch4 = True
        self.enemy_spawn_switch5 = True
    
    def update_timestep(self, dt):
        self.dt = dt

    def spawn_player(self, dt):
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2 + 300
        self.player = Player((x,y), dt, [self.visible_sprites])

    def enemies(self, dt):
        spawn_time = pg.time.get_ticks() / 1000
        if self.enemy_spawn_switch1 == True:
            enemy0=Enemy( 
                pos=(SPAWN_LANE1, 0), 
                dt=dt, 
                groups=[self.visible_sprites, self.enemy_sprites], 
                width=10, 
                height=10, 
                speed=50, 
                direction=[0,1], 
                spawn_time=spawn_time, 
                health=5,
                movement_switch1=True
                )
            self.enemy_spawn_switch1 = False
            
        if self.enemy_spawn_switch2 == True:
            enemy1=Enemy( 
                pos=(SPAWN_LANE2, 0), 
                dt=dt, 
                groups=[self.visible_sprites, self.enemy_sprites], 
                width=10, 
                height=10, 
                speed=50, 
                direction=[0,1], 
                spawn_time=spawn_time, 
                health=5,
                movement_switch1=True
                )
            self.enemy_spawn_switch2 = False

        if self.enemy_spawn_switch3 == True:
            enemy2=Enemy( 
                pos=(SPAWN_LANE3, 0), 
                dt=dt, 
                groups=[self.visible_sprites, self.enemy_sprites], 
                width=10, 
                height=10, 
                speed=50, 
                direction=[0,1], 
                spawn_time=spawn_time, 
                health=5,
                movement_switch1=True
                )
            self.enemy_spawn_switch3 = False

        if self.enemy_spawn_switch4 == True:
            enemy3=Enemy( 
                pos=(SPAWN_LANE4, 0), 
                dt=dt, 
                groups=[self.visible_sprites, self.enemy_sprites], 
                width=10, 
                height=10, 
                speed=50, 
                direction=[0,1], 
                spawn_time=spawn_time, 
                health=5,
                movement_switch1=True
                )
            self.enemy_spawn_switch4 = False

        if self.enemy_spawn_switch5 == True:
            enemy4=Enemy( 
                pos=(SPAWN_LANE5, 0), 
                dt=dt, 
                groups=[self.visible_sprites, self.enemy_sprites], 
                width=10, 
                height=10, 
                speed=50, 
                direction=[0,1], 
                spawn_time=spawn_time, 
                health=5,
                movement_switch1=True
                )
            self.enemy_spawn_switch5 = False

        for enemy in self.enemy_sprites:
            enemy.move(dt)

    
    def run(self, dt):
        self.update_timestep(dt)
        self.enemies(dt)
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update(dt)