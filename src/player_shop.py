# src/player_shop.py

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE

# Define button dimensions and positions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 10

POWER_BUTTON_POS = (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)
SPEED_BUTTON_POS = (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2)
HEALTH_BUTTON_POS = (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)

def display_shop(screen, player):
    """
    Display the shop menu with upgrade buttons.
    """
    font = pygame.font.SysFont(None, 36)
    screen.fill(BLACK)

    # Display player's coins
    coins_text = font.render(f"Coins: {player.coins}", True, WHITE)
    screen.blit(coins_text, (10, 10))

    # Draw and label buttons for Power, Speed, and Health upgrades
    draw_button(screen, font, "Power", player.power_level, POWER_BUTTON_POS, player.power_level + 1)
    draw_button(screen, font, "Speed", player.speed_level, SPEED_BUTTON_POS, player.speed_level + 1)
    draw_button(screen, font, "Health", player.health_level, HEALTH_BUTTON_POS, player.health_level + 1)

    # Display instructions
    instructions = font.render("Click a button to upgrade skill", True, WHITE)
    close_text = font.render("Press P to close the shop", True, WHITE)
    screen.blit(instructions, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 160))
    screen.blit(close_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 200))

    pygame.display.flip()

def draw_button(screen, font, skill_name, level, position, cost):
    """
    Draws an upgrade button for a skill.
    """
    button_color = (0, 128, 255)  # Blue color
    button_rect = pygame.Rect(position, (BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, button_color, button_rect)

    # Render text for skill and cost
    button_text = font.render(f"{skill_name} (Level {level}): Cost {cost}", True, WHITE)
    screen.blit(button_text, (position[0] + BUTTON_WIDTH // 2 - button_text.get_width() // 2,
                              position[1] + BUTTON_HEIGHT // 2 - button_text.get_height() // 2))

    return button_rect

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
