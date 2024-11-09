import pygame
import random
from src.projectile import Projectile

class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, image_path, screen_width, screen_height):
        super().__init__()
        
        # Load and scale the boss image
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (100, 100))  # Boss is larger than regular enemies
        # Start the boss near the middle-top of the screen, but lower than before
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 4))

        # Movement variables
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed_x = 4
        self.direction = 1  # Horizontal movement direction
        self.hp = 20  # Boss has higher health than regular enemies

        # Shooting interval
        self.shoot_interval = 2000  # 2000 ms = 2 seconds
        self.shoot_timer = pygame.time.get_ticks()

    def update(self, projectiles):
        # Horizontal movement
        self.rect.x += self.speed_x * self.direction
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.direction *= -1  # Reverse direction at screen edges

        # Check if it's time to shoot in all directions
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_timer >= self.shoot_interval:
            self.shoot_in_all_directions(projectiles)
            self.shoot_timer = current_time

    def shoot_in_all_directions(self, projectiles):
        """Shoot projectiles in north, east, south, and west directions from the boss."""
        directions = [
            ('up', 0, -1),       # North
            ('down', 0, 1),      # South
            ('left', -1, 0),     # West
            ('right', 1, 0)      # East
        ]
        for dir, dx, dy in directions:
            projectile = Projectile(self.rect.centerx, self.rect.centery, direction=dir, color=(255, 0, 0))
            projectile.dx = dx  # Horizontal speed multiplier
            projectile.dy = dy  # Vertical speed multiplier
            projectiles.append(projectile)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()  # Remove boss when health reaches zero

    def draw(self, screen):
        """Draw the boss on the screen."""
        screen.blit(self.image, self.rect)
