import pygame
import random
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE
from src.player import Player
from src.asteroid import Asteroid
from src.projectile import Projectile
from src.enemy import Enemy
from src.BossEnemy import BossEnemy

# Constants for ammo system
MAX_AMMO = 50
RELOAD_TIME_MS = 2000  # 2 seconds in milliseconds

def end_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Over")
    # (Remaining code for the end screen here...)

def draw_health_bar(screen, player):
    bar_width = 200
    bar_height = 20
    bar_x = 10
    bar_y = 10
    health_ratio = player.health / player.max_health
    pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

def draw_ammo_count(screen, ammo, reloading):
    font = pygame.font.SysFont(None, 36)
    ammo_text = font.render(f"Ammo: {ammo}/{MAX_AMMO}", True, WHITE)
    screen.blit(ammo_text, (10, 40))
    if reloading:
        reload_text = font.render("Reloading...", True, (255, 255, 0))
        screen.blit(reload_text, (10, 70))

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Asteroid Game")
    clock = pygame.time.Clock()
    
    shoot_sound = pygame.mixer.Sound('assets/sprites/sounds/laser.mp3')
    expo_sound = pygame.mixer.Sound('assets/sprites/sounds/expo.mp3')
    bg_sound = pygame.mixer.Sound('assets/sprites/sounds/bg.mp3')
    bg_sound.play()

    player = Player([
        'assets/sprites/spaceship/MainShipBaseFullhealth.png',
        'assets/sprites/spaceship/MainShipBaseSlightdamage.png',
        'assets/sprites/spaceship/MainShipBaseDamaged.png',
        'assets/sprites/spaceship/MainShipBaseVerydamaged.png',
    ])

    background_image = pygame.image.load("assets/sprites/background/level1.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_y1 = 0
    background_y2 = -SCREEN_HEIGHT

    asteroids = []
    projectiles = []
    enemies = [Enemy('assets/sprites/enemies/enemy1.png', SCREEN_WIDTH) for _ in range(3)]
    enemies_killed = 0
    boss_enemy = None
    boss_spawned = False
    score = 0
    destroyed_asteroids_count = 0

    ammo = MAX_AMMO
    reloading = False
    reload_start_time = None

    running = True
    while running:
        # Background scrolling
        background_y1 += 1
        background_y2 += 1
        if background_y1 >= SCREEN_HEIGHT:
            background_y1 = -SCREEN_HEIGHT
        if background_y2 >= SCREEN_HEIGHT:
            background_y2 = -SCREEN_HEIGHT

        screen.blit(background_image, (0, background_y1))
        screen.blit(background_image, (0, background_y2))

        # Player updates and drawing
        player.update_image()
        player.update_immunity()
        player.draw(screen)

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

        # Display health bar, ammo count, and score
        draw_health_bar(screen, player)
        draw_ammo_count(screen, ammo, reloading)
        
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        destroyed_asteroids_text = font.render(f"Asteroids Destroyed: {destroyed_asteroids_count}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
        screen.blit(destroyed_asteroids_text, (SCREEN_WIDTH // 2 - 100, 10))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not reloading:
                    if ammo > 0:
                        shoot_sound.play()
                        projectiles.append(Projectile(player.rect.centerx, player.rect.top, direction='up', source="player"))
                        ammo -= 1
                    else:
                        reloading = True
                        reload_start_time = pygame.time.get_ticks()

        # Handle reloading
        if reloading:
            if pygame.time.get_ticks() - reload_start_time >= RELOAD_TIME_MS:
                ammo = MAX_AMMO
                reloading = False

        # Update player movement
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        # Spawn asteroids at intervals
        if random.randint(1, 60) == 1:
            asteroids.append(Asteroid())

        # Update projectiles and remove off-screen ones
        projectiles_to_remove = []
        for projectile in projectiles:
            projectile.move()
            if projectile.rect.y < 0 or projectile.rect.y > SCREEN_HEIGHT:
                projectiles_to_remove.append(projectile)
        for projectile in projectiles_to_remove:
            projectiles.remove(projectile)

        # Update asteroids and handle collisions
        asteroids_to_remove = []
        for asteroid in asteroids:
            if not asteroid.exploding:
                asteroid.move()

            if not player.is_immune and asteroid.hitbox.colliderect(player.hitbox) and not asteroid.exploding:
                player.take_damage(10)
                asteroid.explode()
                expo_sound.play()

                if player.health <= 0:
                    end_screen()
                    return

            for projectile in projectiles[:]:
                if projectile.direction == 'up' and projectile.rect.colliderect(asteroid.rect) and not asteroid.exploding:
                    projectiles.remove(projectile)
                    asteroid.explode()
                    expo_sound.play()
                    score += 20
                    destroyed_asteroids_count += 1
                    break

            if asteroid.rect.top > SCREEN_HEIGHT or asteroid.is_exploded():
                asteroids_to_remove.append(asteroid)
        for asteroid in asteroids_to_remove:
            asteroids.remove(asteroid)

        # Check for enemy projectile collisions with player only
        for projectile in projectiles[:]:
            if projectile.direction == 'down' and projectile.rect.colliderect(player.hitbox):
                projectiles.remove(projectile)
                player.take_damage(10)

        # Check for projectile-enemy collisions
        for enemy in enemies[:]:
            for projectile in projectiles[:]:
                if projectile.rect.colliderect(enemy.rect) and projectile.source == "player":
                    projectiles.remove(projectile)
                    enemy.take_damage(player.damage)
                    if enemy.hp <= 0:
                        score += 50
                        enemies_killed += 1
                        enemies.remove(enemy)
                        expo_sound.play()
                        break

        if enemies_killed == 3 and len(enemies) == 0 and not boss_spawned:
            enemies.extend([Enemy('assets/sprites/enemies/enemy1.png', SCREEN_WIDTH) for _ in range(5)])

        if enemies_killed == 8 and not boss_spawned:
            boss_enemy = BossEnemy('assets/sprites/boss/boss1.png', SCREEN_WIDTH, SCREEN_HEIGHT)
            boss_spawned = True

        # Import the required font at the top if not already imported
        font_victory = pygame.font.SysFont(None, 100)  # Adjust the font size as needed

        # Check for projectile-boss collision only if boss_enemy exists and projectile is from the player
        if boss_enemy is not None:
            for projectile in projectiles[:]:
                if projectile.rect.colliderect(boss_enemy.rect) and projectile.source == "player":
                    projectiles.remove(projectile)
                    boss_enemy.take_damage(player.damage)
                    if boss_enemy.hp <= 0:  # Boss defeated
                        score += 100  # Reward for defeating the boss
                        boss_enemy = None  # Set boss_enemy to None to avoid further collision checks
                        
                        # Display "VICTORY" text in the center of the screen
                        victory_text = font_victory.render("VICTORY", True, (0, 255, 0))  # Bright green text
                        screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2,
                                                SCREEN_HEIGHT // 2 - victory_text.get_height() // 2))
                        pygame.display.flip()  # Update the display to show the final screen with "VICTORY"

                        pygame.time.delay(3000)  # Freeze the screen for 3 seconds
                        end_screen()  # End the game after the delay
                        return  # Exit the game loop

        clock.tick(FPS)
