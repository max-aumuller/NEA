import pygame

WHITE = (255, 255, 255)

pygame.init()
size = (1280, 900)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Asteroids")

done = False
clock = pygame.time.Clock()

while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()