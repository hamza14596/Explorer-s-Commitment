from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from help import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Explorer's Commitment")
        self.clock = pygame.time.Clock()
        self.import_assets()    

        self.tmx_maps= {0: load_pygame('data/levels/omni.tmx')}
        self.current_stage = Level(self.tmx_maps[0], self.level_frames)

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('graphics', 'level', 'flag'),
            'saw' : import_folder('graphics', 'enemies', 'saw', 'animation'),
            'floor_spike' : import_folder('graphics', 'enemies', 'floor_spikes'),
            'palms' : import_sub_folders('graphics', 'level', 'palms')
        }
        

    def run(self):
        dt = self.clock.tick(60) / 1000
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(dt) 
            pygame.display.update()
    


if __name__ == '__main__': 
    game = Game()
    game.run()

