import pygame as pg
import sys, time

from settings import *
from mainmenu import MainMenu
from level import Level
from ui import Border

class Game:
    def __init__(self):
        #initialize pygame
        pg.init()
        
        # initialize screen 
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption('Dog Shmup')
        
        # create clock and setup of timestep
        self.clock = pg.time.Clock()
        self.previous_time = time.time()
        self.dt = 0
        
        # setting initial state
        self.state = 'mainmenu'
        self.menu_active = 0 
        self.level_active = 0
    
    def slowdown(self, dt):
        keys = pg.key.get_pressed()
        if keys[pg.K_LCTRL]:
            self.dt = dt / 2 

    def run(self):
        while True:
            # draw empty screen
            self.screen.fill(BACKGROUND_COLOR)
            
            # create a timestep
            self.dt = time.time() - self.previous_time
            self.previous_time = time.time()

            self.slowdown(self.dt)

            # create exit protocol
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            
            # running main menu
            if self.state == 'mainmenu':
                if self.menu_active == 0:                    
                    gamestate = MainMenu()
                    self.menu_active = 1
                gamestate.run()
                if gamestate.start_run() == 0:
                    gamestate = None
                    self.menu_active = 0
                    self.state = 'level'
            
            # starting the level
            if self.state == 'level':
                if self.level_active == 0:
                    gamestate = Level(self.dt)
                    self.level_active = 1
                gamestate.run(self.dt)
            
            # creating a border to indicate 3:4 ratio
            border = Border()
            border.display()

            # update display
            pg.display.update()

            # limit FPS
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()