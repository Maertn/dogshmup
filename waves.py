import pygame as pg

from settings import *
from enemies import Enemy, PopcornBunny

class Wave:
    def __init__(self, groups, dt):
        self.dt = dt
        self.spawn_time = pg.time.get_ticks()
        self.current_time = 0
        self.groups = groups
    
    def update_timestep(self, dt):
        self.dt = dt

    def update_time(self, spawn_time):
        self.current_time = pg.time.get_ticks() - spawn_time
    
    def spawn_enemies(self, groups, current_time, dt, enemy_dummy=[]):
        if current_time >= 500 and (0 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE3, 0), 
                dt=dt, 
                groups=[groups[0], groups[1]],
                )
            enemy_dummy.append(0)
        
        if current_time >= 1500 and (1 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE1, 0), 
                dt=dt, 
                groups=[groups[0], groups[1]],
                )
            enemy_dummy.append(1)
        
        if current_time >= 3000 and (2 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE5, 0), 
                dt=dt, 
                groups=[groups[0], groups[1]],
                )
            enemy_dummy.append(2)
        
        if current_time >= 4500 and (3 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE2, 0), 
                dt=dt, 
                groups=[groups[0], groups[1]],
                )
            enemy_dummy.append(3)

        if current_time >= 6000 and (4 not in enemy_dummy):
            PopcornBunny(
                pos=(SPAWN_LANE4, 0), 
                dt=dt, 
                groups=[groups[0], groups[1]],
                )
            enemy_dummy.append(4)
        
        for enemy in groups[1]:
            enemy.ai(dt, groups)


    def run(self, dt):
        self.update_timestep(dt)
        self.update_time(self.spawn_time)
        self.spawn_enemies(self.groups, self.current_time, self.dt)
        print(self.groups[0].sprites()[0].position)