import pygame
import sys
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from src.game_loop import game_loop  # Import game_loop from src/game_loop.py

def home_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Asteroid Game - Home")
    font_title = pygame.font.Font(pygame.font.match_font('freesansbold', bold=True), 72)
    font_subtitle = pygame.font.Font(pygame.font.match_font('freesansbold', bold=True), 48)
    font_options = pygame.font.Font(pygame.font.match_font('freesansbold', bold=True), 36)
    clock = pygame.time.Clock()

    # Load background image and scale to fit screen
    background_image = pygame.image.load("assets/sprites/background/homescreen.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_y = 0

    # Load asteroid sprite sheets
    asteroid_sprite_sheet_1 = pygame.image.load("assets/sprites/background/asteroid2.png")
    asteroid_sprite_sheet_2 = pygame.image.load("assets/sprites/background/asteroid3.png")
    sprite_size_2 = 63  # Each cell is 101x101 pixels for asteroid3
    sprite_size = 128  # Assuming each cell is 128x128 pixels
    asteroid_frames_1 = []
    asteroid_frames_2 = []

    # Extract each frame from the first sprite sheet
    for row in range(6):
        for col in range(6):
            frame = asteroid_sprite_sheet_1.subsurface(pygame.Rect(col * sprite_size, row * sprite_size, sprite_size, sprite_size))
            frame = pygame.transform.scale(frame, (50, 50))
            asteroid_frames_1.append(frame)

    # Extract each frame from the second sprite sheet
    for row in range(7):
        for col in range(7):
            frame = asteroid_sprite_sheet_2.subsurface(pygame.Rect(col * sprite_size_2, row * sprite_size_2, sprite_size_2, sprite_size_2))
            frame = pygame.transform.scale(frame, (50, 50))
            asteroid_frames_2.append(frame)

    # Combine all asteroid frames
    all_asteroid_frames = [asteroid_frames_1, asteroid_frames_2]
    asteroids = []

    # Colors for text and buttons
    title_color = (0, 255, 0)  # Bright Green
    subtitle_color = (255, 255, 255)  # White
    button_color = (255, 165, 0)  # Orange
    button_hover_color = (255, 215, 0)  # Gold
    button_text_color = BLACK

    # Button attributes
    button_width, button_height = 200, 60
    start_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2), (button_width, button_height))
    quit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 100), (button_width, button_height))

    running = True
    while running:
        # Animate background
        background_y = (background_y + 1) % SCREEN_HEIGHT
        screen.blit(background_image, (0, background_y - SCREEN_HEIGHT))
        screen.blit(background_image, (0, background_y))

        # Spawn asteroids at random intervals
        if random.randint(1, 60) == 1:
            x_position = random.randint(0, SCREEN_WIDTH - 50)
            asteroid_type = random.choice(all_asteroid_frames)  # Randomly choose an asteroid type
            asteroids.append({'rect': pygame.Rect(x_position, -50, 50, 50), 'frame_index': 0, 'frames': asteroid_type})

        # Update and draw asteroids
        for asteroid in asteroids[:]:
            asteroid['rect'].y += 3  # Move asteroid down
            asteroid['frame_index'] = (asteroid['frame_index'] + 1) % len(asteroid['frames'])  # Update frame index for animation
            current_frame = asteroid['frames'][asteroid['frame_index']]
            screen.blit(current_frame, asteroid['rect'].topleft)

            if asteroid['rect'].y > SCREEN_HEIGHT:
                asteroids.remove(asteroid)

        # Display title and subtitle
        title_text = font_title.render("SPACE ASTEROID GAME", True, title_color)
        subtitle_text = font_subtitle.render("Defend your ship, fight the odds!", True, subtitle_color)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 200))

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()

        start_color = button_hover_color if start_button_rect.collidepoint(mouse_pos) else button_color
        quit_color = button_hover_color if quit_button_rect.collidepoint(mouse_pos) else button_color

        pygame.draw.rect(screen, start_color, start_button_rect, border_radius=15)
        pygame.draw.rect(screen, quit_color, quit_button_rect, border_radius=15)

        start_text = font_options.render("Start Game", True, button_text_color)
        quit_text = font_options.render("Quit", True, button_text_color)
        screen.blit(start_text, (start_button_rect.x + button_width // 2 - start_text.get_width() // 2, start_button_rect.y + button_height // 2 - start_text.get_height() // 2))
        screen.blit(quit_text, (quit_button_rect.x + button_width // 2 - quit_text.get_width() // 2, quit_button_rect.y + button_height // 2 - quit_text.get_height() // 2))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return True  # Indicate to start the game
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Update display
        pygame.display.flip()
        clock.tick(60)

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

def main():
    while True:
        # Show the home screen and wait for the user to start the game or quit
        start_game = home_screen()
        
        if start_game:
            print("Game Started!")  # Temporary placeholder
            game_loop()  # Calls your actual game loop from src/game_loop.py

if __name__ == "__main__":
    main()
