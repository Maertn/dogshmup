import pygame as pg
import time

from settings import *
from player import Player
from enemies import Enemy
from waves import *

class Level():
    def __init__(self, dt):
        
        # import timestep and current_time
        self.dt = dt
        self.spawn_time = pg.time.get_ticks() * dt
        self.current_time = 0

        # get display
        self.display_surface = pg.display.get_surface()

        # setting up sprite groups
        self.visible_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.enemy_bullet_sprites = pg.sprite.Group()

        self.list_of_sprite_groups = [
            self.visible_sprites,
            self.enemy_sprites
        ]
        
        # setup wave spawning
        self.waves = []

        # spawn player
        self.spawn_player(self.dt)
   
    def update_timestep(self, dt):
        self.dt = dt

    def update_current_time(self, dt, spawn_time):
        self.current_time = (pg.time.get_ticks() * dt) - spawn_time

    def spawn_player(self, dt):
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2 + 300
        self.player = Player((x,y), dt, [self.visible_sprites])

    def spawn_wave(self, dt, dummy=[]):
        if dummy:
            pass
        else:
            wave = Wave1_1([self.visible_sprites, self.enemy_sprites, self.enemy_bullet_sprites], dt)
            self.waves.append(wave)
            dummy.append(0)
            
        for wave in self.waves:
            wave.run(dt)

    def run(self, dt):
        self.update_timestep(dt)
        self.update_current_time(dt, self.spawn_time)
        self.spawn_wave(dt)
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update(dt)
        print(self.enemy_bullet_sprites)