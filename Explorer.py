from settings import *
from ticker import Ticker

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((50, 58))
        self.image.fill('blue') 


        self.rect= self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()

        self.direction = vector()
        self.speed = 100
        self.gravity = 60
        self.jump = False
        self.jump_height = 200

        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': True, 'left': False, 'right': False}


        self.ticker = {
            'wall jump': Ticker(200),
            'wall slide block': Ticker(100)
        }

    def input(self):
        keys = pygame.key.get_pressed()

        input_vector = vector(0,0)
        if not self.ticker['wall jump'].active:
            if keys[pygame.K_d]:
                input_vector.x += 1
            if keys[pygame.K_a]:
                input_vector.x -= 1

            self.direction.x = input_vector.normalize().x  if input_vector else input_vector.x
                
        if keys[pygame.K_SPACE] and self.direction.y == 0:
                self.jump = True
               

    def move(self,dt):

        self.rect.x += self.direction.x * self.speed * dt
        self.collisions('horizontal')

        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.ticker['wall slide block'].active:
            self.direction.y = 0
            self.rect.y += self.gravity * dt
            
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt
            self.direction.y += self.gravity / 2 * dt
            
    
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.ticker['wall slide block'].activate()
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.ticker['wall slide block'].active:
                self.ticker['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False

        self.collisions('vertical')     
    

    def check_on_surface(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        right_rect = pygame.Rect(self.rect.topright + vector(0,self.rect.height / 4), (2, self.rect.height / 2))
        left_rect = pygame.Rect(self.rect.topleft + vector(0,self.rect.height / 4), (-2, self.rect.height / 2))


        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False
        

    def collisions(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right

                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left

                else:  
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0  

                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0  

    def update_tickers(self):  
        for ticker in self.ticker.values():
            ticker.update() 

    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.update_tickers()
        self.input()
        self.move(dt)
        self.check_on_surface()
    
