import pygame
import random
from src.projectile import Projectile  # Import the existing Projectile class

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, screen_width):
        super().__init__()
        
        # Load and scale the enemy image to 66x66 px
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (66, 66))
        self.rect = self.image.get_rect()
        
        # Position at the top of the screen, moving horizontally
        self.screen_width = screen_width
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = 10  # Start at the top of the screen
        
        # Movement variables
        self.speed_x = 3
        self.direction = 1  # 1 for right, -1 for left
        
        # Shooting interval
        self.shoot_interval = random.randint(60, 120)  # Random interval to shoot
        self.shoot_timer = 0
        
        # Health points
        self.hp = 3  # Enemy starts with 3 HP

    def update(self, projectiles):
        """
        Update enemy position and handle shooting.
        """
        # Horizontal movement
        self.rect.x += self.speed_x * self.direction

        # Reverse direction at screen edges
        if self.rect.right >= self.screen_width or self.rect.left <= 0:
            self.direction *= -1

        # Shooting logic
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            # Shoot a red projectile moving downward
            projectile = Projectile(self.rect.centerx, self.rect.bottom, direction='down', color=(255, 0, 0))
            projectiles.append(projectile)  # Add to projectiles list
            self.shoot_timer = 0
            self.shoot_interval = random.randint(60, 120)  # Reset interval

    def take_damage(self, damage):
        """
        Reduces enemy's health by the given damage amount.
        """
        self.hp -= damage
        print(f"Enemy takes {damage} damage, remaining health: {self.hp}")
        if self.hp <= 0:
            self.kill()  # Remove the enemy if HP is 0 or below

    def draw(self, screen):
        """
        Draw the enemy on the screen.
        """
        screen.blit(self.image, self.rect)
