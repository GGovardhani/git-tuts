import pygame
import random
import time
import os

pygame.init()

# Screen settings
width, height = 600, 600
game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Snake and food settings
snake_x, snake_y = width // 2, height // 2
change_x, change_y = 0, 0
food_x, food_y = random.randrange(0, width, 10), random.randrange(0, height, 10)
clock = pygame.time.Clock()
snake_body = [(snake_x, snake_y)]
score = 0  # Score variable
speed = 10  # Starting speed

# Big food settings
big_food = None  # (x, y) position
big_food_timer = 0  # Time to track disappearance

# Font settings
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 50)

# Load high score from file
high_score = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as file:
        try:
            high_score = int(file.read())
        except ValueError:
            high_score = 0

def spawn_big_food():
    """Spawns big food for 5 seconds after every 5 points."""
    global big_food, big_food_timer
    big_food = (random.randrange(0, width, 10), random.randrange(0, height, 10))
    big_food_timer = time.time()  # Start timer

def display_snake_and_food():
    global snake_x, snake_y, food_x, food_y, score, big_food, big_food_timer, speed, high_score

    # Move snake
    snake_x = (snake_x + change_x) % width
    snake_y = (snake_y + change_y) % height

    # Check for collision with itself
    if (snake_x, snake_y) in snake_body[1:]:
        game_over_screen()

    # Add new head position
    snake_body.append((snake_x, snake_y))

    # Check if normal food is eaten
    if (food_x, food_y) == (snake_x, snake_y):
        score += 1
        food_x, food_y = random.randrange(0, width, 10), random.randrange(0, height, 10)
        
        # Increase speed every 10 points
        if score % 10 == 0:
            speed += 3  

        # Spawn big food after every 5 points
        if score % 5 == 0:
            spawn_big_food()
    
    # Check if big food is eaten
    elif big_food and (snake_x, snake_y) == big_food:
        score += 3  # Big food gives 3 points
        big_food = None  # Remove big food

    else:
        del snake_body[0]  # Remove tail only if food is not eaten

    # Remove big food after 5 seconds
    if big_food and time.time() - big_food_timer > 5:
        big_food = None  

    # Draw game screen
    game_screen.fill((0, 0, 0))

    # Draw snake
    for (x, y) in snake_body:
        pygame.draw.rect(game_screen, (0, 255, 0), [x, y, 10, 10])

    # Draw normal food
    pygame.draw.rect(game_screen, (255, 0, 0), [food_x, food_y, 10, 10])

    # Draw big food (yellow) if active
    if big_food:
        pygame.draw.rect(game_screen, (255, 255, 0), [big_food[0], big_food[1], 15, 15])  

    # Render score text
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    game_screen.blit(score_text, (10, 10))

    # Render high score text
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    game_screen.blit(high_score_text, (400, 10))

    # Update display
    pygame.display.update()

def game_over_screen():
    global high_score

    # Update high score if needed
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as file:
            file.write(str(high_score))

    game_screen.fill((0, 0, 0))  
    game_over_text = game_over_font.render("GAME OVER!", True, (255, 0, 0))
    final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    exit_text = font.render("Press any key to exit", True, (200, 200, 200))

    game_screen.blit(game_over_text, (width // 2 - 100, height // 2 - 50))
    game_screen.blit(final_score_text, (width // 2 - 80, height // 2))
    game_screen.blit(high_score_text, (width // 2 - 80, height // 2 + 40))
    game_screen.blit(exit_text, (width // 2 - 110, height // 2 + 80))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                quit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and change_x == 0:
                change_x = -10
                change_y = 0
            elif event.key == pygame.K_d and change_x == 0:
                change_x = 10
                change_y = 0
            elif event.key == pygame.K_w and change_y == 0:
                change_x = 0
                change_y = -10
            elif event.key == pygame.K_s and change_y == 0:
                change_x = 0
                change_y = 10

    display_snake_and_food()
    clock.tick(10)
