from settings import *
from player import Player
from sprites import *
import random


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivor")
        self.running = True
        self.clock = pygame.time.Clock()

        #groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprite = pygame.sprite.Group()

        #sprites
        self.player = Player(self.all_sprites, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), self.collision_sprite)
        for _ in range(10):
            x, y = random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)
            w,h = random.randint(60, 100), random.randint(50, 100)
            CollisionSprite((x,y), (w,h), (self.all_sprites, self.collision_sprite))

    def run(self):
        while self.running:
            #dt
            dt = self.clock.tick(30) / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #update
            self.all_sprites.update(dt)

            #draw
            self.display_surface.fill("black")
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
