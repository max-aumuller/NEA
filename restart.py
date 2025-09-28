import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height]) #create the rectangular object
        self.image.fill(BLACK) #make the object black
        self.rect = self.image.get_rect() #create a rect from the surface
        self.rect.x = x
        self.rect.y = y
        #give the asteroids random speeds so they don't all move the same
        self.x_speed = random.randint(-2, 2)
        self.y_speed = random.randint(-2, 2)

    def update(self):
        #move the asteroid by it's speed each frame
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        #kill the asteroid if it goes off the screen
        if self.rect.top > 900 or self.rect.bottom < 0:
            self.kill()
        elif self.rect.left > 1280 or self.rect.right < 0:
            self.kill()

pygame.init()
size = (1280, 900)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Asteroids")

asteroids = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

done = False
clock = pygame.time.Clock()

while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Spawn asteroids
    if len(asteroids) < 4:
        asteroid = Asteroid(20, 20, random.randint(0, 1280), random.randint(0, 900))
        asteroids.add(asteroid)
        all_sprites.add(asteroid)

    all_sprites.update()

    screen.fill(WHITE)
    all_sprites.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()