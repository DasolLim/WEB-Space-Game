import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_SPEED

class Asteroid:
    def __init__(self):
        # Load the asteroid image and randomly scale it
        self.original_image = pygame.image.load('assets/sprites/asteroid/asteriod.png').convert_alpha()
        self.scale = random.uniform(0.5, 3)  # Scale factor between 0.5x and 1.5x
        self.image = pygame.transform.scale(
            self.original_image, 
            (int(self.original_image.get_width() * self.scale), int(self.original_image.get_height() * self.scale))
        )
        
        # Set the asteroid's position
        self.rect = self.image.get_rect(
            center=(random.randint(0, SCREEN_WIDTH - self.image.get_width()), -self.image.get_height())
        )
        
        # Define a smaller hitbox inside the asteroid image rect to ignore empty space
        hitbox_margin = 0.6
        self.hitbox = pygame.Rect(
            self.rect.x + int(self.rect.width * hitbox_margin / 2),
            self.rect.y + int(self.rect.height * hitbox_margin / 2),
            int(self.rect.width * (1 - hitbox_margin)),
            int(self.rect.height * (1 - hitbox_margin))
        )

        # Rotation setup
        self.rotation_angle = 0  # Initial rotation angle
        self.rotation_speed = random.uniform(1, 3)  # Random rotation speed between 1 and 3 degrees per frame

        # Explosion animation setup
        self.exploding = False
        self.explosion_images = self.load_explosion_images('assets/sprites/asteroid/asteroidExplode.png', 8)
        self.explosion_index = 0
        self.explosion_frame_delay = 5
        self.explosion_frame_counter = 0

    def load_explosion_images(self, path, frames):
        # Load explosion frames from the sprite sheet and scale them
        sprite_sheet = pygame.image.load(path).convert_alpha()
        explosion_images = []
        frame_width = sprite_sheet.get_width() // frames
        
        for i in range(frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, sprite_sheet.get_height()))
            # Scale each explosion frame to match the asteroid size
            scaled_frame = pygame.transform.scale(
                frame,
                (int(frame_width * self.scale), int(sprite_sheet.get_height() * self.scale))
            )
            explosion_images.append(scaled_frame)
        
        return explosion_images

    def move(self):
        # Move asteroid downwards if not exploding
        if not self.exploding:
            self.rect.y += ASTEROID_SPEED
            self.hitbox.y += ASTEROID_SPEED  # Move the hitbox as well

            # Increase the rotation angle
            self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360  # Keep it within 0-359 degrees

    def draw(self, screen):
        if self.exploding:
            # Draw the explosion animation
            if self.explosion_index < len(self.explosion_images):
                screen.blit(self.explosion_images[self.explosion_index], self.rect)
                # Control animation speed
                self.explosion_frame_counter += 1
                if self.explosion_frame_counter >= self.explosion_frame_delay:
                    self.explosion_frame_counter = 0
                    self.explosion_index += 1
        else:
            # Rotate the image and get the new rect centered on the original position
            rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            
            # Draw the rotated asteroid
            screen.blit(rotated_image, rotated_rect)

            # Uncomment the following line to visualize the hitbox for debugging
            # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def explode(self):
        # Start explosion sequence
        self.exploding = True
        self.explosion_index = 0
        self.explosion_frame_counter = 0

    def is_exploded(self):
        # Check if the explosion animation is complete
        return self.exploding and self.explosion_index >= len(self.explosion_images)
