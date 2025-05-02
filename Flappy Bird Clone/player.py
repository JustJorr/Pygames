from Settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, groups, pos):
        super(). __init__(groups)
        self.image = pg.image.load(join("5games-main", "Flappy Bird Clone", "image", "pngwing.com.png")).convert_alpha()
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_frect(center = pos)

        #direction and speed
        self.direction = pg.Vector2(0, 0)
        self.speed = 12
        self.gravity = -0.5

    def input(self):
        self.rect.clamp_ip((0,0, WINDOW_WIDTH, WINDOW_HEIGHT))
        keys = pg.key.get_just_pressed()
        if keys[pg.K_SPACE]:
            self.direction.x += 1
            self.direction.y = self.speed
        else:
            self.direction.x += 1
            self.direction.y += self.gravity
            print(self.direction.x)

    def move(self, dt):
        self.rect.centerx += self.direction.x * dt
        self.rect.centery += -self.direction.y * self.speed * dt
        if self.direction.x >= 15:
            self.direction.x = 15

    def update(self, dt):
        self.input()
        self.move(dt)

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x + camera_x, self.rect.y))
