import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

# Define button dimensions and positions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 10

POWER_BUTTON_POS = (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - 120)
SPEED_BUTTON_POS = (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
HEALTH_BUTTON_POS = (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

# Define colors
BUTTON_COLOR = (0, 128, 255)   # Blue color for button
BUTTON_HOVER_COLOR = (30, 144, 255)  # Lighter blue for hover
BAR_COLOR = (50, 205, 50)      # Green color for skill bar
TEXT_COLOR = BLACK              # Black text color
BACKGROUND_COLOR = WHITE        # White background color

def display_shop(screen, player):
    """
    Display the shop menu with upgrade buttons and skill bars.
    """
    font = pygame.font.SysFont(None, 36)
    screen.fill(BACKGROUND_COLOR)

    # Display player's coins at the top left
    coins_text = font.render(f"Coins: {player.coins}", True, TEXT_COLOR)
    screen.blit(coins_text, (10, 10))

    # Draw buttons and skill bars
    draw_skill_upgrade(screen, font, "Power", player.power_level, POWER_BUTTON_POS, player.power_level + 1)
    draw_skill_upgrade(screen, font, "Speed", player.speed_level, SPEED_BUTTON_POS, player.speed_level + 1)
    draw_skill_upgrade(screen, font, "Health", player.health_level, HEALTH_BUTTON_POS, player.health_level + 1)

    # Display instructions at the bottom of the shop
    instructions = font.render("Click a button to upgrade skill", True, TEXT_COLOR)
    close_text = font.render("Press P to close the shop", True, TEXT_COLOR)
    screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT // 2 + 120))
    screen.blit(close_text, (SCREEN_WIDTH // 2 - close_text.get_width() // 2, SCREEN_HEIGHT // 2 + 160))

    pygame.display.flip()

def draw_skill_upgrade(screen, font, skill_name, level, position, cost):
    """
    Draws a button and a skill bar for upgrading a skill.
    """
    # Button hover effect
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(position, (BUTTON_WIDTH, BUTTON_HEIGHT))
    button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR

    # Draw the button
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    
    # Render the skill name, level, and cost on the button
    button_text = font.render(f"{skill_name} (Level {level}): Cost {cost}", True, WHITE)
    screen.blit(button_text, (position[0] + BUTTON_WIDTH // 2 - button_text.get_width() // 2,
                              position[1] + BUTTON_HEIGHT // 2 - button_text.get_height() // 2))

    # Draw skill bar background
    bar_background_rect = pygame.Rect(position[0], position[1] + BUTTON_HEIGHT + 10, BUTTON_WIDTH, 20)
    pygame.draw.rect(screen, BLACK, bar_background_rect, border_radius=5)

    # Calculate and draw the filled portion of the skill bar
    fill_width = int((level / 5) * BUTTON_WIDTH)  # Assuming max level is 5
    fill_rect = pygame.Rect(position[0], position[1] + BUTTON_HEIGHT + 10, fill_width, 20)
    pygame.draw.rect(screen, BAR_COLOR, fill_rect, border_radius=5)

def handle_shop_click(player, mouse_pos):
    """
    Handles the click event for upgrading skills if clicked within the button.
    """
    if is_click_on_button(mouse_pos, POWER_BUTTON_POS):
        player.upgrade_power()
    elif is_click_on_button(mouse_pos, SPEED_BUTTON_POS):
        player.upgrade_speed()
    elif is_click_on_button(mouse_pos, HEALTH_BUTTON_POS):
        player.upgrade_health()

def is_click_on_button(mouse_pos, button_pos):
    """
    Checks if a click is within the boundaries of a button.
    """
    button_rect = pygame.Rect(button_pos, (BUTTON_WIDTH, BUTTON_HEIGHT))
    return button_rect.collidepoint(mouse_pos)
