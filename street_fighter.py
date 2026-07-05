
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

        # combat related
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_rect = None
        self.facing_right = True
        self.has_hit = False

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
    
    def attack(self, target):
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = 10   # attack hitbox stays for 10 frames

            self.has_hit = False

            self.facing_right = self.rect.centerx < target.rect.centerx

            if self.facing_right:
                self.attack_rect = pygame.Rect(self.rect.right, self.rect.y + 20, 50, 20)
            else:
                self.attack_rect = pygame.Rect(self.rect.left - 50, self.rect.y + 20, 50, 20)

    def update(self, screen_height: int, screen_width: int, target):
        
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

        if self.is_attacking:
            self.attack_timer -= 1

            if self.attack_rect != None:
                if self.facing_right:
                    self.attack_rect.left = self.rect.right
                else:
                    self.attack_rect.right = self.rect.left

                self.attack_rect.y = self.rect.y + 20

                if self.attack_rect.colliderect(target.rect) and not self.has_hit:
                    target.health -= 10
                    self.has_hit = True
                    print(f"target health is now {target.health}")

            if self.attack_timer == 0:
                self.is_attacking = False
                self.attack_rect = None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        if self.is_attacking and self.attack_rect:
            pygame.draw.rect(screen, (0, 0, 0), self.attack_rect)

pygame.init()

icon_image = pygame.image.load("image.png")

pygame.display.set_caption("Street Fighter")
pygame.display.set_icon(icon_image)

screen = pygame.display.set_mode((0, 0), pygame.NOFRAME) # or pygame.FULLSCREEN

# might need later for borders logic and stuff
screen_height = screen.get_height()
screen_width = screen.get_width()

clock = pygame.Clock()

game_font = pygame.font.SysFont(None, 36)

player1 = Fighter(screen_width / 2 - screen_width / 4, screen_height - 100, (0, 0, 255)) # player 1 = blue
player2 = Fighter(screen_width / 2 + screen_width / 4, screen_height - 100, (255, 0, 0)) # player 2 = red

player1_win_msg = game_font.render("PLAYER ONE WINS!", True, (0, 0, 255))
player2_win_msg = game_font.render("PLAYER TWO WINS!", True, (255, 0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                player1.attack(player2)

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
    
    screen.fill((255, 255, 255)) # white

    player1.update(screen_height, screen_width, player2)
    player2.update(screen_height, screen_width, player1)

    player1_health_bar = pygame.Rect(50, 50, player1.health * 2, 50)
    player2_health_bar = pygame.Rect(screen_width - 50 - player2.health * 2, 50, player2.health * 2, 50)

    pygame.draw.rect(screen, (255, 0, 0), player1_health_bar)
    pygame.draw.rect(screen, (255, 0, 0), player2_health_bar)

    if player2.health <= 0:
        player1.draw(screen)
        screen.blit(player1_win_msg, (screen_width / 2 - player1_win_msg.get_width() / 2, screen_height / 2 - player1_win_msg.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False
        continue
    elif player1.health <= 0:
        player2.draw(screen)
        screen.blit(player2_win_msg, (screen_width / 2 - player2_win_msg.get_width() / 2, screen_height / 2 - player2_win_msg.get_height() / 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False
        continue
    else:
        player1.draw(screen)
        player2.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
