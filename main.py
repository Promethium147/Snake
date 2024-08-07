import pygame
import random
from time import sleep

# Snake game with Pygame
# github.com/Promethium147
# 2024-08-07

# Control the snake with arrow keys
# Press Q to quit

# Todo
# Show highscore
# Store highscore in file
# Read highscore from file
# Track highscore
# Statistics

# If False, you end on the opposite side, if you "hit" the wall
# Otherwise walls are deadly
DEADLY_WALLS = False

# If False, hitting the snake body is allowed
DEADLY_BODY = True

# I like to use hex colors, Pygame uses RGB, so I convert them
bg_color_hex = "#222222"
snake_color_hex = "#ffff00"
food_color_hex = "#00ff00"
score_color_hex = "#9900ff"
game_over_color_hex = "#ff0000"

SPEED = 10
BLOCK_SIZE = 20

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600


def get_random_nr():
    return round(random.randrange(0, WINDOW_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE


def hex_to_rgb(color):
    color = color.lstrip('#')
    return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))


snake_color = hex_to_rgb(snake_color_hex)
bg_color = hex_to_rgb(bg_color_hex)
food_color = hex_to_rgb(food_color_hex)
score_color = hex_to_rgb(score_color_hex)
game_over_color = hex_to_rgb(game_over_color_hex)

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

game_over = False
score = 0

# Snake start position - Screen center
x1 = WINDOW_WIDTH / 2
y1 = WINDOW_HEIGHT / 2

# Change in x and y
x1_change = 0
y1_change = 0

snake_body = []
length_of_snake = 1

clock = pygame.time.Clock()

# Initial food position
food_x = get_random_nr()
food_y = get_random_nr()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -BLOCK_SIZE
                y1_change = 0
            elif event.key == pygame.K_RIGHT:
                x1_change = BLOCK_SIZE
                y1_change = 0
            elif event.key == pygame.K_UP:
                y1_change = -BLOCK_SIZE
                x1_change = 0
            elif event.key == pygame.K_DOWN:
                y1_change = BLOCK_SIZE
                x1_change = 0
            elif event.key == pygame.K_q:
                game_over = True

    x1 += x1_change
    y1 += y1_change

    if DEADLY_WALLS:
        # Check for collision with wall
        if x1 >= WINDOW_WIDTH or x1 < 0 or y1 >= WINDOW_HEIGHT or y1 < 0:
            game_over = True
    else:
        if x1 > WINDOW_WIDTH:
            x1 = 0
        if x1 < 0:
            x1 = WINDOW_WIDTH
        if y1 > WINDOW_HEIGHT:
            y1 = 0
        if y1 < 0:
            y1 = WINDOW_HEIGHT

    window.fill(bg_color)

    pygame.draw.rect(window, food_color, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

    # Update snake body
    snake_head = [x1, y1]
    snake_body.append(snake_head)

    if len(snake_body) > length_of_snake:
        del snake_body[0]

    if DEADLY_BODY:
        # Check for collision with snake itself, except the head
        for segment in snake_body[:-1]:
            if segment == snake_head:
                game_over = True

    # Drawing the snake
    for segment in snake_body:
        pygame.draw.rect(window, snake_color, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

    # Show score
    font_style = pygame.font.SysFont("Arial", 30)
    score_text = font_style.render("Score: " + str(score), True, score_color)
    window.blit(score_text, (5, 5))
    pygame.display.update()

    # If snake head hits food
    if x1 == food_x and y1 == food_y:
        food_x = get_random_nr()
        food_y = get_random_nr()
        length_of_snake += 1
        score += 1

    # If food spawns on snake body, move it elsewhere
    for segment in snake_body[:-1]:
        if segment[0] == food_x and segment[1] == food_y:
            food_x = get_random_nr()
            food_y = get_random_nr()

    clock.tick(SPEED)

font_style = pygame.font.SysFont(None, 50)
score_text = font_style.render("GAME OVER", True, game_over_color)
tsx = score_text.get_width()
tsy = score_text.get_height()
window.blit(score_text, (WINDOW_WIDTH // 2 - tsx // 2, WINDOW_HEIGHT // 2 - tsy // 2))

pygame.display.update()
sleep(2)

