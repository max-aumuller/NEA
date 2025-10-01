import pygame
import random
from pygame import Vector2

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (128, 128, 128)

# Create the asteroid class
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
        if self.rect.top > 1100 or self.rect.bottom < -200:
            self.kill()
        elif self.rect.left > 1480 or self.rect.right < -200:
            self.kill()

# Create the mini asteroid class
class Meteor(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, xSpeed, ySpeed):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREY)
        self . rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = xSpeed
        self.y_speed = ySpeed
    
    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.top > 1281 or self.rect.bottom < 0:
            self.kill()
        elif self.rect.left > 900 or self.rect.right < 0:
            self.kill()

# Create player class
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
        self.last_shot_time = 0 # time since a bullet was last fired
        self.shot_cooldown = 250 #how long has to pass before firing another bullet
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

#Create bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((5, 5)) #make the square
        self.image.fill(RED) #make it red
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.velocity = direction.normalize() * 10 #the bullet will always move in a at a fixed speed
    
    def update(self):
        #move the bullet
        self.pos += self.velocity
        self.rect.center = self.pos
        #kill the bullet if it goes off the screen
        if (self.rect.right < 0 or self.rect.left > 1280 or self.rect.bottom < 0 or self.rect.top > 900):
            self.kill()

# Set the width and height of the screen [width, height]
pygame.init()
font = pygame.font.SysFont('ocraextended', 36)
size = (1280, 900)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Asteroids")

# Create groups
asteroids = pygame.sprite.Group()
meteors = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
player1 = Player((320, 240)) #spawn the play at this position
all_sprites.add(player1)

bullets = pygame.sprite.Group()
 
# Loop until the user clicks the close button.
done = False

score = 0
last_score_time= 0

asteroid_counter = 0
max_asteroids = 2

clock = pygame.time.Clock() #used to controll frame rate
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    current_time = pygame.time.get_ticks() # track time for firing cooldown

    #add +1 score every 15 seconds
    if current_time - last_score_time >= 15000:
        score += 1
        last_score_time = current_time
    
    # Handle key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: #quit on escape
        done = True
    if keys[pygame.K_UP]:  # Accelerate forward
        player1.speed += 0.2  # Gradually increase speed

    if keys[pygame.K_LEFT]: # rotate left
        player1.rotate(-5)
    if keys[pygame.K_RIGHT]: # rotate right
        player1.rotate(5)
    if keys[pygame.K_SPACE]: #fire the bullet
        if current_time - player1.last_shot_time >= player1.shot_cooldown:
            bullet = Bullet(player1.pos, player1.direction) # create a new bullet
            bullets.add(bullet)
            all_sprites.add(bullet)
            player1.last_shot_time =  current_time #reset the cooldown timer

    # Spawn asteroids
    if len(asteroids) < 15:
        x_spawn = random.randint(1281, 1301)
        x_choice = random.randint(0,1)
        if x_choice == 0:
            x_spawn -= 1301
        y_spawn = random.randint(901, 921)
        y_choice = random.randint(0,1)
        if y_choice == 0:
            y_spawn -= 921

        print(x_spawn)
        asteroid = Asteroid(20, 20, x_spawn, y_spawn)
        asteroids.add(asteroid)
        all_sprites.add(asteroid)
    
    # Collision detection of player and asteroids
    if pygame.sprite.spritecollide(player1, asteroids, True): #if, true, remove the asteroid
        player1.lives -= 1 #player loses a life
        if player1.lives <=0: #end the game if no lives left
            done = False

    #Collision detection of player and meteorites
    if pygame.sprite.spritecollide(player1, meteors, True):
        player1.lives -=1
        if player1.lives <=0:
            done = False

    # destroyes both the bullet and asteroid if they hit, and spawns in 2 meteorites
    asteroid_hits = pygame.sprite.groupcollide(asteroids, bullets, True, True) 
    for asteroid in asteroid_hits:
        score += 100
        meteor_speed = 3
        x, y = asteroid.rect.center
        meteor1 = Meteor (10, 10, x, y, meteor_speed, -meteor_speed)
        meteor2 = Meteor (10, 10, x, y, -meteor_speed, meteor_speed)
        all_sprites.add(meteor1, meteor2)
        meteors.add(meteor1, meteor2)
    
    meteor_hits = pygame.sprite.groupcollide(bullets, meteors, True, True)
    for meteor in meteor_hits:
        score += 50

    all_sprites.update()
    """
    if asteroid_counter % 60 == 0:
        chanceOfSpawn = random.randint(0, 10)
        if len(asteroids) < max_asteroids:
            if chanceOfSpawn < 8:
                asteroid = Asteroid(20, 20, random.randint(0, 1280), random.randint(0, 900))
                asteroids.add(asteroid)
                all_sprites.add(asteroid)
    """

    screen.fill(WHITE)

    all_sprites.draw(screen)
    asteroid_counter += 1

    #draw the score in the screen
    score_text = font.render(f"score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    lives_text = font.render(f"lives: {player1.lives}", True, BLACK)
    screen.blit(lives_text, (640, 10))

    pygame.display.flip()
    clock.tick(60) #run at 60 fps

pygame.quit()