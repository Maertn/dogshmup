import pygame as pg
import math

from settings import *
from enemies import Enemy, PopcornBird
from bullets import EnemyBullet
from path import CircularPath


class Wave:
    def __init__(self, groups, dt):
        # time attr
        self.dt = dt
        self.current_time_dummy = []
        self.current_time = 0
        
        # sprite group attr
        self.groups = groups
        self.enemy_sprites0 = pg.sprite.Group()
        self.enemy_sprites1 = pg.sprite.Group()
    
    def update_timestep(self, dt):
        self.dt = dt
        # print(self.dt)

    def update_current_time(self):
        self.current_time_dummy.append(self.dt)
        self.current_time = sum(self.current_time_dummy)
    
    def spawn_enemies(self, groups, current_time, dt, enemy_dummy=[]):
        pass


    def run(self, dt):
        self.update_timestep(dt)
        self.update_current_time()
        self.spawn_enemies(self.groups, self.current_time, self.dt)

class TestWavePolar(Wave):
    """Made for testing polar movements"""
    def __init__(self, groups, dt):
        super().__init__(groups, dt)
      
    def spawn_enemies(self, groups, current_time, dt, enemy_dummy =[]):
        if 0 not in enemy_dummy:
            EnemyBullet(
                dt=dt,
                pos= [(SCREEN_WIDTH / 2) + 100, SCREEN_HEIGHT / 2],
                groups=[groups[1], groups[3]],
                speed=250,
                direction=(0,1),
                type='type1'
            )
            
            EnemyBullet(
                dt=dt,
                pos= [(SCREEN_WIDTH / 2) - 100, SCREEN_HEIGHT / 2],
                groups=[groups[1], groups[4]],
                speed=250,
                direction=(0,1),
                type='type1'
            )
            enemy_dummy.append(0)

        for bullet in groups[3]:
            if 1 not in enemy_dummy:
                bullet.path = CircularPath(
                    dt = dt,
                    position = bullet.pos,
                    radius = 200,
                    angle_in_radians = -5 * math.pi,
                    velocity = bullet.speed * 15 * (5/4),
                    phase = 0
                    )
                enemy_dummy.append(1)
            if bullet.path:
                bullet.move_path(dt)
            else: continue                

        for bullet in groups[4]:
            if 2 not in enemy_dummy:
                bullet.path = CircularPath(
                    dt = dt,
                    position = bullet.pos,
                    radius = 200,
                    angle_in_radians = 5 * math.pi,
                    velocity = bullet.speed * 15 * (5/4),
                    phase = math.pi
                    )
                enemy_dummy.append(2)
            if bullet.path:
                bullet.move_path(dt)
            else: continue

class TestWavePolar1(Wave):
    """Made for testing polar movements"""
    def __init__(self, groups, dt):
        super().__init__(groups, dt)
            
    def spawn_enemies(self, groups, current_time, dt, enemy_dummy =[]):
        if 0 not in enemy_dummy:
            EnemyBullet(
                dt=dt,
                pos= [(SCREEN_WIDTH / 2), SCREEN_HEIGHT / 2],
                groups=[groups[1], groups[3]],
                speed=150,
                direction=(0,1),
                type='type1'
            )
            # bullet_dict = bullet.polar_move(100, math.pi, 50)
            # print(bullet_dict)
            # for step in bullet_dict.items():
            #     EnemyBullet(
            #     dt=dt,
            #     pos= step[1][1],
            #     groups=[groups[1], groups[3]],
            #     speed=0,
            #     direction=(0,1),
            #     type='type1'
            #     )
            enemy_dummy.append(0)
        
        for bullet in groups[3]:
            bullet.polar_move(100, (1/12)*math.pi, 10)
               
class Wave1_1(Wave):
    def __init__(self, groups, dt):
        super().__init__(groups, dt)

        
    def spawn_enemies(self, groups, current_time, dt, enemy_dummy=[]):
        if current_time >= 1 and (0 not in enemy_dummy):
            PopcornBird(
                pos=(SPAWN_LANE3, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites0],
                movement_switch1 = True,
                movement_switch2 = True 
                )
            enemy_dummy.append(0)
            # print('1', current_time, self.current_time)
        
        if current_time >= 2 and (1 not in enemy_dummy):
            PopcornBird(
                pos=(SPAWN_LANE1, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites0],
                movement_switch1 = True,
                movement_switch2 = True 
                )
            enemy_dummy.append(1)
            # print('2', current_time, self.current_time)
        
        if current_time >= 3 and (2 not in enemy_dummy):
            PopcornBird(
                pos=(SPAWN_LANE5, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites0],
                movement_switch1 = True,
                movement_switch2 = True 
                )
            enemy_dummy.append(2)
            # print('3', current_time, self.current_time)
        
        if current_time >= 4 and (3 not in enemy_dummy):
            PopcornBird(
                pos=(SPAWN_LANE2, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites0],
                movement_switch1 = True,
                movement_switch2 = True 
                )
            enemy_dummy.append(3)
            # print('4', current_time, self.current_time)

        if current_time >= 5 and (4 not in enemy_dummy):
            PopcornBird(
                pos=(SPAWN_LANE4, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites0],
                movement_switch1 = True,
                movement_switch2 = True                
                )
            enemy_dummy.append(4)
            # print('5', current_time, self.current_time)
        
        for enemy in self.enemy_sprites0:
            enemy.ai0(dt, groups, enemy.movement_switch1, enemy.movement_switch2)

        if current_time >= 6.5 and (5 not in enemy_dummy):
            PopcornBird(
                pos=(SPAWN_LANE2, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites1]                
                )
            enemy_dummy.append(5)

        if current_time >= 6.75 and (6 not in enemy_dummy):
            PopcornBird(
                pos=(SPAWN_LANE2, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites1],              
                )
            enemy_dummy.append(6)
        
        if current_time >= 7 and (7 not in enemy_dummy):
            PopcornBird(
                pos=(SPAWN_LANE2, 0), 
                dt=dt, 
                groups=[groups[0], groups[1], self.enemy_sprites1],
                movement_switch1 = True,
                movement_switch2 = True                
                )
            enemy_dummy.append(7)

        for enemy in self.enemy_sprites1:
            enemy.ai1(dt, groups)
