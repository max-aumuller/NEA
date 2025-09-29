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

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("ship.png").convert_alpha() #load in the image used for the ship
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.xPos = x
        self.yPos = y
        self.xSpeed = 0
        self.ySpeed = 0
    def update(self):
        self.xPos += self.xSpeed
        self.yPos += self.ySpeed
        self.xSpeed *= 0.98
        self.ySpeed *= 0.98
        self.rect.x = self.xPos
        self.rect.y = self.yPos


pygame.init()
size = (1280, 900)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Asteroids")

asteroids = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player1 = Player(320, 240) #spawn the play at this position
all_sprites.add(player1)

done = False
clock = pygame.time.Clock()

while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: #quit on escape
        done = True
    if keys[pygame.K_UP]:  # Accelerate forward
        player1.ySpeed += 0.2  # Gradually increase speed

    if keys[pygame.K_LEFT]: # rotate left
        player1.xSpeed -= 0.2
    if keys[pygame.K_RIGHT]: # rotate right
        player1.xSpeed += 0.2

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