import pygame
import random
from config import SCREEN_WIDTH, ASTEROID_SPEED, RED

class Asteroid:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 50), -50, 50, 50)

    def move(self):
        self.rect.y += ASTEROID_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
