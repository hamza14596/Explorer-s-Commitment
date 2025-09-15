from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from help import *
from data import Data
from debug import debug
from UI import UI
from above import AboveWorld

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Explorer's Commitment")
        self.clock = pygame.time.Clock()
        self.import_assets()    

        self.UI = UI(self.font, self.UI_frames)
        self.data = Data(self.UI)
        self.tmx_maps= {
            0: load_pygame('data/levels/0.tmx'),
            1: load_pygame('data/levels/1.tmx'),
            2: load_pygame('data/levels/2.tmx'),
            3: load_pygame('data/levels/3.tmx'),
            4: load_pygame('data/levels/4.tmx'),
            5: load_pygame('data/levels/5.tmx'),
            6: load_pygame('data/levels/6.tmx')
            
            }
        self.tmx_aboveworld = load_pygame('data/overworld/overworld.tmx')
        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames,self.audio_files, self.data, self.switch_stage)
        self.bg_music.play()

    def switch_stage(self, target, unlock = 0):
        if target == 'level':
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames,self.audio_files, self.data, self.switch_stage)
            pass
        else:
            if unlock > 0:
                self.data.unlocked_level = unlock
            else:
                self.data.health -= 1
            self.current_stage = AboveWorld(self.tmx_aboveworld, self.data, self.aboveworld_frames, self.switch_stage)
            

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('graphics', 'level', 'flag'),
            'saw' : import_folder('graphics', 'enemies', 'saw', 'animation'),
            'floor_spike' : import_folder('graphics', 'enemies', 'floor_spikes'),
            'palms' : import_sub_folders('graphics', 'level', 'palms'),
            'candle': import_folder('graphics', 'level', 'candle'),
            'window': import_folder('graphics', 'level', 'window'),
            'big_chain': import_folder('graphics', 'level', 'small_chains'),
            'small_chain': import_folder('graphics','level', 'small_chains'),
            'candle_light': import_folder('graphics','level','candle light'),
            'player' : import_sub_folders('graphics','player'),
            'saw' : import_folder('graphics','enemies','saw','animation'),
            'saw_chain' : import_folder('graphics','enemies','saw','saw_chain'),
            'helicopter' : import_folder('graphics','level','helicopter'),
            'boat' : import_folder('graphics','objects','boat'),
            'spike' : import_image('graphics','enemies','spike_ball','Spiked Ball'),
            'spike_chain' : import_image('graphics','enemies','spike_ball','spiked_chain'),
            'tooth': import_folder('graphics','enemies','tooth','run'),
            'shell': import_sub_folders('graphics','enemies','shell'),
            'pearl': import_image('graphics','enemies','bullets','pearl'),
            'items': import_sub_folders('graphics','items'),
            'particle': import_folder('graphics','effects','particle'),
            'items': import_sub_folders('graphics','items'),
            'water_top' : import_folder('graphics', 'level', 'water', 'top'),
            'water_body': import_image('graphics','level','water','body'),
            'bg_tiles' : import_folder_dict('graphics','level','bg','tiles'),
            'cloud_small': import_folder('graphics', 'level', 'clouds', 'small'),
            'cloud_large' : import_image('graphics','level','clouds','large_cloud')
        }

        self.font = pygame.font.Font('graphics/ui/runescape_uf.ttf', 40)
        self.UI_frames = {
            'heart' : import_folder('graphics','ui','heart'),
            'coin': import_image('graphics','ui','coin')
            
        }

        self.aboveworld_frames = {
            'palm' : import_folder('graphics','overworld','objects','palm'),
            'water' : import_folder('graphics','overworld','objects','water'),
            'path' : import_folder_dict('graphics','objects','overworld','path'),
            'icon': import_sub_folders('graphics','map','icon')
        }

        self.audio_files = {
            'coin': pygame.mixer.Sound('audio/coin.wav'),
            'attack':pygame.mixer.Sound('audio/attack.wav'),
            'jump':pygame.mixer.Sound('audio/jump.wav'),
            'damage':pygame.mixer.Sound('audio/damage.wav'),
            'pearl':pygame.mixer.Sound('audio/pearl.wav')
        }

        self.bg_music = pygame.mixer.Sound('audio/Ruder Buster.mp3')

    def check_game_over(self):
        if self.data.health <= 0:
            pygame.quit()
            sys.exit()

        

    def run(self):
        dt = self.clock.tick(30) / 2500
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.check_game_over()
            self.current_stage.run(dt) 
            self.UI.update(dt)
              
            pygame.display.update()
           
    


if __name__ == '__main__': 
    game = Game()
    game.run()

