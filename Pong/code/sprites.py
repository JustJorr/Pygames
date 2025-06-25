from settings import *
import random

class Ball(pg.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, update_score):
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites
        self.update_score = update_score

        #image
        self.image = pg.Surface(SIZE['ball'], pg.SRCALPHA)
        pg.draw.circle(self.image, COLORS['ball'], (SIZE["ball"][0] / 2, SIZE["ball"][1] / 2), SIZE["ball"][0] / 2)

        #rect n move
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.old_rect = self.rect.copy()
        self.direction = pg.Vector2(random.choice((1,-1)),random.uniform(0.7,0.8) * random.choice((-1, 1)))
        self.speed_modifier = 0

        #timer
        self.start_time = pg.time.get_ticks()
        self.duration = 1200

    def move(self, dt):
        self.rect.x += self.direction.x * SPEED["ball"] * dt * self.speed_modifier
        self.collision("horizontal")
        self.rect.y += self.direction.y * SPEED["ball"] * dt * self.speed_modifier
        self.collision("vertical")
        # if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
        #     self.direction.x *= -1
        # if self.rect.top < 0 or self.rect.bottom > WINDOW_HEIGHT:
        #     self.direction.y *= -1

    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.rect.right > sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1

                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= self.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1

    def wall_collision(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1

        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1

        if self.rect.right >= WINDOW_WIDTH or self.rect.left <= 0:
            self.update_score("player" if self.rect.x < WINDOW_WIDTH / 2 else "opponent")
            self.reset()

    def reset(self):
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.direction = pg.Vector2(random.choice((1,-1)), random.uniform(0.7, 0.8) * random.choice((-1, 1)))
        self.start_time = pg.time.get_ticks()

    def timer(self):
        if pg.time.get_ticks() - self.start_time >= self.duration:
            self.speed_modifier = 1
        else:
            self.speed_modifier = 0

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.timer()
        self.move(dt)
        self.wall_collision()