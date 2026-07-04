
import pygame

class Fighter:

    def __init__(self, start_x: int, start_y: int, color: tuple):

        # general
        self.rect = pygame.Rect(start_x, start_y, 50, 100) # hitbox
        self.color = color
        self.speed = 10
        self.health = 100

        # moving related
        self.vel_y = 0 # vertical velocity
        self.vel_x = 0 # horizontal velocity
        self.gravity = 1
        self.jump_power = -20
        self.is_jumping = False
        self.is_crouching = False

    def jump(self, moving_left: bool, moving_right: bool):
        if not self.is_jumping:
            self.vel_y = self.jump_power
            self.is_jumping = True

            if moving_left and not moving_right:
                self.vel_x = -self.speed
            elif moving_right and not moving_left:
                self.vel_x = self.speed
            else:
                self.vel_x = 0

    def crouch(self):
        if not self.is_crouching and not self.is_jumping:
            self.rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height / 2, self.rect.width, self.rect.height / 2)
            self.is_crouching = True

    def uncrouch(self):
        if self.is_crouching:
            self.rect = pygame.Rect(self.rect.x, self.rect.y - self.rect.height, self.rect.width, self.rect.height * 2)
            self.is_crouching = False

    def move_right(self):
        if not self.is_jumping and not self.is_crouching:
            self.rect.x += self.speed

    def move_left(self):
        if not self.is_jumping and not self.is_crouching:
            self.rect.x -= self.speed
    
    def update(self, screen_height: int, screen_width: int):
        
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.is_jumping:
            self.rect.x += self.vel_x

        floor = screen_height - 100
        if self.rect.bottom >= floor:
            self.rect.bottom = floor
            self.vel_y = 0
            self.vel_x = 0
            self.is_jumping = False
        
        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

pygame.init()

icon_image = pygame.image.load("image.png")

pygame.display.set_caption("Street Fighter")
pygame.display.set_icon(icon_image)

screen = pygame.display.set_mode((0, 0), pygame.NOFRAME) # or pygame.FULLSCREEN

# might need later for borders logic and stuff
screen_height = screen.get_height()
screen_width = screen.get_width()

clock = pygame.Clock()

WHITE = (255, 255, 255)

player1 = Fighter(350, screen_height - 100, (0, 0, 255)) # player 1 = blue
player2 = Fighter(900, screen_height - 100, (255, 0, 0)) # player 2 = red

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    is_pressing_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
    is_pressing_left = keys[pygame.K_a] or keys[pygame.K_LEFT]

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player1.jump(is_pressing_left, is_pressing_right)

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player1.crouch()
    else:
        player1.uncrouch()

    if is_pressing_right:
        player1.move_right()

    if is_pressing_left:
        player1.move_left()

    if keys[pygame.K_ESCAPE]:
        running = False
    
    screen.fill(WHITE)

    player1.update(screen_height, screen_width)
    player2.update(screen_height, screen_width)

    player1.draw(screen)
    player2.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
