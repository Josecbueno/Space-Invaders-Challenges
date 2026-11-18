import pygame
from config import *
from player import Player
from obstacle import Obstacle

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Player Game")
clock = pygame.time.Clock()

# Create a player object
player = Player(375, 530)
player2 = Player(100, 100, PLAYER_COLOR2,2)  # Create a second player object

obstacles = [] # List to store obstacles

last_obstacle_spawn_time = pygame.time.get_ticks()  # Track the last time an obstacle was spawned

score = 0  # Initialize the score
high_score = 0  # Initialize the high score
game_over = False  # Initialize the game over state
paused = False  # Initialize the pause state
# Initialize the survival timer
start_time = pygame.time.get_ticks()
survival_time = 0

font = pygame.font.Font(None, 36)   

def restart_game():
    global player, player2, obstacles, score, game_over, paused
    global start_time, survival_time, pause_start_time

    player = Player(375, 530)
    player2 = Player(100, 100, PLAYER_COLOR2, 2)

    obstacles = []
    score = 0
    game_over = False
    paused = False
    # Reset the survival timer
    start_time = pygame.time.get_ticks()
    survival_time = 0
    pause_start_time = 0


# GAME LOOP
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not game_over:
                if not paused:
                    paused = True
                    pause_start_time = pygame.time.get_ticks()
                else:
                    paused = False
                    start_time += pygame.time.get_ticks() - pause_start_time

            if event.key == pygame.K_r and game_over:
                restart_game()

            # Increase player speed
            if event.key == pygame.K_PLUS or (event.key == pygame.K_EQUALS and event.mod & pygame.KMOD_SHIFT):
                player.speed = min(12, player.speed + 1)

            # Decrease player speed
            if event.key == pygame.K_MINUS:
                player.speed = max(2, player.speed - 1)

    if not game_over and not paused:
        # Update the survival time
        survival_time = (pygame.time.get_ticks() - start_time) // 1000
        #OBSTACLES spawning logic
        # Calculate the obstacle spawn delay based on the score
        current_spawn_delay = max(150, SPAWN_OBSTACLE_DELAY - (score // 10) * 50)

        current_time = pygame.time.get_ticks()

        if current_time - last_obstacle_spawn_time > current_spawn_delay:
            obstacles.append(Obstacle())
            last_obstacle_spawn_time = current_time

        # Update the position of each obstacle
        for obstacle in obstacles:
            obstacle.move()
            # Check collision with both players
            if player.rect.colliderect(obstacle.rect) or player2.rect.colliderect(obstacle.rect):
                game_over = True

        # Remove obstacles that are off the screen
        visible_obstacles = []
        for obstacle in obstacles:
            if not obstacle.is_off_screen():
                visible_obstacles.append(obstacle)
            else :
                score += 1  # Increment the score for each obstacle that goes off screen
                # Update the high score
                if score > high_score:
                    high_score = score
        obstacles = visible_obstacles


        # Update the player's position
        player.moveArrows()
        player2.moveWASD()  # Update the second player's position

    screen.fill(BACKGROUND_COLOR)  # Blue background
    player.draw(screen)  # Draw the player rectangle
    player2.draw(screen)  # Draw the second player rectangle
    
    for obstacle in obstacles:
        obstacle.draw(screen)  # Draw each obstacle

    # Display the score
    
    # Display the current score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Display the survival time
    time_text = font.render(f"Time: {survival_time}s", True, (255, 255, 255))
    screen.blit(time_text, (10, 50))

    # Display the high score
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))
    screen.blit(high_score_text, (10, 90))

    # Display the game over message if the game is over
    if game_over:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

    # Display the pause message if the game is paused
    if paused:
        pause_text = font.render("PAUSE", True, (255, 255, 0))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
    
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()