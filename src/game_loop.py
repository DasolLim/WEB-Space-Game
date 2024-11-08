import pygame
import random
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE
from src.player import Player
from src.asteroid import Asteroid
from src.projectile import Projectile

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Asteroid Game")
    clock = pygame.time.Clock()

    player = Player('assets/sprites/spaceship/Main Ship - Base - Full health.png')
    asteroids = []
    projectiles = []
    score = 0

    font = pygame.font.SysFont(None, 36)
    running = True
    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                projectiles.append(Projectile(player.rect.centerx, player.rect.top))

        # Player movement
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Spawn asteroids at intervals
        if random.randint(1, 60) == 1:
            asteroids.append(Asteroid())

        # Update projectiles
        for projectile in projectiles[:]:
            projectile.move()
            if projectile.rect.y < 0:
                projectiles.remove(projectile)

        # Update asteroids and check collisions
        for asteroid in asteroids[:]:
            asteroid.move()
            if asteroid.rect.colliderect(player.rect):
                player.health -= 10
                asteroids.remove(asteroid)
            elif asteroid.rect.top > SCREEN_HEIGHT:
                asteroids.remove(asteroid)
                score += 10

        # Check for projectile-asteroid collisions
        for projectile in projectiles[:]:
            for asteroid in asteroids[:]:
                if projectile.rect.colliderect(asteroid.rect):
                    projectiles.remove(projectile)
                    asteroids.remove(asteroid)
                    score += 20
                    break

        # Draw everything
        player.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)
        for projectile in projectiles:
            projectile.draw(screen)

        # Display health and score
        health_text = font.render(f"Health: {player.health}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(health_text, (10, 10))
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

        # Update display and check for game over
        pygame.display.flip()
        if player.health <= 0:
            print("Game Over!")
            running = False

        clock.tick(FPS)
