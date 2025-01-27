import pygame

class ResourceManager:
    @staticmethod
    def load_image(path, scale=None):
        try:
            image = pygame.image.load(path)
            return pygame.transform.scale(image, scale) if scale else image
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            return None

    @staticmethod
    def load_font(path, size):
        try:
            return pygame.font.Font(path, size)
        except pygame.error as e:
            print(f"Error loading font {path}: {e}")
            return pygame.font.Font(None, size)