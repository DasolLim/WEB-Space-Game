import pygame
from config import PROJECTILE_SPEED, YELLOW

class Projectile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)

    def move(self):
        self.rect.y -= PROJECTILE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)
