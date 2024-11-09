import pygame
import random
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE
from src.player import Player
from src.asteroid import Asteroid
from src.projectile import Projectile
from src.enemy import Enemy
from src.BossEnemy import BossEnemy  # Import the BossEnemy class

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Asteroid Game")
    clock = pygame.time.Clock()
    
    # Load sound effect for shooting
    shoot_sound = pygame.mixer.Sound('assets/sprites/sounds/laser.mp3')
    expo_sound = pygame.mixer.Sound('assets/sprites/sounds/expo.mp3')
    player = Player([
        'assets/sprites/spaceship/MainShipBaseFullhealth.png',   # Image 1: health 100-76
        'assets/sprites/spaceship/MainShipBaseSlightdamage.png', # Image 2: health 75-51
        'assets/sprites/spaceship/MainShipBaseDamaged.png',      # Image 3: health 50-26
        'assets/sprites/spaceship/MainShipBaseVerydamaged.png',  # Image 4: health 25-0
    ])

    asteroids = []
    projectiles = []
    enemies = [Enemy('assets/sprites/enemies/enemy1.png', SCREEN_WIDTH) for _ in range(3)]  # Start with 3 enemies
    enemies_killed = 0  # Track how many enemies have been defeated
    boss_enemy = None  # Initialize boss as None
    boss_spawned = False  # Track if boss has been spawned
    score = 0
    destroyed_asteroids_count = 0  # Counter for asteroids destroyed by the player

    font = pygame.font.SysFont(None, 36)  # Font for displaying text

    running = True
    while running:
        screen.fill(BLACK)

        # Update player's image and draw based on health every frame
        player.update_image()
        player.update_immunity()  # Update immunity status and flashing if applicable
        player.draw(screen)

        # Draw asteroids, enemies, and boss
        for asteroid in asteroids:
            asteroid.draw(screen)
        for enemy in enemies:
            enemy.update(projectiles)
            enemy.draw(screen)
        if boss_enemy:
            boss_enemy.update(projectiles)
            boss_enemy.draw(screen)

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_sound.play()
                    projectiles.append(Projectile(player.rect.centerx, player.rect.top, direction='up', source="player"))

        # Only update the game state if the shop is not open
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
                expo_sound.play()

            # Check for projectile-asteroid collisions
            for projectile in projectiles[:]:
                if projectile.direction == 'up' and projectile.rect.colliderect(asteroid.rect) and not asteroid.exploding:
                    projectiles.remove(projectile)
                    asteroid.explode()
                    expo_sound.play()
                    score += 20
                    destroyed_asteroids_count += 1
                    break

            # Mark asteroid for removal if it is off-screen or exploded
            if asteroid.rect.top > SCREEN_HEIGHT or asteroid.is_exploded():
                asteroids_to_remove.append(asteroid)

        # Remove all asteroids marked for removal
        for asteroid in asteroids_to_remove:
            asteroids.remove(asteroid)

        # Check for enemy projectile collisions with player only
        for projectile in projectiles[:]:
            if projectile.direction == 'down' and projectile.rect.colliderect(player.hitbox):
                projectiles.remove(projectile)
                player.take_damage(10)  # Damage the player using take_damage()

        # Check for projectile-enemy collisions
        for enemy in enemies[:]:
            for projectile in projectiles[:]:
                if projectile.rect.colliderect(enemy.rect) and projectile.source == "player":
                    projectiles.remove(projectile)
                    enemy.take_damage(player.damage)  # Apply damage based on player's power level
                    if enemy.hp <= 0:
                        score += 50
                        enemies_killed += 1  # Increment enemies killed count
                        enemies.remove(enemy)
                        expo_sound.play()
                        break

        # Spawn additional enemies after the first 3 are killed
        if enemies_killed == 3 and len(enemies) == 0 and not boss_spawned:
            enemies.extend([Enemy('assets/sprites/enemies/enemy1.png', SCREEN_WIDTH) for _ in range(5)])

        # Spawn Boss after all 8 regular enemies are defeated
        if enemies_killed == 8 and not boss_spawned:
            boss_enemy = BossEnemy('assets/sprites/boss/boss1.png', SCREEN_WIDTH, SCREEN_HEIGHT)
            boss_spawned = True

        # Check for projectile-boss collision only if boss_enemy exists and projectile is from the player
        if boss_enemy is not None:
            for projectile in projectiles[:]:
                if projectile.rect.colliderect(boss_enemy.rect) and projectile.source == "player":
                    projectiles.remove(projectile)
                    boss_enemy.take_damage(player.damage)
                    if boss_enemy.hp <= 0:  # Boss defeated
                        score += 100  # Reward for defeating the boss
                        boss_enemy = None  # Set boss_enemy to None to avoid further collision checks
                        break  # Exit loop immediately after boss is defeated

        clock.tick(FPS)
