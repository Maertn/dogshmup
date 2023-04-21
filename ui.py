import pygame as pg
from settings import *

class Border:
    def __init__(self):
        # general
        self.display_surface = pg.display.get_surface()
        
        # border setup
        self.left_border = pg.Rect(0, 0, BORDER_WIDTH, BORDER_HEIGHT)
        self.right_border = pg.Rect(BORDER_WIDTH + GAME_WIDTH, 0, BORDER_WIDTH, BORDER_HEIGHT)
    
    def draw_border(self):
        pg.draw.rect(self.display_surface, BORDER_COLOR, self.left_border)
        pg.draw.rect(self.display_surface, BORDER_COLOR, self.right_border)

    def display(self):
        self.draw_border()