import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Asteroid Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game variables
clock = pygame.time.Clock()
FPS = 60  # Frames per second
player_speed = 5
asteroid_speed = 3
projectile_speed = 10
player_health = 100
score = 0
  
# Load player spaceship image
player_img = pygame.image.load('sprites\spaceship\Main Ship - Base - Full health.png')  # Replace with your spaceship image file
player_rect = player_img.get_rect()
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

# Asteroid list
asteroids = []

# Projectile list
projectiles = []

# Function to spawn asteroids
def spawn_asteroid():
    asteroid = pygame.Rect(random.randint(0, SCREEN_WIDTH - 50), -50, 50, 50)
    asteroids.append(asteroid)

# Function to shoot projectiles
def shoot_projectile():
    # Creates a projectile starting from the player's position
    projectile = pygame.Rect(player_rect.centerx, player_rect.top, 5, 10)
    projectiles.append(projectile)

# Game loop
def game_loop():
    global score, player_health

    # Main game loop
    running = True
    while running:
        screen.fill(BLACK)  # Clear screen with black background

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press space to shoot
                    shoot_projectile()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < SCREEN_HEIGHT:
            player_rect.y += player_speed

        # Spawn asteroids at intervals
        if random.randint(1, 60) == 1:
            spawn_asteroid()

        # Move and handle projectiles
        for projectile in projectiles[:]:
            projectile.y -= projectile_speed
            if projectile.y < 0:  # Remove off-screen projectiles
                projectiles.remove(projectile)

        # Move asteroids and check for collisions
        for asteroid in asteroids[:]:
            asteroid.y += asteroid_speed
            if asteroid.colliderect(player_rect):  # Collision with player
                player_health -= 10
                asteroids.remove(asteroid)
            elif asteroid.top > SCREEN_HEIGHT:  # Remove off-screen asteroids
                asteroids.remove(asteroid)
                score += 10

        # Check for projectile-asteroid collisions
        for projectile in projectiles[:]:
            for asteroid in asteroids[:]:
                if projectile.colliderect(asteroid):  # Projectile hits asteroid
                    asteroids.remove(asteroid)
                    projectiles.remove(projectile)
                    score += 20  # Increase score for destroying an asteroid
                    break

        # Draw player
        screen.blit(player_img, player_rect)

        # Draw asteroids
        for asteroid in asteroids:
            pygame.draw.rect(screen, RED, asteroid)

        # Draw projectiles
        for projectile in projectiles:
            pygame.draw.rect(screen, YELLOW, projectile)

        # Display health and score
        font = pygame.font.SysFont(None, 36)
        health_text = font.render(f"Health: {player_health}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(health_text, (10, 10))
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

        # Update display
        pygame.display.flip()

        # Check for game over
        if player_health <= 0:
            print("Game Over!")
            running = False

        # Control the frame rate
        clock.tick(FPS)

# Run the game
game_loop()
pygame.quit()
