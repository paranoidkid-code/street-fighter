
import pygame

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("hello world!")

clock = pygame.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

x = 350
y = 250

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                y-= 10
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                y += 10
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                x += 10
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                x -= 10
    
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLUE, (x, y, 100, 100))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
