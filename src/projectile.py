import pygame
from config import PROJECTILE_SPEED, YELLOW, RED

class Projectile:
    def __init__(self, x, y, direction='up', color=YELLOW, source="player"):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.direction = direction  # 'up' for player projectiles, 'down' for enemy projectiles
        self.color = color  # Color of the projectile
        self.source = source  # Track whether this was fired by "player" or "enemy"

    def move(self):
        # Move up for player projectiles, down for enemy projectiles
        if self.direction == 'up':
            self.rect.y -= PROJECTILE_SPEED
        elif self.direction == 'down':
            self.rect.y += PROJECTILE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
