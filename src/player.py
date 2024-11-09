import pygame
from config import PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, image_paths):  # Renamed image_path to image_paths
        # Load images for different health levels
        self.images = {
            "full": pygame.image.load(image_paths[0]),
            "three_quarters": pygame.image.load(image_paths[1]),
            "half": pygame.image.load(image_paths[2]),
            "low": pygame.image.load(image_paths[3]),
        }
        self.image = self.images["full"]  # Start with the full health image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.health = 100

    def update_image(self):
        # Update player image based on current health
        if self.health > 75:
            self.image = self.images["full"]
        elif 51 <= self.health <= 75:
            self.image = self.images["three_quarters"]
        elif 26 <= self.health <= 50:
            self.image = self.images["half"]
        else:
            self.image = self.images["low"]

    def move(self, keys):
        dx = 0
        dy = 0

        # Horizontal movement
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            dx = PLAYER_SPEED

        # Vertical movement
        if keys[pygame.K_UP] and self.rect.top > 0:
            dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            dy = PLAYER_SPEED

        # Apply movement
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)
