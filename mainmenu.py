import pygame as pg
from settings import *

class MainMenu:
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.Font(MENU_FONT, MENU_FONT_SIZE)
    
    def show_main_menu_text(self):
        text_surf = self.font.render('Dog Shmup', False, MENU_COLOR)
        x = SCREEN_WIDTH / 2
        y = SCREEN_HEIGHT / 2 - 200
        text_rect = text_surf.get_rect(center = (x,y))

        pg.draw.rect(self.display_surface, 'black', text_rect)
        self.display_surface.blit(text_surf, text_rect)
    
    def start_run(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            return 0
        

    def run(self):
        self.show_main_menu_text()
        self.start_run()