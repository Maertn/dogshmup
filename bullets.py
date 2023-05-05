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
        
        # movement attributes
        self.direction = direction
        self.speed = speed
        self.pos = [self.rect.centerx, self.rect.centery]
        
        # attributes for move_path()
        self.path = None
        self.path_index = 0
        
        # attributes for polar_move() and polar_move_delta(), also angular_move() 
        self.start_pos_dummy = [pos[0],pos[1]]
        self.current_pos_dummy = [pos[0],pos[1]]
        self.current_pos_dummy1 = [pos[0],pos[1]]
        self.current_direction_dummy = [self.direction[0], self.direction[1]]
        self.movement_dummy = []
        self.polar_move_path_index = 0
        self.polar = False
        self.theta = 0
        self.check_dummy = 0
                
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
        
    # Linear movement through polar coordinates
    def polar_move_delta(self, delta_r, delta_theta, initial_position_dummy = []):
        """This method takes a polar coordinate and takes the shortest path towards that coordinate.
        This method came about when attempting to code motion on a polar plane."""
        if 0 not in initial_position_dummy:
            self.current_pos_dummy = (self.pos[0], self.pos[1])
            initial_position_dummy.append(0)
        print(self.current_pos_dummy, initial_position_dummy)
        displacement_x = delta_r * math.cos(delta_theta)
        displacement_y = delta_r * math.sin(delta_theta)
        total_displacement = math.hypot(displacement_x, displacement_y)
        destination = (self.current_pos_dummy[0] + displacement_x, self.current_pos_dummy[1] + displacement_y)
        print(destination)
        self.direction = pg.math.Vector2(math.cos(delta_theta), math.sin(delta_theta)).normalize()
        
        if destination[0] >= self.pos[0]:    
            check_for_x = self.pos[0] + (self.direction[0] * self.speed * self.dt) >= destination[0] - (self.direction[0] * self.speed * self.dt)
        else:
            check_for_x = self.pos[0] + (self.direction[0] * self.speed * self.dt) <= destination[0] - (self.direction[0] * self.speed * self.dt)
        
        if destination[1] >= self.pos[1]:
            check_for_y = self.pos[1] + (self.direction[1] * self.speed * self.dt) >= destination[1] - (self.direction[1] * self.speed * self.dt)
        else:
            check_for_y = self.pos[1] + (self.direction[1] * self.speed * self.dt) <= destination[1] - (self.direction[1] * self.speed * self.dt)
        
        if check_for_x and check_for_y:
            return 'Next'
            
    def polar_move(self, radius, angle_in_radians, resolution, initial_position_dummy=[]):
        """Curved movement towards the specified polar coordinates with respect to position when called."""
        # get position of call
        self.polar = True
        
        if 0 not in initial_position_dummy:
            self.current_pos_dummy1 = (self.pos[0], self.pos[1])
            initial_position_dummy.append(0)
        if 1 not in initial_position_dummy:
            self.current_direction_dummy = (self.direction[0], self.direction[1])
        
        # ratio of radial to angular displacement
        initial_angle = 0
        radial_path = radius
        angular_path = angle_in_radians * radius
        total_path = radial_path + angular_path
        if radius !=0 and angle_in_radians !=0:
            radial_ratio = total_path / radial_path
            angular_ratio = total_path / angular_path
        if radius == 0:
            radial_ratio = 0
            angular_ratio = 1
        
        # rectangular coordinates
        initial_position = self.current_pos_dummy1
        origin = (initial_position [0] - radius, initial_position[1])
        current_direction = (self.direction[0], self.direction[1])
        polar_path_x = radius * math.cos(angle_in_radians)
        polar_path_y = radius * math.sin(angle_in_radians)
        destination = (initial_position[0] + polar_path_x, initial_position[1] + polar_path_y)
        
        steps = resolution
        radial_step = radial_path / steps
        angular_step = angle_in_radians / steps
        list_of_steps = list(range(0, steps + 2))
        position_dict = {}
        
        for step in list_of_steps:
            displacement_x = radial_step * step * math.cos(initial_angle + (angular_step * step))
            displacement_y = radial_step * step * -math.sin(initial_angle + (angular_step * step))
            displacement = (displacement_x, displacement_y)
            position_dict[step] = [displacement]

        for step in list_of_steps:
            current_position = position_dict[step][0]
            if step < len(position_dict) - 1:
                next_position = position_dict[step + 1][0]
            else:
                next_direction = (math.sin(initial_angle + angle_in_radians), -math.cos(initial_angle + angle_in_radians))
                next_position = (current_position[0]+(next_direction[0]*self.speed), (current_position[1]+(next_direction[1]*self.speed)))
            displacement_x = current_position[0] - next_position[0]
            displacement_y = current_position[1] - next_position[1]
            displacement = math.sqrt(math.pow(displacement_x,2) + math.pow(displacement_y, 2))
            direction_x = displacement_x / displacement
            direction_y = -displacement_y / displacement
            
            if current_position[0] <= next_position[0]:
                direction_x = abs(direction_x)
            else:
                direction_x = -abs(direction_x)
            
            if current_position[1] <= next_position[1]:
                direction_y = abs(direction_y)
            else: 
                direction_y = -abs(direction_y)
            
            direction = (direction_x, direction_y)
            position_dict[step].append(direction)
        
   
        k = self.polar_move_path_index
        if k < len(position_dict) - 1:
            destination = (initial_position[0] + position_dict[k + 1][0][0], initial_position[1] + position_dict[k + 1][0][1])
            direction = [position_dict[k][1][0], position_dict[k][1][1]]
            
            if destination[0] >= self.pos[0]:
                direction[0] = abs(direction[0])
            elif destination[0] < self.pos[0]: 
                direction[0] = -abs(direction[0])

            
            if destination[1] >= self.pos[1]:
                direction[1] = abs(direction[1])
            elif destination[1] < self.pos[1]: 
                direction[1] = -abs(direction[1])
 
            
            self.direction = pg.math.Vector2(direction[0], direction[1]).normalize()
            
            print(k, position_dict[k][0][0], destination, initial_position[0] + position_dict[k][0][0] - destination[0], self.direction)
            
            check_for_x = False
            check_for_y = False
            
            if destination[0] >= self.pos[0]:    
                check_for_x = self.pos[0] >= destination[0] - (self.direction[0] * self.speed * self.dt)
                diff_x = destination[0] - (self.pos[0] + (self.direction[0] * self.speed * self.dt))
            if destination[0] < self.pos[0]:
                check_for_x = self.pos[0] <= destination[0] - (self.direction[0] * self.speed * self.dt)
                diff_x = destination[0] - (self.pos[0] + (self.direction[0] * self.speed * self.dt))
            
            if destination[1] >= self.pos[1]:
                check_for_y = self.pos[1] >= destination[1] - (self.direction[1] * self.speed * self.dt)
                diff_y = destination[1] - (self.pos[1] + (self.direction[1] * self.speed * self.dt))
            if destination[1] < self.pos[1]:
                check_for_y = self.pos[1] <= destination[1] - (self.direction[1] * self.speed * self.dt)
                diff_y = destination[1] - (self.pos[1] + (self.direction[1] * self.speed * self.dt))
            
            if check_for_x and check_for_y:
                diff = math.sqrt(math.pow(diff_x,2) + math.pow(diff_y,2))
                self.direction = position_dict[k + 1][1]
                self.pos = (destination[0] - (diff*self.direction[0]) * 0, destination[1] - (diff_y*self.direction[1]) * 0)
                self.polar_move_path_index += 1
                self.check_dummy = 0
                
            else:
                self.pos[0] += self.direction[0] * self.speed * self.dt
                self.pos[1] += self.direction[1] * self.speed * self.dt
                self.rect.centerx = round(self.pos[0])
                self.rect.centery = round(self.pos[1])
                


        else:
            self.direction = (position_dict[len(list(position_dict.items()))-1][1])
                        
    # Angular movement            
    def angular_move_old0(self, radius, dummy=[]):
        """This method gives an approximation of circular motion.
        This method only influences the direction of the bullet.
        It is imprecise and not recommended for actual usage."""
        if not dummy:
            self.start_pos_dummy = (self.pos[0], self.pos[1])
            dummy.append(0)
        origin = (self.start_pos_dummy[0] - radius, self.start_pos_dummy[1])
        path = 2*math.pi*radius
        relative_position = (self.pos[0] - origin[0], self.pos[1] - origin[1])
        angular_velocity = (self.pos + (self.direction * self.speed * self.dt))/path
        print(relative_position, angular_velocity)
        self.direction = pg.math.Vector2(((-(self.pos[1] - origin[1]) / radius) * self.dt), (((self.pos[0] - origin[0]) / radius) * self.dt)).normalize()    

    # Movement along a circle
    def angular_move_old1(self, dt, radius, angle, angular_velocity):
        # define circle
        origin = [self.pos[0] - radius, self.pos[1]]
        current_position = [self.pos[0], self.pos[1]]
        # relative_position = (current_position - origin)
        next_position = [current_position[0] + (radius * math.cos(self.theta)), current_position[1] + (radius * -math.sin(self.theta))]
        self.pos = next_position
        self.rect.centerx = round(self.pos[0])
        self.rect.centery = round(self.pos[1])
        current_position = [self.pos[0], self.pos[1]]
        self.theta += (angular_velocity * dt) % 2*math.pi

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
        if self.path == None and self.polar == False:
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
            
    def animate_sprite(self):
        animation = self.animations	
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.pos)
        self.rect = self.rect.inflate((-10, -10))
        self.image = pg.transform.rotate(self.image, math.degrees(math.atan2(self.direction[0], self.direction[1])))

    def move(self, dt):
        self.pos = [self.pos[0], self.pos[1]]
        self.pos[0] += self.direction[0] * self.speed * dt
        self.pos[1] += self.direction[1] * self.speed * dt
        self.rect.centerx = round(self.pos[0])
        self.rect.centery = round(self.pos[1])

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
