import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player settings
player_size = 30
player_pos = [WIDTH // 2, HEIGHT // 2]
player_angle = 0
player_speed = 5
rotation_speed = 5
bullets = []

# Asteroid settings
asteroid_size = 40
asteroid_speed = 2
asteroids = []

# Define bullet settings
bullet_speed = 10

# Create an asteroid
def create_asteroid():
    x = random.choice([0, WIDTH])
    y = random.choice([0, HEIGHT])
    dx, dy = random.randint(-2, 2), random.randint(-2, 2)
    asteroids.append({'pos': [x, y], 'dir': [dx, dy]})

# Rotate player
def rotate_player(angle):
    rad = math.radians(angle)
    return [math.cos(rad), -math.sin(rad)]

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Fire a bullet
                bullet_dir = rotate_player(player_angle)
                bullets.append({
                    'pos': list(player_pos),
                    'dir': bullet_dir
                })

    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle += rotation_speed
    if keys[pygame.K_RIGHT]:
        player_angle -= rotation_speed
    if keys[pygame.K_UP]:
        move_dir = rotate_player(player_angle)
        player_pos[0] += move_dir[0] * player_speed
        player_pos[1] += move_dir[1] * player_speed

    # Wrap player around screen
    player_pos[0] %= WIDTH
    player_pos[1] %= HEIGHT

    # Update bullets
    for bullet in bullets[:]:
        bullet['pos'][0] += bullet['dir'][0] * bullet_speed
        bullet['pos'][1] += bullet['dir'][1] * bullet_speed
        if not (0 <= bullet['pos'][0] <= WIDTH and 0 <= bullet['pos'][1] <= HEIGHT):
            bullets.remove(bullet)

    # Spawn asteroids
    if len(asteroids) < 5:
        create_asteroid()

    # Update asteroids
    for asteroid in asteroids:
        asteroid['pos'][0] += asteroid['dir'][0] * asteroid_speed
        asteroid['pos'][1] += asteroid['dir'][1] * asteroid_speed
        asteroid['pos'][0] %= WIDTH
        asteroid['pos'][1] %= HEIGHT

    # Collision detection
    for bullet in bullets[:]:
        bullet_x, bullet_y = bullet['pos']
        for asteroid in asteroids[:]:
            asteroid_x, asteroid_y = asteroid['pos']
            distance = math.hypot(bullet_x - asteroid_x, bullet_y - asteroid_y)
            if distance < asteroid_size:
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                break

    # Draw player
    player_vertices = [
        (player_pos[0] + math.cos(math.radians(player_angle)) * player_size,
         player_pos[1] - math.sin(math.radians(player_angle)) * player_size),
        (player_pos[0] + math.cos(math.radians(player_angle + 140)) * player_size // 2,
         player_pos[1] - math.sin(math.radians(player_angle + 140)) * player_size // 2),
        (player_pos[0] + math.cos(math.radians(player_angle - 140)) * player_size // 2,
         player_pos[1] - math.sin(math.radians(player_angle - 140)) * player_size // 2),
    ]
    pygame.draw.polygon(screen, WHITE, player_vertices)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, (int(bullet['pos'][0]), int(bullet['pos'][1])), 5)

    # Draw asteroids
    for asteroid in asteroids:
        pygame.draw.circle(screen, WHITE, (int(asteroid['pos'][0]), int(asteroid['pos'][1])), asteroid_size)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
