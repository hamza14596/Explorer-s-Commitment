from settings import *


class AboveWorld:
    def __init__(self, tmx_map, data, aboveworld_frames):
        self.display_surface = pygame.display.get_surface()
        self.data = data

        self.all_sprites = pygame.sprite.Group()

        self.setup(tmx_map, aboveworld_frames)

    def setup(self, tmx_map, aboveworld_frames):
        pass

    def run(self,dt):
        pass