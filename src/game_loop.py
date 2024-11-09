import pygame
import random
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE
from src.player import Player
from src.asteroid import Asteroid
from src.projectile import Projectile
from src.enemy import Enemy

def end_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Over")
    font_title = pygame.font.Font(pygame.font.match_font('arcadeclassic', bold=True), 72)
    font_options = pygame.font.Font(pygame.font.match_font('arcadeclassic', bold=True), 48)
    font_prompt = pygame.font.Font(pygame.font.match_font('arcadeclassic', bold=True), 42)
    clock = pygame.time.Clock()

    # Load background image and scale to fit screen
    background_image = pygame.image.load("assets/sprites/background/endscreen.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Colors for text and buttons
    title_color = (255, 255, 0)  # Yellow
    button_color = (34, 139, 34)  # Forest Green
    button_hover_color = (50, 205, 50)  # Lime Green
    button_text_color = WHITE

    # Button attributes
    button_width, button_height = 200, 60
    yes_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width - 20, SCREEN_HEIGHT // 2 + 50), (button_width, button_height))
    no_button_rect = pygame.Rect((SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 50), (button_width, button_height))

    running = True
    while running:
        screen.blit(background_image, (0, 0))

        # Display title
        title_text = font_title.render("GAME OVER", True, title_color)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))

        # Display prompt
        prompt_text = font_prompt.render("Do you want to play again?", True, (255, 255, 0))
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()

        yes_color = button_hover_color if yes_button_rect.collidepoint(mouse_pos) else button_color
        no_color = button_hover_color if no_button_rect.collidepoint(mouse_pos) else button_color

        pygame.draw.rect(screen, yes_color, yes_button_rect, border_radius=30)
        pygame.draw.rect(screen, no_color, no_button_rect, border_radius=30)

        yes_text = font_options.render("YES", True, button_text_color)
        no_text = font_options.render("NO", True, button_text_color)
        screen.blit(yes_text, (yes_button_rect.x + button_width // 2 - yes_text.get_width() // 2, yes_button_rect.y + button_height // 2 - yes_text.get_height() // 2))
        screen.blit(no_text, (no_button_rect.x + button_width // 2 - no_text.get_width() // 2, no_button_rect.y + button_height // 2 - no_text.get_height() // 2))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button_rect.collidepoint(event.pos):
                    game_loop()  # Restart the game loop
                if no_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Update display
        pygame.display.flip()
        clock.tick(60)

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

    # Load and scale background image
    background_image = pygame.image.load("assets/sprites/background/level1.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_y1 = 0
    background_y2 = -SCREEN_HEIGHT

    asteroids = []
    projectiles = []
    enemies = [Enemy('assets/sprites/enemies/enemy1.png', SCREEN_WIDTH)]
    score = 0
    show_shop = False

    running = True
    while running:
        if show_shop:
            display_shop(screen, player)
        else:
            # Draw scrolling background
            background_y1 += 1
            background_y2 += 1

            # Reset background positions when they move off the screen
            if background_y1 >= SCREEN_HEIGHT:
                background_y1 = -SCREEN_HEIGHT
            if background_y2 >= SCREEN_HEIGHT:
                background_y2 = -SCREEN_HEIGHT

            screen.blit(background_image, (0, background_y1))
            screen.blit(background_image, (0, background_y2))

            # Draw all game objects
            player.draw(screen)
            for asteroid in asteroids:
                asteroid.draw(screen)
            for enemy in enemies:
                enemy.update(projectiles)
                enemy.draw(screen)
            for projectile in projectiles:
                projectile.draw(screen)

            # Display health and score
            font = pygame.font.SysFont(None, 36)
            health_text = font.render(f"Health: {player.health}", True, WHITE)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(health_text, (10, 10))
            screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

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

        # Update asteroids and check collisions
        for asteroid in asteroids[:]:
            if not asteroid.exploding:
                asteroid.move()

            # Check collision with player's hitbox
            if asteroid.hitbox.colliderect(player.hitbox) and not asteroid.exploding:
                player.health -= 10
                asteroid.explode()  # Start explosion on collision

                # Render end screen if health is zero or below
                if player.health <= 0:
                    end_screen()
                    return

            elif asteroid.rect.top > SCREEN_HEIGHT:
                asteroids.remove(asteroid)

            # Check for projectile-asteroid collisions
            for projectile in projectiles[:]:
                if projectile.rect.colliderect(asteroid.rect) and not asteroid.exploding:
                    projectiles.remove(projectile)
                    asteroid.explode()
                    score += 20
                    break
                if asteroid.is_exploded():
                    asteroids.remove(asteroid)

        # Check for projectile-enemy collisions
        for enemy in enemies[:]:
            for projectile in projectiles[:]:
                if projectile.rect.colliderect(enemy.rect):
                    projectiles.remove(projectile)
                    enemy.take_damage()  # Enemy takes 1 damage
                    if enemy.hp <= 0:
                        score += 50  # Score increase for defeating enemy
                        enemies.remove(enemy)
                        break

        clock.tick(FPS)