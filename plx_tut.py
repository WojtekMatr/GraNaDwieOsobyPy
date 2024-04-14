import os

import pygame

pygame.init()
GRAVITY = 0.75
clock = pygame.time.Clock()
FPS = 60

# create game window
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 455

moving_left = False
moving_right = False
enemy_moving_left = False
enemy_moving_right = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Parallax")

# define game variables
scroll = 0

ground_image = pygame.image.load("ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

bg_images = []
for i in range(0, 7):
    bg_image = pygame.image.load(f"png/layer_{i}.png").convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()


def draw_bg():
    for x in range(5):
        speed = 1
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.2


def draw_ground():
    for x in range(15):
        screen.blit(ground_image, ((x * ground_width) - scroll * 2.5, SCREEN_HEIGHT - ground_height))





class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.attack = False
        self.attacking = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Attack']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def check_collision(self, enemy):
        if self.rect.colliderect(enemy.rect):  # Sprawdzenie kolizji gracza z przeciwnikiem
            if self.attacking:  # Jeśli gracz atakuje
                enemy.health -= 0.5  # Odejmij punkty życia przeciwnika
                if enemy.health <= 20:
                    enemy.update_action(3)
                    if enemy.health <= 0:
                        print(enemy.health)
                        enemy.kill()
    def death(self):
        if self.health < 0:
            print(enemy.health)
            enemy.kill()
    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            if (self.rect.x > 250):
                dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            if (self.rect.x < 1200):
                dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        if self.attack == True and self.attacking == False:
            self.attacking = False
            self.attacking = True

        self.vel_y += GRAVITY
        if self.vel_y > 12:
            self.vel_y
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 450:
            dy = 450 - self.rect.bottom
            self.in_air = False

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        self.rect.x += dx
        self.rect.y += dy
    def death(self):
        if self.health <= 0:
            self.alive = False
    def update(self):
        self.update_animation()
        self.death()

    def draw(self):
        if self.alive:
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


player = Soldier('player', 150, 390, 0.12, 2)
enemy = Soldier('enemy', 1000, 390, 0.12, 2)
# player2 = Soldier(400, 200, 3)
# game loop
run = True
while run:

    clock.tick(FPS)

    # draw world
    draw_bg()
    draw_ground()
    player.update()
    player.check_collision(enemy)
    player.draw()
    enemy.update()
    #enemy.flip = True
    enemy.draw()
    #enemy.in_air= False
    #enemy.check_collision(player)
    if player.attacking:
        player.update_action(4)
        player.attacking = False
    elif player.in_air:
        player.update_action(2)
    elif moving_left or moving_right:
        player.update_action(1)
    else:
        player.update_action(0)
    player.move(moving_left, moving_right)
    enemy.move(enemy_moving_left,enemy_moving_right)
    enemy.kill()
    if enemy.attacking:
        enemy.update_action(4)
        enemy.attacking = False
    elif enemy.in_air == True:
        enemy.update_action(2)
    elif enemy_moving_left or enemy_moving_right:
            enemy.update_action(1)
    else:
        if enemy.health > 20:
            enemy.update_action(0)
    #if enemy.health <= 0:
        #player.update_action(3)
        #player.kill()
    # get keypresses
    key = pygame.key.get_pressed()
    if key[pygame.K_a] and scroll > 0:
        scroll -= 2
    if key[pygame.K_d] and scroll < 10000:
        scroll += 2

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_e:
                player.attack = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_UP:
                enemy.jump = True
            if event.key == pygame.K_LEFT:
                enemy_moving_left = True
            if event.key == pygame.K_RIGHT:
                enemy_moving_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_e:
                player.attack = False
            if event.key == pygame.K_w:
                shoot = False
            if event.key == pygame.K_UP:
                enemy.jump = False
            if event.key == pygame.K_LEFT:
                enemy_moving_left = False
            if event.key == pygame.K_RIGHT:
                enemy_moving_right = False


    pygame.display.update()

pygame.quit()
