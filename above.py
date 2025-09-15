from settings import *
from sprites import Sprite, AnimatedSprite, Node, Icon, PathSprite
from groups import WorldSprites
from random import randint


class AboveWorld:
    def __init__(self, tmx_map, data, aboveworld_frames, switch_stage):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.switch_stage = switch_stage

        self.all_sprites = WorldSprites(data)
        self.node_sprites = pygame.sprite.Group()

        self.setup(tmx_map, aboveworld_frames)

        self.current_node = [node for node in self.node_sprites if node.level == 0][0]

        self.path_frames = aboveworld_frames['path']
        self.create_path_sprites()

    def setup(self, tmx_map, aboveworld_frames):


        for layer in ['main','top']:
            for x,y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, Z_LAYERS['bg tiles'])



        for col in range(tmx_map.width):
            for row in range(tmx_map.height):
                AnimatedSprite((col * TILE_SIZE, row * TILE_SIZE), aboveworld_frames['water'], self.all_sprites, Z_LAYERS['bg'])



        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'palm':
                AnimatedSprite((obj.x, obj.y), aboveworld_frames['palm'], self.all_sprites, Z_LAYERS['main'])
            else:
                z = Z_LAYERS[f'{'bg details' if obj.name == 'grass' else 'bg tiles'}']
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, z)


        self.paths = {}
        for obj in tmx_map.get_layer_by_name('Paths'):
            pos = [(int(p.x + TILE_SIZE / 2), int(p.y + TILE_SIZE / 2)) for p in obj.points]

            start = obj.properties['start']
            end = obj.properties['end']
            self.paths[end] = {'pos': pos, 'start': start}
            



        for obj in tmx_map.get_layer_by_name('Nodes'):

            if obj.name == 'Node' and obj.properties['stage']== self.data.current_level:
                self.icon = Icon((obj.x + TILE_SIZE / 2,obj.y + TILE_SIZE / 2),self.all_sprites,aboveworld_frames['icon'] )

            if obj.name == 'Node':
                available_path = {k:v for k,v in obj.properties.items() if k in {'left','right','up','down'}}
                Node(pos = (obj.x, obj.y),
                    surf = aboveworld_frames['path']['node'],
                    groups = (self.all_sprites,self.node_sprites),
                    level = obj.properties['stage'],
                    data = self.data,
                    paths = available_path)
   
   
    def create_path_sprites(self):
        print("Creating paths for level:", [node.level for node in self.node_sprites])
        print("Available paths:", self.paths.keys())

        # Map node levels to grid positions
        nodes = {node.level: vector(node.grid_pos) for node in self.node_sprites}

        path_tiles = {}

        # Iterate only over paths that actually exist
        for path_id in sorted(self.paths.keys()):
            data = self.paths[path_id]
            path = data['pos']
            start_node, end_node = nodes[data['start']], nodes[path_id]
            path_tiles[path_id] = [start_node]

            for index, points in enumerate(path):
                if index < len(path) - 1:
                    start, end = vector(points), vector(path[index + 1])
                    path_dir = (end - start) / TILE_SIZE
                    start_tile = vector(int(start[0] / TILE_SIZE), int(start[1] / TILE_SIZE))

                    # Y-direction tiles
                    if path_dir.y:
                        dir_y = 1 if path_dir.y > 0 else -1
                        for y in range(dir_y, int(path_dir.y) + dir_y, dir_y):
                            path_tiles[path_id].append(start_tile + vector(0, y))

                    # X-direction tiles
                    if path_dir.x:
                        dir_x = 1 if path_dir.x > 0 else -1
                        for x in range(dir_x, int(path_dir.x) + dir_x, dir_x):
                            path_tiles[path_id].append(start_tile + vector(x, 0))

            path_tiles[path_id].append(end_node)

        # Create PathSprites
        for key, path in path_tiles.items():
            for index, tile in enumerate(path):
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

                if 0 < index < len(path) - 1:
                    prev_tile = path[index - 1] - tile
                    next_tile = path[index + 1] - tile

                    if prev_tile.x == next_tile.x:
                        surf = self.path_frames['vertical']
                    elif prev_tile.y == next_tile.y:
                        surf = self.path_frames['horizontal']
                    elif (prev_tile.x, prev_tile.y, next_tile.x, next_tile.y) in [(-1, 0, 0, -1), (0, -1, -1, 0)]:
                        surf = self.path_frames['tl']
                    elif (prev_tile.x, prev_tile.y, next_tile.x, next_tile.y) in [(1, 0, 0, 1), (0, 1, 1, 0)]:
                        surf = self.path_frames['br']
                    elif (prev_tile.x, prev_tile.y, next_tile.x, next_tile.y) in [(-1, 0, 0, 1), (0, 1, -1, 0)]:
                        surf = self.path_frames['bl']
                    elif (prev_tile.x, prev_tile.y, next_tile.x, next_tile.y) in [(1, 0, 0, -1), (0, -1, 1, 0)]:
                        surf = self.path_frames['tr']
                    else:
                        surf = self.path_frames['horizontal']

                PathSprite(
                    pos=(tile.x * TILE_SIZE, tile.y * TILE_SIZE),
                    surf=surf,
                    groups=self.all_sprites,
                    level=key
                )


    def input(self):
        keys = pygame.key.get_pressed()
        if self.current_node and not self.icon.path:
            if keys[pygame.K_w] and self.current_node.can_move('up'):
                self.move('up')
            if keys[pygame.K_d] and self.current_node.can_move('right'):
                self.move('right')
            if keys[pygame.K_s] and self.current_node.can_move('down'):
                self.move('down')
            if keys[pygame.K_a] and self.current_node.can_move('left'):
                self.move('left')
            if keys[pygame.K_RETURN]:
                self.data.current_level = self.current_node.level
                self.switch_stage('level')

    def move(self, direction):
        path_key = int(self.current_node.paths[direction][0])
        path_reverse = True if self.current_node.paths[direction][-1] == 'r' else False
        path = self.paths[path_key]['pos'][:] if not path_reverse else self.paths[path_key]['pos'][::-1]
        self.icon.start_move(path)

    def get_current_node(self):
        nodes = pygame.sprite.spritecollide(self.icon, self.node_sprites, False)
        if nodes:
            self.current_node = nodes[0]

    def run(self,dt):
        self.input()
        self.get_current_node()
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.icon.rect.center)