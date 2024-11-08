import pygame
from config import PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.health = 100

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PLAYER_SPEED

    def draw(self, screen):
        screen.blit(self.image, self.rect)
