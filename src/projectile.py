import pygame
from config import PROJECTILE_SPEED, YELLOW

class Projectile:
    def __init__(self, x, y, direction='up'):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.direction = direction  # 'up' for upward, 'down' for downward

    def move(self):
        if self.direction == 'up':
            self.rect.y -= PROJECTILE_SPEED
        elif self.direction == 'down':
            self.rect.y += PROJECTILE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)