import pygame
import sys
import time
from sprites import BG, Ground, Bird, Obstacle

pygame.init()

running = True
FPS = 120

W_WIDTH = 480
W_HEIGHT = 800

class Game:
    def __init__(self):
        self.display_surface = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        bg_height = pygame.image.load('graphics/background.png').get_height()
        self.scale_factor = W_HEIGHT / bg_height

        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.bird = Bird(self.all_sprites, self.scale_factor * 1.2)

        #timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

    def collision(self):
        if pygame.sprite.spritecollide(self.bird, self.collision_sprites, False)\
        or self.bird.rect.top <= 0:

            pygame.quit()
            sys.exit()

    def run(self):
        last_time = time.time()
        while True:

            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.bird.jump()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump()
                
                if event.type == self.obstacle_timer:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)

            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.collision()
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()
            self.clock.tick(FPS)

if running == True:
    game = Game()
    game.run()
