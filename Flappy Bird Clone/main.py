from Settings import *
from player import Player
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.display_screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption("Flappy Bird Clone")
        self.running = True
        self.clock = pg.time.Clock()

        #background
        self.image_background = pg.image.load(join("5games-main", "Flappy Bird Clone", "image", "Flappy bird bg.jpg")).convert_alpha()
        self.image_background = pg.transform.scale(self.image_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.pipes_surf = pg.image.load(join("5games-main", "Flappy Bird Clone", "image", "pipes.png")).convert_alpha()
        self.pipes_surf = pg.transform.scale(self.pipes_surf, (100, 250))

        #groups
        self.all_sprites = pg.sprite.Group()
        self.pipes = pg.sprite.Group()

        #sprites
        self.player = Player(self.all_sprites, (50, 500))

        #pipes timer
        self.pipe_event = pg.event.custom_type()
        pg.time.set_timer(self.pipe_event, random.randint(1000, 10000))

        #camera
        self.camera_x = 0

    def run(self):
        while self.running:
            dt = self.clock.tick(30) / 1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == self.pipe_event:
                    Pipes((self.all_sprites, self.pipes), self.pipes_surf, (WINDOW_WIDTH + 100, 470))

            #update
            self.all_sprites.update(dt)
            self.camera_x -= 0.5

            #draw
            self.display_screen.blit(self.image_background, (self.camera_x, 0))
            for sprite in self.all_sprites:
                sprite.draw(self.display_screen, self.camera_x)
            pg.display.update()

            # reset the camera if it has moved off the screen
            if self.camera_x < -WINDOW_WIDTH:
                self.camera_x = 0

        pg.quit()

if __name__ == "__main__":
    game = Game()
    game.run()