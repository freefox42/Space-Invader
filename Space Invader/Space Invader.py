import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader")

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BORDER = pygame.Rect(WIDTH//2 - 1, 0, 2, HEIGHT)
HEALTH_FONT = pygame.font.SysFont("ubuntu", 20)
WINNER_FONT = pygame.font.SysFont("impact", 100)

FPS = 60
VEL = 4
BULLET_VEL = 8
MAX_BULLET = 8
SPACESHIP_WH = 50

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Space Invader/Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Space Invader/Assets", "Gun+Silencer.mp3"))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Space Invader/Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WH, SPACESHIP_WH)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Space Invader/Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WH, SPACESHIP_WH)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Space Invader/Assets", "space.png")), (WIDTH, HEIGHT))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

def yellow_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 2:
        yellow.y += VEL

def red_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 2:
        red.y += VEL

def bullet_movement(yellow_bullet, red_bullet, yellow, red):
    for bullet in yellow_bullet:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullet.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullet.remove(bullet)
    for bullet in red_bullet:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullet.remove(bullet)
        elif bullet.x < 0:
            red_bullet.remove(bullet)

def draw_window(yellow, red, yellow_bullet, red_bullet, yellow_hp, red_hp):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    yellow_text = HEALTH_FONT.render("Health: " + str(yellow_hp), 1, WHITE)
    red_text = HEALTH_FONT.render("Health: " + str(red_hp), 1, WHITE)
    WIN.blit(yellow_text, (10, 10))
    WIN.blit(red_text, (WIDTH - red_text.get_width() - 10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in yellow_bullet:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullet:
        pygame.draw.rect(WIN, RED, bullet)
    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(4000)

def main():
    yellow = pygame.Rect(150, 300, SPACESHIP_WH, SPACESHIP_WH)
    red = pygame.Rect(800, 300, SPACESHIP_WH, SPACESHIP_WH)
    yellow_bullet = []
    red_bullet = []
    yellow_hp = 10
    red_hp = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_CAPSLOCK and len(yellow_bullet) < MAX_BULLET:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 4)
                    yellow_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullet) < MAX_BULLET:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 4)
                    red_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_hp -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_hp -= 1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if yellow_hp <= 0:
            winner_text = "Red Wins!"
        if red_hp <= 0:
            winner_text = "Yellow Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        key_pressed = pygame.key.get_pressed()
        yellow_movement(key_pressed, yellow)
        red_movement(key_pressed, red)
        bullet_movement(yellow_bullet, red_bullet, yellow, red)
        draw_window(yellow, red, yellow_bullet, red_bullet, yellow_hp, red_hp)
    main()

if __name__ == "__main__":
    main()