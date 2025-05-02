import random
from Settings import *

class Pipes(pg.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.speed = 2

    def update(self, dt):
        self.rect.x -= self.speed

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x + camera_x, self.rect.y))