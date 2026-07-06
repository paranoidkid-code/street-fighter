
import pygame

class Fighter:

    def __init__(self, start_x: int, start_y: int, color: tuple):

        # general
        self.rect = pygame.Rect(start_x, start_y, 50, 100) # hitbox, might need the width to be 70
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
        self.current_attack_damage = 0
        self.attack_offset_y = 0
        self.is_hit = False
        self.hitstun_timer = 0
        self.current_kb_x = 0
        self.current_kb_y = 0

    def jump(self, moving_left: bool, moving_right: bool):
        if not self.is_jumping and not self.is_hit: # might need "and not self.is_attacking"
            self.vel_y = self.jump_power
            self.is_jumping = True

            if moving_left and not moving_right:
                self.vel_x = -self.speed
            elif moving_right and not moving_left:
                self.vel_x = self.speed
            else:
                self.vel_x = 0

    def crouch(self):
        if not self.is_crouching and not self.is_jumping and not self.is_attacking and not self.is_hit:
            self.rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height / 2, self.rect.width, self.rect.height / 2)
            self.is_crouching = True

    def uncrouch(self):
        if self.is_crouching and not self.is_attacking and not self.is_hit:
            self.rect = pygame.Rect(self.rect.x, self.rect.y - self.rect.height, self.rect.width, self.rect.height * 2)
            self.is_crouching = False

    def move_right(self):
        if not self.is_jumping and not self.is_crouching and not self.is_attacking and not self.is_hit:
            self.rect.x += self.speed

    def move_left(self):
        if not self.is_jumping and not self.is_crouching and not self.is_attacking and not self.is_hit:
            self.rect.x -= self.speed
    
    def attack(self, target, attack_type: str):
        if not self.is_attacking and not self.is_hit:
            self.is_attacking = True
            self.has_hit = False

            # ---- punches ----
            if attack_type == "light":
                self.attack_timer = 10
                self.current_attack_damage = 10
                reach = 50
                self.current_kb_x = 5
                self.current_kb_y = -5
            elif attack_type == "medium":
                self.attack_timer = 20
                self.current_attack_damage = 20
                reach = 75
                self.current_kb_x = 8
                self.current_kb_y = -8
            elif attack_type == "heavy":
                self.attack_timer = 30
                self.current_attack_damage = 30
                reach = 100
                self.current_kb_x = 12
                self.current_kb_y = -12

            # ---- kicks ----
            elif attack_type == "light_kick":
                self.attack_timer = 12
                self.current_attack_damage = 12
                reach = 55
                self.current_kb_x = 6
                self.current_kb_y = -6
            elif attack_type == "medium_kick":
                self.attack_timer = 22
                self.current_attack_damage = 22
                reach = 80
                self.current_kb_x = 10
                self.current_kb_y = -10
            elif attack_type == "heavy_kick":
                self.attack_timer = 35
                self.current_attack_damage = 35
                reach = 110
                self.current_kb_x = 15
                self.current_kb_y = -15
            else:
                print(f"unknown keyword {attack_type}")
                self.attack_timer = 10
                self.current_attack_damage = 10
                reach = 50
                self.current_kb_x = 5
                self.current_kb_y = -5

            self.facing_right = self.rect.centerx < target.rect.centerx

            if "kick" in attack_type:
                if self.is_crouching: self.attack_offset_y = 30
                else: self.attack_offset_y = 70
            else:
                self.attack_offset_y = 10

            if self.facing_right:
                self.attack_rect = pygame.Rect(self.rect.right, self.attack_offset_y, reach, 20)
            else:
                self.attack_rect = pygame.Rect(self.rect.left - reach, self.attack_offset_y, reach, 20)

    def update(self, screen_height: int, screen_width: int, target):
        
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.is_jumping or self.is_hit:
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

        if self.is_hit:
            self.hitstun_timer -= 1
            if self.hitstun_timer == 0:
                self.is_hit = False
                if not self.is_jumping:
                    self.vel_x = 0

        if self.is_attacking:
            self.attack_timer -= 1

            if self.attack_rect != None:
                if self.facing_right:
                    self.attack_rect.left = self.rect.right
                else:
                    self.attack_rect.right = self.rect.left

                self.attack_rect.y = self.rect.y + self.attack_offset_y

                if self.attack_rect.colliderect(target.rect) and not self.has_hit:
                    target.health -= self.current_attack_damage
                    self.has_hit = True
                    print(f"target health is now {target.health}")

                    target.is_hit = True
                    target.hitstun_timer = 20

                    target.vel_y = self.current_kb_y

                    if target.vel_y < 0:
                        target.is_jumping = True

                    if self.facing_right:
                        target.vel_x = self.current_kb_x
                    else:
                        target.vel_x = -self.current_kb_x

            if self.attack_timer == 0:
                self.is_attacking = False
                self.attack_rect = None

    def draw(self, screen):
        if self.is_hit:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)
        else:
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
            
            # player 1 attacks
            if event.key == pygame.K_r:
                player1.attack(player2, "light")

            if event.key == pygame.K_t:
                player1.attack(player2, "medium")

            if event.key == pygame.K_y:
                player1.attack(player2, "heavy")

            if event.key == pygame.K_f:
                player1.attack(player2, "light_kick")

            if event.key == pygame.K_g:
                player1.attack(player2, "medium_kick")

            if event.key == pygame.K_h:
                player1.attack(player2, "heavy_kick")

            # player 2 attacks
            if event.key == pygame.K_0:
                player2.attack(player1, "light")

            if event.key == pygame.K_MINUS:
                player2.attack(player1, "medium")

            if event.key == pygame.K_EQUALS:
                player2.attack(player1, "heavy")

            if event.key == pygame.K_p:
                player2.attack(player1, "light_kick")

            if event.key == pygame.K_LEFTBRACKET:
                player2.attack(player1, "medium_kick")

            if event.key == pygame.K_RIGHTBRACKET:
                player2.attack(player1, "heavy_kick")

    keys = pygame.key.get_pressed()

    is_pressing_right = keys[pygame.K_d]
    is_pressing_left = keys[pygame.K_a]

    if keys[pygame.K_w]:
        player1.jump(is_pressing_left, is_pressing_right)

    if keys[pygame.K_s]:
        player1.crouch()
    else:
        player1.uncrouch()

    if is_pressing_right:
        player1.move_right()

    if is_pressing_left:
        player1.move_left()

    p2_is_pressing_right = keys[pygame.K_l]
    p2_is_pressing_left = keys[pygame.K_j]

    if keys[pygame.K_i]:
        player2.jump(p2_is_pressing_left, p2_is_pressing_right)
    
    if keys[pygame.K_k]:
        player2.crouch()
    else:
        player2.uncrouch()

    if p2_is_pressing_right:
        player2.move_right()

    if p2_is_pressing_left:
        player2.move_left()

    if keys[pygame.K_ESCAPE]:
        running = False
    
    screen.fill((255, 255, 255)) # white

    player1.update(screen_height, screen_width, player2)
    player2.update(screen_height, screen_width, player1)

    p1_display_health = max(0, player1.health)
    p2_display_health = max(0, player2.health) # if health < 0, health = 0 for display purposes

    player1_health_bar = pygame.Rect(50, 50, p1_display_health * 2, 50)
    player2_health_bar = pygame.Rect(screen_width - 50 - p2_display_health * 2, 50, p2_display_health * 2, 50)

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
