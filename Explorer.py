from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((50, 58))
        self.image.fill('blue') 


        self.rect= self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()

        self.direction = vector()
        self.speed = 50
        self.gravity = 20
        self.jump = False
        self.jump_height = 100

        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': True, 'left': False, 'right': False}
        

    def input(self):
        keys = pygame.key.get_pressed()

        input_vector = vector(0,0)

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

        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        self.direction.y += self.gravity / 2 * dt
        self.collisions('vertical')

        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.jump = False

    def check_on_surface(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, self.rect.bottom + 1, self.rect.width, 2)

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

                        

    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
