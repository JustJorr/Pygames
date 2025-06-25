from settings import *

class Paddle(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        
        #image
        self.image = pg.Surface(SIZE['paddle'], pg.SRCALPHA)
        pg.draw.rect(self.image, COLORS["paddle"], pg.FRect((0,0), SIZE["paddle"]), 0, 10)
        # self.image.fill(COLORS["paddle"])

        #rect n move
        self.rect = self.image.get_frect(center= POS["player"])
        self.old_rect = self.rect.copy()
        self.direction = 0
        self.speed = SPEED["player"]

    def move(self, dt):
        self.rect.centery += self.direction * self.speed * dt
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom
        #self.rect.clamp_ip((0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)

class Player(Paddle):
    def __init__(self, groups):
        super().__init__(groups)

    def get_direction(self):
        keys = pg.key.get_pressed()
        self.direction = int(keys[pg.K_DOWN]) - int(keys[pg.K_UP])

class Opponent(Paddle):
    def __init__(self, groups, ball):
        super().__init__(groups)
        self.speed = SPEED["opponent"]
        self.rect.center = POS["opponent"]
        self.ball = ball

    def get_direction(self):
        # keys = pg.key.get_pressed()
        # self.direction = int(keys[pg.K_s]) - int(keys[pg.K_w])
        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1 
