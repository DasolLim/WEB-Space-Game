import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_SPEED

class Asteroid:
    def __init__(self):
        # Load the asteroid image
        self.image = pygame.image.load('assets/sprites/asteroid/asteriod.png').convert_alpha()
        self.rect = self.image.get_rect(
            center=(random.randint(0, SCREEN_WIDTH - 50), -50)
        )
        
        # Explosion animation setup
        self.exploding = False
        self.explosion_images = self.load_explosion_images('assets/sprites/asteroid/asteroidExplode.png', 8)
        self.explosion_index = 0
        self.explosion_frame_delay = 5  # Adjust frame delay for explosion animation speed
        self.explosion_frame_counter = 0

    def load_explosion_images(self, path, frames):
        # Load explosion frames from the sprite sheet
        sprite_sheet = pygame.image.load(path).convert_alpha()
        explosion_images = []
        frame_width = sprite_sheet.get_width() // frames
        
        for i in range(frames):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, sprite_sheet.get_height()))
            explosion_images.append(frame)
        
        return explosion_images

    def move(self):
        # Move asteroid downwards if not exploding
        if not self.exploding:
            self.rect.y += ASTEROID_SPEED

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
            # Draw the asteroid if it's not exploding
            screen.blit(self.image, self.rect)

    def explode(self):
        # Start explosion sequence
        self.exploding = True
        self.explosion_index = 0
        self.explosion_frame_counter = 0

    def is_exploded(self):
        # Check if the explosion animation is complete
        return self.exploding and self.explosion_index >= len(self.explosion_images)
