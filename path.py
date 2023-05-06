import pygame as pg
import math

from settings import *

class CircularPath:
    def __init__(self, dt, position, radius, angle_in_radians, velocity, phase):
        self.initial_position = position
        self.radius = radius
        self.initial_angle = 0 - phase
        self.length_of_path = angle_in_radians * self.radius 
        self.angular_velocity = (velocity * dt) / self.length_of_path
        self.steps = int(round(angle_in_radians / self.angular_velocity))
        self.list_of_steps = list(range(0, self.steps + 1))
        print(self.steps)
        
    def create_dict(self):
        dict = {}
        for step in self.list_of_steps:
            current_angle = self.initial_angle + (self.angular_velocity * step)
            positionx = self.initial_position[0] + math.cos(current_angle) * self.radius
            positiony = self.initial_position[1] + math.sin(current_angle) * self.radius
            dict[step] = (positionx, positiony)
        return dict