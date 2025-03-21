from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, pos, collision_sprites):
        super(). __init__(groups)
        self.image = pygame.image.load(join("5games-main", "Vampire survivor", "images", "player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-40, 0)

        #movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.clamp_ip((0,0, WINDOW_WIDTH, WINDOW_HEIGHT))

    def move(self, dt):
        self.direction.x += self.direction.y * self.speed * dt
        self.collision("horizontal")
        self.direction.y += self.direction.y * self.speed * dt
        self.collision("vertical")

    def collision(self, direction):
        for sprite in self.collision_sprite:
            if sprite.collision(self.rect):
                if direction == "horizontal":
                    if self.direction.x > 0 : self.rect.right = sprite.rect.left
                    if self.direction.x < 0 : self.rect.left = sprite.rect.right
                else:
                    if self.direction.x > 0 : self.rect.bottom = sprite.rect.top
                    if self.direction.x < 0 : self.rect.top = sprite.rect.bottom

    def update(self, dt):
        self.input()
        self.move(dt)
