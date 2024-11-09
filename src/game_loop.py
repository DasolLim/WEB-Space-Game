import pygame
import random
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE
from src.player import Player
from src.asteroid import Asteroid
from src.projectile import Projectile
from src.enemy import Enemy
from src.player_shop import display_shop, handle_shop_click  # Import shop functions

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
    enemies = [Enemy('assets/sprites/enemies/enemy1.png', SCREEN_WIDTH) for _ in range(3)]  # Start with 3 enemies
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

            # Update player's image based on health every frame
            player.update_image()
            player.update_immunity()  # Update immunity status and flashing if applicable
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
            destroyed_asteroids_text = font.render(f"Asteroids Destroyed: {destroyed_asteroids_count}", True, WHITE)
            screen.blit(health_text, (10, 10))
            screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
            screen.blit(destroyed_asteroids_text, (SCREEN_WIDTH // 2 - 100, 10))

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

        # Update projectiles and remove off-screen ones
        projectiles_to_remove = []
        for projectile in projectiles:
            projectile.move()
            # Remove projectile if it goes off the screen (top or bottom)
            if projectile.rect.y < 0 or projectile.rect.y > SCREEN_HEIGHT:
                projectiles_to_remove.append(projectile)

        # Remove all projectiles marked for removal
        for projectile in projectiles_to_remove:
            projectiles.remove(projectile)

        # Update asteroids and handle collisions
        asteroids_to_remove = []
        for asteroid in asteroids:
            if not asteroid.exploding:
                asteroid.move()

            # Check collision with player's hitbox only if the player is not immune
            if not player.is_immune and asteroid.hitbox.colliderect(player.hitbox) and not asteroid.exploding:
                player.take_damage(10)  # Use take_damage to apply immunity
                asteroid.explode()  # Start explosion on collision

            # Check for projectile-asteroid collisions
            for projectile in projectiles[:]:
                if projectile.direction == 'up' and projectile.rect.colliderect(asteroid.rect) and not asteroid.exploding:
                    projectiles.remove(projectile)
                    asteroid.explode()
                    score += 20
                    destroyed_asteroids_count += 1
                    break

            # Mark asteroid for removal if it is off-screen or exploded
            if asteroid.rect.top > SCREEN_HEIGHT or asteroid.is_exploded():
                asteroids_to_remove.append(asteroid)

        # Remove all asteroids marked for removal
        for asteroid in asteroids_to_remove:
            asteroids.remove(asteroid)

        # Check for enemy projectile collisions with player
        for projectile in projectiles[:]:
            if projectile.direction == 'down' and projectile.rect.colliderect(player.hitbox):
                projectiles.remove(projectile)
                player.take_damage(10)  # Damage the player using take_damage()

        # Check for projectile-enemy collisions
        for enemy in enemies[:]:
            for projectile in projectiles[:]:
                if projectile.rect.colliderect(enemy.rect):
                    projectiles.remove(projectile)
                    enemy.take_damage(player.damage)  # Apply damage based on player's power level
                    if enemy.hp <= 0:
                        score += 50
                        enemies.remove(enemy)
                        break

        

        clock.tick(FPS)
