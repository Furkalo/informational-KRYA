import pygame

class Target:
    def __init__(self, x, y, image, speed_multiplier=1):
        self.x = x
        self.y = y
        self.image = image
        self.speed_multiplier = speed_multiplier
        self.rect = pygame.Rect(x + 20, y, 60, 60)

    def move(self, width):
        self.x -= 2 ** self.speed_multiplier
        if self.x < -150:
            self.x = width
        self.rect.x = self.x + 20

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))