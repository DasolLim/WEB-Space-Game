import pygame
from config import PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, image_paths):
        # Load images for different health levels
        self.images = {
            "full": pygame.image.load(image_paths[0]),
            "three_quarters": pygame.image.load(image_paths[1]),
            "half": pygame.image.load(image_paths[2]),
            "low": pygame.image.load(image_paths[3]),
        }
        self.image = self.images["full"]
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.health = 100

        # Define a smaller hitbox inside the player's image rect
        self.hitbox = pygame.Rect(
            self.rect.x + 7,
            self.rect.y + 8,
            self.rect.width - 15,
            self.rect.height - 15
        )

        # Initialize player skills and coins
        self.coins = 25  # Starting coins
        self.power_level = 0
        self.speed_level = 0
        self.health_level = 0
        self.max_skill_level = 5

        # Base stats
        self.base_speed = PLAYER_SPEED
        self.base_health = 100
        self.base_damage = 1

        # Current stats based on upgrades
        self.speed = self.base_speed
        self.damage = self.base_damage
        self.max_health = self.base_health
        self.health = self.max_health  # Set health to max health initially

        # Immunity variables
        self.is_immune = False
        self.immunity_duration = 1500  # Immunity duration in milliseconds (1.5 seconds)
        self.immunity_start_time = 0
        self.visible = True  # Controls flashing

    def start_immunity(self):
        """Activate immunity and start flashing."""
        self.is_immune = True
        self.immunity_start_time = pygame.time.get_ticks()  # Record the start time of immunity
        self.visible = True  # Start with visible

    def update_immunity(self):
        """Update immunity status and handle flashing."""
        if self.is_immune:
            current_time = pygame.time.get_ticks()
            if current_time - self.immunity_start_time >= self.immunity_duration:
                self.is_immune = False  # End immunity after duration
                self.visible = True  # Ensure player is visible after immunity ends
            else:
                # Flashing effect (toggle visibility every 200ms)
                if (current_time - self.immunity_start_time) // 200 % 2 == 0:
                    self.visible = False
                else:
                    self.visible = True

    def take_damage(self, amount):
        """Take damage if not immune and start immunity."""
        if not self.is_immune:
            self.health -= amount
            self.start_immunity()  # Activate immunity after taking damage

    def upgrade_power(self):
        """
        Increases player power level and damage if coins are sufficient.
        """
        if self.power_level < self.max_skill_level and self.coins >= self.power_level + 1:
            self.coins -= self.power_level + 1
            self.power_level += 1
            self.damage = self.base_damage + self.power_level
            print(f"Power upgraded to level {self.power_level}, damage is now {self.damage}")

    def upgrade_speed(self):
        """
        Increases player speed level if coins are sufficient.
        """
        if self.speed_level < self.max_skill_level and self.coins >= self.speed_level + 1:
            self.coins -= self.speed_level + 1
            self.speed_level += 1
            self.speed = self.base_speed + self.speed_level
            print(f"Speed upgraded to level {self.speed_level}, speed is now {self.speed}")

    def upgrade_health(self):
        """
        Increases player health level and max health if coins are sufficient.
        """
        if self.health_level < self.max_skill_level and self.coins >= self.health_level + 1:
            self.coins -= self.health_level + 1
            self.health_level += 1
            self.max_health = self.base_health + (self.health_level * 10)
            self.health = min(self.health + 10, self.max_health)  # Increase current health by 10, up to max health
            print(f"Health upgraded to level {self.health_level}, max health is now {self.max_health}")

    def update_image(self):
        """
        Update player image based on current health level.
        """
        if self.health > 75:
            self.image = self.images["full"]
        elif 51 <= self.health <= 75:
            self.image = self.images["three_quarters"]
        elif 26 <= self.health <= 50:
            self.image = self.images["half"]
        else:
            self.image = self.images["low"]

    def move(self, keys):
        """
        Handles player movement based on key inputs and speed.
        """
        dx = 0
        dy = 0

        # Horizontal movement
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            dx = -self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            dx = self.speed

        # Vertical movement
        if keys[pygame.K_UP] and self.rect.top > 0:
            dy = -self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            dy = self.speed

        # Apply movement to both image rect and hitbox
        self.rect.x += dx
        self.rect.y += dy
        self.hitbox.x += dx
        self.hitbox.y += dy

    def draw(self, screen):
        if self.visible:  # Draw only if visible (for flashing effect)
            screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)  # Uncomment to visualize the hitbox
