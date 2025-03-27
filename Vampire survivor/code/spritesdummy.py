from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, groups, pos, size):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill("blue")
        self.rect = self.image.get_frect(center = pos)
