import random
from settings import *
from playerdummy import Player
from spritesdummy import *
from groupsdummy import AllSprites
from pytmx.util_pygame import load_pygame


class Game:
    def __init__(self):
        pygame.init()
        self.display_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dummy")
        self.clock = pygame.time.Clock()
        self.running = True

        #groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprite = pygame.sprite.Group()
        self.player = Player((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), self.all_sprites, self.collision_sprite)

    def setup(self):
        map = load_pygame(join("5games-main", "Vampire survivor", "data", "maps", "world.tmx"))

    def run(self):
        #while loop
        while self.running:
            #dt
            dt = self.clock.tick(30) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #updating
            self.all_sprites.update(dt)

            #drawing
            self.display_screen.fill("black")
            self.all_sprites.draw(self.display_screen)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
