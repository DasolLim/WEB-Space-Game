import pygame
import random
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE
from src.player import Player
from src.asteroid import Asteroid
from src.projectile import Projectile
from src.enemy import Enemy

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Asteroid Game")
    clock = pygame.time.Clock()

    player = Player([
        'assets\sprites\spaceship\MainShipBaseFullhealth.png',   # Image 1: health 100-76
        'assets\sprites\spaceship\MainShipBaseSlightdamage.png', # Image 2: health 75-51
        'assets\sprites\spaceship\MainShipBaseDamaged.png',      # Image 3: health 50-26
        'assets\sprites\spaceship\MainShipBaseVerydamaged.png',  # Image 4: health 25-0
    ])

    asteroids = []
    projectiles = []
    score = 0
    # Create an instance of Enemy
    enemy_image_path = 'assets\sprites\enemies\enemy1.png'  # Replace with actual enemy image path
    enemies = [Enemy(enemy_image_path, SCREEN_WIDTH)]

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
                shoot_sound = pygame.mixer.Sound('assets/sprites/sounds/laser.mp3')
                shoot_sound.play()

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
            if not asteroid.exploding:
                asteroid.move()
                
            if asteroid.rect.colliderect(player.rect) and not asteroid.exploding:
                player.health -= 10
                asteroid.explode()  # Start explosion on collision

            elif asteroid.rect.top > SCREEN_HEIGHT:
                asteroids.remove(asteroid)
                score += 10

            # Check for projectile-asteroid collisions
            for projectile in projectiles[:]:
                if projectile.rect.colliderect(asteroid.rect) and not asteroid.exploding:
                    projectiles.remove(projectile)
                    asteroid.explode()  # Start explosion on collision
                    score += 20
                    break

            # Remove asteroid if explosion animation is complete
            if asteroid.is_exploded():
                asteroids.remove(asteroid)

        # Draw asteroids
        for asteroid in asteroids:
            asteroid.draw(screen)
        for enemy in enemies:
            enemy.update(projectiles)  # Update each enemy and add projectiles to list
            enemy.draw(screen)         
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
