import pygame as pg

from settings import *
from enemies import Enemy, PopcornBunny

class Wave:
    def __init__(self, groups, dt):
        # time attr
        self.dt = dt
        self.spawn_time = pg.time.get_ticks() * dt
        self.current_time = 0
        
        # sprite group attr
        self.groups = groups
        self.enemy_sprites0 = pg.sprite.Group()
        self.enemy_sprites1 = pg.sprite.Group()
    
    def update_timestep(self, dt):
        self.dt = dt

    def update_time(self, dt, spawn_time):
        self.current_time = (pg.time.get_ticks() * dt) - spawn_time
    
    def spawn_enemies(self, groups, current_time, dt, enemy_dummy=[]):
        pass


    def run(self, dt):
        self.update_timestep(dt)
        self.update_time(dt, self.spawn_time)
        self.spawn_enemies(self.groups, self.current_time, self.dt)


class Wave1_1(Wave):
    def __init__(self, groups, dt):
        super().__init__(groups, dt)

        
    def spawn_enemies(self, groups, current_time, dt, enemy_dummy=[]):
        if current_time >= 5 and (0 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE3, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites0],
                movement_switch1 = True,
                movement_switch2 = True 
                )
            enemy_dummy.append(0)
        
        if current_time >= 15 and (1 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE1, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites0],
                movement_switch1 = True,
                movement_switch2 = True 
                )
            enemy_dummy.append(1)
        
        if current_time >= 30 and (2 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE5, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites0],
                movement_switch1 = True,
                movement_switch2 = True 
                )
            enemy_dummy.append(2)
        
        if current_time >= 45 and (3 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE2, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites0],
                movement_switch1 = True,
                movement_switch2 = True 
                )
            enemy_dummy.append(3)

        if current_time >= 60 and (4 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE4, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites0],
                movement_switch1 = True,
                movement_switch2 = True                
                )
            enemy_dummy.append(4)
        
        for enemy in self.enemy_sprites0:
            enemy.ai0(dt, groups, enemy.movement_switch1, enemy.movement_switch2)

        if current_time >= 100 and (5 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE2, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites1]                
                )
            enemy_dummy.append(5)

        if current_time >= 110 and (6 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE2, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites1],              
                )
            enemy_dummy.append(6)
        
        if current_time >= 120 and (7 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE2, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites1],
                movement_switch1 = True,
                movement_switch2 = True                
                )
            enemy_dummy.append(7)

        for enemy in self.enemy_sprites1:
            enemy.ai1(dt, groups)
