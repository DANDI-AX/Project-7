import pygame
import random

# Initializing the game
pygame.init()

# Colors
black = (40, 40, 40)
white = (255, 255, 255)
green = (102, 255, 102)
red = (255, 102, 102)
blue = (102, 178, 255)
yellow = (255, 255, 0)

width, height = 600, 400
game_dis = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

snake_size = 10
snake_speed = 15
message_font = pygame.font.SysFont('calibri', 24, bold=True)
score_font = pygame.font.SysFont('calibri', 18)

special_food_eaten = False
speed_boost_duration = 300  # Number of game loops for speed boost (adjust as needed)
speed_boost_timer = 0

score = 0
special_food_color = yellow  # Yellow color for the special food


# Functions
def print_score(score):
    text = score_font.render("Score: " + str(score), True, white)
    game_dis.blit(text, [10, 10])


def draw_snake(snake_pixel):
    for i, pixel in enumerate(snake_pixel):
        color = green
        if i == len(snake_pixel) - 1:
            color = (0, 255, 0)  # Color for the head
        elif i % 2 == 0:
            color = (0, 200, 0)  # Darker shade for even segments
        pygame.draw.circle(game_dis, color, (int(pixel[0] + snake_size / 2), int(pixel[1] + snake_size / 2)),
                           int(snake_size / 2))


def draw_settings_menu(pass_through_wall):
    settings_font = pygame.font.SysFont('calibri', 24)
    pass_through_text = "On" if pass_through_wall else "Off"
    settings_text = settings_font.render(f"Settings: Pass Through Wall ({pass_through_text}) - Press S to toggle", True, white)
    game_dis.blit(settings_text, [10, height - 30])
    pygame.display.update()

def run_game():
    global snake_speed, special_food_eaten, speed_boost_timer, score
    score = 0  # Reset the score to 0
    game_over = False
    game_close = False
    game_pause = False
    pass_through_wall = False
    x = width / 2
    y = height / 2
    x_speed = snake_size
    y_speed = 0
    snake_pixel = []
    snake_length = 1
    target_x = round(random.randrange(0, ((width - snake_size) / 10.0)) * 10.0)
    target_y = round(random.randrange(0, ((height - snake_size) / 10.0)) * 10.0)
    special_food_x = -10  # Move the special food off-screen
    special_food_y = -10
    while not game_over:
        while game_close:
            game_dis.fill(black)
            game_over_message = message_font.render("Game Over! Press R to Restart or Q to Quit", True, red)
            game_dis.blit(game_over_message, [width / 6, height / 3])
            print_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        run_game()
                    if event.type == pygame.QUIT:
                        game_over = True
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_speed = -snake_size
                    y_speed = 0
                elif event.key == pygame.K_RIGHT:
                    x_speed = snake_size
                    y_speed = 0
                elif event.key == pygame.K_UP:
                    x_speed = 0
                    y_speed = -snake_size
                elif event.key == pygame.K_DOWN:
                    x_speed = 0
                    y_speed = snake_size
                elif event.key == pygame.K_p:
                    game_pause = not game_pause
                elif event.key == pygame.K_s:  # Toggle pass through wall setting
                    pass_through_wall = not pass_through_wall
                    draw_settings_menu(pass_through_wall)

        if game_pause:
            pause_font = pygame.font.SysFont('calibri', 24)
            pause_text = pause_font.render("Paused, press 'P' to resume", True, white)
            game_dis.blit(pause_text, [width / 3, height / 3])
            pygame.display.update()
            continue

        x += x_speed
        y += y_speed

        if pass_through_wall:
            # Wrap around the screen edges
            if x >= width:
                x = 0
            elif x < 0:
                x = width - snake_size
            elif y >= height:
                y = 0
            elif y < 0:
                y = height - snake_size
        else:
            # Game over if the snake hits the walls
            if x >= width or x < 0 or y >= height or y < 0:
                game_close = True

        game_dis.fill(black)
        pygame.draw.circle(game_dis, blue, (int(target_x + snake_size / 2), int(target_y + snake_size / 2)),
                           int(snake_size / 2))
        pygame.draw.circle(game_dis, special_food_color,
                           (int(special_food_x + snake_size / 2), int(special_food_y + snake_size / 2)),
                           int(snake_size / 2))
        snake_pixel.append([x, y])

        if len(snake_pixel) > snake_length:
            del snake_pixel[0]

        for pixel in snake_pixel[:-1]:
            if pixel == [x, y]:
                game_close = True

        draw_snake(snake_pixel)
        print_score(score)
        pygame.display.update()
        if x == target_x and y == target_y:
            score += 1
            target_x = round(random.randrange(0, ((width - snake_size) / 10.0)) * 10.0)
            target_y = round(random.randrange(0, ((height - snake_size) / 10.0)) * 10.0)
            snake_length += 1
            # Generate a special food once every 5 regular foods after the score is over 4
            if score > 5 and score % 6 == 0:
                special_food_x = round(random.randrange(0, ((width - snake_size) / 10.0)) * 10.0)
                special_food_y = round(random.randrange(0, ((height - snake_size) / 10.0)) * 10.0)

        if x == special_food_x and y == special_food_y:
            score += 3  # Add 3 points to the score
            snake_length += 3  # Increase the snake's length by 3
            special_food_eaten = True
            speed_boost_timer = speed_boost_duration
            special_food_x = -10  # Move the special food off-screen
            special_food_y = -10
            snake_speed = 30  # Increase snake's speed

        if special_food_eaten and speed_boost_timer > 0:
            snake_speed = 30  # Adjust the speed boost value as needed
            speed_boost_timer -= 5
        else:
            snake_speed = 15  # Reset snake speed to normal when speed boost ends
            special_food_eaten = False

        clock.tick(snake_speed)
    pygame.quit()
    quit()

run_game()
