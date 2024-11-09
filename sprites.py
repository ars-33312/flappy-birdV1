import pygame
from random import choice, randint

W_WIDTH = 480
W_HEIGHT = 800
FPS = 120

#creating background
class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        bg_image = pygame.image.load('graphics/background.png').convert()

        #background scale
        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_height() * scale_factor

        full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))

        #background image scaling
        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_sized_image, (0,0))
        self.image.blit(full_sized_image, (full_height ,0))

        #background pos
        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)
    
    #background moving
    def update(self, dt):
        self.pos.x -= 250 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

#creating ground
class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        #ground image
        ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surface, pygame.math.Vector2(ground_surface.get_size()) * scale_factor)

        #ground pos
        self.rect = self.image.get_rect(bottomleft = (0, W_HEIGHT + 75))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    #ground moving
    def update(self, dt):
        self.pos.x -= 310 * dt
        if self.rect.centerx < 82:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)

#creating bird
class Bird(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        #bird images and animation
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        #bird rect
        self.rect = self.image.get_rect(midleft = (W_WIDTH / 20, W_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #bird falling down speed
        self.gravity = 1200
        self.direction = 0

    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(3):
            surface = pygame.image.load(f'graphics/bird{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surface, pygame.math.Vector2(surface.get_size()) * scale_factor)
            self.frames.append(scaled_surface)

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.direction = -500

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
    def rotate(self):
        rotated_bird = pygame.transform.rotozoom(self.image, -self.direction / 12.5, 1)
        self.image = rotated_bird

    def update(self,dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

#creating obstacles(pipes)
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        orientation = choice(('up','down'))
        surface = pygame.image.load(f'graphics/obstacles/{choice((0,1))}.png').convert_alpha()
        self.image = pygame.transform.scale(surface, pygame.math.Vector2(surface.get_size()) * scale_factor)

        x = W_WIDTH + randint(40,100)

        if orientation == 'up':
            y = W_HEIGHT + randint(100, 150)
            self.rect = self.image.get_rect(midbottom = (x, y))
        else:
            y = randint(-150, -100)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop = (x, y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()