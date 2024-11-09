import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from src.game_loop import game_loop  # Import game_loop from src/game_loop.py

def home_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Asteroid Game - Home")
    font_title = pygame.font.SysFont(None, 72)
    font_subtitle = pygame.font.SysFont(None, 48)
    font_options = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    # Colors for text and buttons
    title_color = (255, 223, 0)  # Gold
    subtitle_color = (255, 69, 0)  # Red-Orange
    button_color = (0, 128, 255)  # Blue
    button_hover_color = (30, 144, 255)  # Lighter Blue
    button_text_color = WHITE

    # Button attributes
    button_width, button_height = 200, 60
    start_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2), (button_width, button_height))
    quit_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 100), (button_width, button_height))

    running = True
    while running:
        screen.fill(BLACK)

        # Display title and subtitle
        title_text = font_title.render("SPACE ASTEROID GAME", True, title_color)
        subtitle_text = font_subtitle.render("Defend your ship, fight the odds!", True, subtitle_color)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 200))

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()

        start_color = button_hover_color if start_button_rect.collidepoint(mouse_pos) else button_color
        quit_color = button_hover_color if quit_button_rect.collidepoint(mouse_pos) else button_color

        pygame.draw.rect(screen, start_color, start_button_rect)
        pygame.draw.rect(screen, quit_color, quit_button_rect)

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

def main():
    while True:
        # Show the home screen and wait for the user to start the game or quit
        start_game = home_screen()
        
        if start_game:
            print("Game Started!")  # Temporary placeholder
            game_loop()  # Calls your actual game loop from src/game_loop.py

if __name__ == "__main__":
    main()