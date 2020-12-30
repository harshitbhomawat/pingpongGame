import random
import sys
import pygame


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.right >= screen_width:
        player_score += 1
        score_time = pygame.time.get_ticks()
    if ball.left <= 0:
        opponent_score += 1
        score_time = pygame.time.get_ticks()
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


def ball_restart():
    global ball_speed_x, ball_speed_y, score_time, screen_width, screen_height, screen
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x, ball_speed_y = (0, 0)
    if current_time - score_time < 700:
        display_number3 = game_font.render("3", True, light_grey)
        screen.blit(display_number3, (screen_width/2, screen_height / 2 - 200))
    elif current_time - score_time < 1400:
        display_number2 = game_font.render("2", False, light_grey)
        screen.blit(display_number2, (screen_width / 2, screen_height / 2 - 200))
    elif current_time - score_time < 2100:
        display_number1 = game_font.render("1", False, light_grey)
        screen.blit(display_number1, (screen_width / 2, screen_height / 2 - 200))
    else:
        score_time = None
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    if opponent.top < ball.top:
        opponent.y += opponent_speed
    if opponent.bottom > ball.bottom:
        opponent.y -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


# General Setup For Every Pygame.
pygame.init()
clock = pygame.time.Clock()
screen_width = 1250
screen_height = 680
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# characters.
# we use every character to be a rect because it will help us to detect collision very efficiently
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)
# colors.
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# speeds.
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Score Variables
player_score = 0
opponent_score = 0

# Creating font
game_font = pygame.font.Font("freesansbold.ttf", 22)

# Timer Starting Point
score_time = True

# A loop.
while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 7
            if event.key == pygame.K_DOWN:
                player_speed += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 7
            if event.key == pygame.K_DOWN:
                player_speed -= 7

    ball_animation()
    player_animation()
    opponent_animation()
    if score_time:
        ball_restart()

    # visuals here order is also necessary because these objects draw on top of each other according to their
    # positions and order
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    player_text = game_font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text, (screen_width / 2 - 25, screen_height / 2))
    opponent_text = game_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text, (screen_width / 2 + 10, screen_height / 2))

    # updating window
    pygame.display.flip()
    clock.tick(70)
