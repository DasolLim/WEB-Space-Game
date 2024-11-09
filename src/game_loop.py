import pygame
import random
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE
from src.player import Player
from src.asteroid import Asteroid
from src.projectile import Projectile
from src.enemy import Enemy

def display_shop(screen, player):
    font = pygame.font.SysFont(None, 36)
    screen.fill(BLACK)  # Fill the screen with black background for the shop

    # Display player's coins
    coins_text = font.render(f"Coins: {player.coins}", True, WHITE)
    screen.blit(coins_text, (10, 10))

    # Display upgrade options
    power_text = font.render(f"Power (Level {player.power_level}): Cost {player.power_level + 1}", True, WHITE)
    speed_text = font.render(f"Speed (Level {player.speed_level}): Cost {player.speed_level + 1}", True, WHITE)
    health_text = font.render(f"Health (Level {player.health_level}): Cost {player.health_level + 1}", True, WHITE)

    screen.blit(power_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60))
    screen.blit(speed_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
    screen.blit(health_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60))

    # Display instructions
    instructions = font.render("Press 1 to upgrade Power, 2 for Speed, 3 for Health", True, WHITE)
    close_text = font.render("Press P to close the shop", True, WHITE)
    screen.blit(instructions, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 120))
    screen.blit(close_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 160))
    pygame.display.flip()

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Asteroid Game")
    clock = pygame.time.Clock()

    player = Player([
        'assets/sprites/spaceship/MainShipBaseFullhealth.png',   # Image 1: health 100-76
        'assets/sprites/spaceship/MainShipBaseSlightdamage.png', # Image 2: health 75-51
        'assets/sprites/spaceship/MainShipBaseDamaged.png',      # Image 3: health 50-26
        'assets/sprites/spaceship/MainShipBaseVerydamaged.png',  # Image 4: health 25-0
    ])

    asteroids = []
    projectiles = []
    enemies = [Enemy('assets/sprites/enemies/enemy1.png', SCREEN_WIDTH)]
    score = 0
    show_shop = False
    destroyed_asteroids_count = 0  # Counter for asteroids destroyed by the player

    font = pygame.font.SysFont(None, 36)  # Font for displaying text

    running = True
    while running:
        if show_shop:
            display_shop(screen, player)
        else:
            screen.fill(BLACK)
            player.draw(screen)
            for asteroid in asteroids:
                asteroid.draw(screen)
            for enemy in enemies:
                enemy.update(projectiles)
                enemy.draw(screen)
            for projectile in projectiles:
                projectile.draw(screen)

            # Display health, score, and destroyed asteroid count
            health_text = font.render(f"Health: {player.health}", True, WHITE)
            score_text = font.render(f"Score: {score}", True, WHITE)
            destroyed_asteroids_text = font.render(f"Asteroids Destroyed: {destroyed_asteroids_count}", True, WHITE)  # Destroyed asteroids count
            screen.blit(health_text, (10, 10))
            screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
            screen.blit(destroyed_asteroids_text, (SCREEN_WIDTH // 2 - 100, 10))  # Display in the top center

            pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    show_shop = not show_shop  # Toggle the shop
                elif show_shop:
                    # Upgrade logic while shop is open
                    if event.key == pygame.K_1:
                        player.upgrade_power()
                    elif event.key == pygame.K_2:
                        player.upgrade_speed()
                    elif event.key == pygame.K_3:
                        player.upgrade_health()
                elif event.key == pygame.K_SPACE:
                    projectiles.append(Projectile(player.rect.centerx, player.rect.top))

        # Only update the game state if the shop is not open
        if not show_shop:
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

        # Update asteroids and handle collisions
        for asteroid in asteroids[:]:
            if not asteroid.exploding:
                asteroid.move()

            # Check collision with player's hitbox
            if asteroid.hitbox.colliderect(player.hitbox) and not asteroid.exploding:
                player.health -= 10
                asteroid.explode()  # Start explosion on collision

            elif asteroid.hitbox.top > SCREEN_HEIGHT:
                asteroids.remove(asteroid)

        # Check for projectile-asteroid collisions
        # Update projectiles
        for projectile in projectiles[:]:
            projectile.move()
            if projectile.rect.y < 0 or projectile.rect.y > SCREEN_HEIGHT:
                projectiles.remove(projectile)

        # Handle collisions
        for asteroid in asteroids[:]:
            if not asteroid.exploding:
                asteroid.move()

            # Check collision with player's hitbox
            if asteroid.hitbox.colliderect(player.hitbox) and not asteroid.exploding:
                player.health -= 10
                asteroid.explode()

            elif asteroid.rect.top > SCREEN_HEIGHT:
                asteroids.remove(asteroid)

            # Check for player projectile-asteroid collisions
            for projectile in projectiles[:]:
                if projectile.direction == 'up' and projectile.rect.colliderect(asteroid.rect) and not asteroid.exploding:
                    projectiles.remove(projectile)
                    asteroid.explode()
                    score += 20
                    destroyed_asteroids_count += 1
                    break

            if asteroid.is_exploded():
                asteroids.remove(asteroid)

        # Check for enemy projectile collisions with player
        for projectile in projectiles[:]:
            if projectile.direction == 'down' and projectile.rect.colliderect(player.hitbox):
                projectiles.remove(projectile)
                player.health -= 10  # Damage the player


            # Remove asteroid if explosion animation is complete
            if asteroid.is_exploded():
                asteroids.remove(asteroid)

        # Check for projectile-enemy collisions
        for enemy in enemies[:]:
            for projectile in projectiles[:]:
                if projectile.rect.colliderect(enemy.rect):
                    projectiles.remove(projectile)
                    enemy.take_damage()
                    if enemy.hp <= 0:
                        score += 50
                        enemies.remove(enemy)
                        break

        clock.tick(FPS)
