import pygame as pg
import time

from settings import *
from player import Player, PlayerSprite
from enemies import Enemy
from waves import *

class Level():
    def __init__(self, dt):
        
        # import timestep and current_time
        self.dt = dt
        self.spawn_time = pg.time.get_ticks() * dt
        self.current_time_dummy = []
        self.current_time = 0

        # get display
        self.display_surface = pg.display.get_surface()

        # setting up sprite groups
        self.player_hitbox_sprite = pg.sprite.Group()
        self.visible_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.enemy_bullet_sprites = pg.sprite.Group()
        self.enemy_bullet_sprites1 = pg.sprite.Group()

        self.list_of_sprite_groups = [
            self.player_hitbox_sprite,
            self.visible_sprites,
            self.enemy_sprites,
            self.enemy_bullet_sprites,
            self.enemy_bullet_sprites1
        ]
        
        # setup wave spawning
        self.waves = []

        # spawn player
        self.spawn_player(self.dt)
    
    def update_timestep(self, dt):
        self.dt = dt

    def update_current_time(self):
        self.current_time_dummy.append(self.dt)
        self.current_time = sum(self.current_time_dummy)

    def spawn_player(self, dt):
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2 + 300
        self.player = Player((x,y), dt, [self.player_hitbox_sprite])
        self.player_sprite = PlayerSprite((x,y), [self.visible_sprites])

    def spawn_wave(self, dt, dummy=[]):
        if dummy:
            pass
        else:
            # wave_test = TestWavePolar([self.player_hitbox_sprite, self.visible_sprites, self.enemy_sprites, self.enemy_bullet_sprites, self.enemy_bullet_sprites1], dt)
            # wave_test1 = TestWavePolar1([self.player_hitbox_sprite, self.visible_sprites, self.enemy_sprites, self.enemy_bullet_sprites, self.enemy_bullet_sprites1], dt)
            wave1 = Wave1_1([self.player_hitbox_sprite, self.visible_sprites, self.enemy_sprites, self.enemy_bullet_sprites], dt)
            # self.waves.append(wave_test)
            # self.waves.append(wave_test1)
            self.waves.append(wave1)
            dummy.append(0)
            
        for wave in self.waves:
            wave.run(dt)

    def run(self, dt):
        self.update_timestep(dt)
        self.update_current_time()
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update(self.dt)
        self.player_sprite.update_sprite(self.player.position)
        self.player_hitbox_sprite.draw(self.display_surface)
        self.player_hitbox_sprite.update(self.dt)
        self.spawn_wave(self.dt)