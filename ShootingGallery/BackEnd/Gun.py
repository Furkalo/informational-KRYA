import pygame
import math

class Gun:
    def __init__(self, width, height, gun_images):
        self.width = width
        self.height = height
        self.gun_images = gun_images
        self.lasers = ['red', 'purple', 'green']

    def calculate_rotation(self, mouse_pos):
        gun_point = (self.width / 2, self.height - 200)

        if mouse_pos[0] != gun_point[0]:
            slope = (mouse_pos[1] - gun_point[1]) / (mouse_pos[0] - gun_point[0])
        else:
            slope = -100000

        angle = math.atan(slope)
        return math.degrees(angle)

    def draw(self, screen, level, mouse_pos):
        rotation = self.calculate_rotation(mouse_pos)
        gun_point = (self.width / 2, self.height - 200)

        if mouse_pos[0] < self.width / 2:
            gun = pygame.transform.flip(self.gun_images[level - 1], True, False)
            if mouse_pos[1] < 600:
                rotated_gun = pygame.transform.rotate(gun, 90 - rotation)
                screen.blit(rotated_gun, (self.width / 2 - 90, self.height - 250))

                clicks = pygame.mouse.get_pressed()
                if clicks[0]:
                    pygame.draw.circle(screen, self.lasers[level - 1], mouse_pos, 5)
        else:
            gun = self.gun_images[level - 1]
            if mouse_pos[1] < 600:
                rotated_gun = pygame.transform.rotate(gun, 270 - rotation)
                screen.blit(rotated_gun, (self.width / 2 - 30, self.height - 250))

                clicks = pygame.mouse.get_pressed()
                if clicks[0]:
                    pygame.draw.circle(screen, self.lasers[level - 1], mouse_pos, 5)