import pygame
import random
from pygame import Vector2

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
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("ship.png").convert_alpha() #load in the image used for the ship
        self.image = pygame.transform.scale(self.image, (50, 50)) #make the image the same size as the ship's rectangle
        self.orig_image = self.image  # Store original image for rotation so quality isn't lost
        self.rect = self.image.get_rect(center=pos) #place the ship in it's starting position
        self.pos = Vector2(pos)  #Use a Vector2 for precise positioning
        self.direction = Vector2(0, -1)  #Facing upward initially
        self.speed = 0  #Movement speed
        self.angle = 0  #Rotation angle in degrees
        self.lives = 3 #the player's lives

    def update(self):
        # Move the player in the direction it is facing
        self.pos += self.direction * self.speed
        self.rect.center = self.pos  # Keep rect updated so it matches Vector2

        # Apply friction
        self.speed *= 0.98

        # Screen wrapping
        if self.rect.top > 900:
            self.pos.y = 0
        elif self.rect.bottom < 0:
            self.pos.y = 900
        if self.rect.left > 1280:
            self.pos.x = 0
        elif self.rect.right < 0:
            self.pos.x = 1280

    def rotate(self, angle_change):
        #rotate the player
        self.angle += angle_change
        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1) #rotate the image
        self.rect = self.image.get_rect(center=self.rect.center)  # Keep center position
        self.direction = Vector2(0, -1).rotate(self.angle)  # Update movement direction


pygame.init()
size = (1280, 900)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Asteroids")

asteroids = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player1 = Player((320, 240)) #spawn the play at this position
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
        player1.speed += 0.2  # Gradually increase speed

    if keys[pygame.K_LEFT]: # rotate left
        player1.rotate(-5)
    if keys[pygame.K_RIGHT]: # rotate right
        player1.rotate(5)

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