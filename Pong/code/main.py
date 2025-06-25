from settings import * 
from player import *
from sprites import *
import json

class Game(pg.sprite.Sprite):
    def __init__(self):
        pg.init()
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption("Pong")
        self.clock = pg.time.Clock()
        self.running = True

        #groups
        self.all_sprites = pg.sprite.Group()
        self.paddle_sprites = pg.sprite.Group()

        #class
        self.player = Player((self.all_sprites,self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score)
        Opponent((self.all_sprites,self.paddle_sprites), self.ball)

        #score
        try:
            with open(join("Vampire survivor", "data", "score_txt")) as score_file:
                self.score = json.load(score_file)
        except:
            self.score = {"player": 0, "opponent": 0}
        self.font = pg.font.Font(None, 160)

    def display_score(self):
        #player
        player_surf = self.font.render(str(self.score["player"]), True, COLORS["bg detail"])
        player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2))
        self.display_surface.blit(player_surf, player_rect)

        #opponent
        opponent_surf = self.font.render(str(self.score["opponent"]), True, COLORS["bg detail"])
        opponent_rect = opponent_surf.get_frect(center = (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2))
        self.display_surface.blit(opponent_surf, opponent_rect)

        #line seperator
        pg.draw.line(self.display_surface, COLORS["bg detail"], (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 3)

    def update_score(self, side):
        self.score["player" if side == "player" else "opponent"] += 1

    def run(self):
        while self.running:
            dt = self.clock.tick(30) / 1000
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    with open(join("Vampire survivor", "data", "score_txt"), "w") as score_file:
                        json.dump(self.score, score_file)

            #updating
            self.all_sprites.update(dt)

            #drawing
            self.display_surface.fill(COLORS["bg"])
            self.all_sprites.draw(self.display_surface)
            self.display_score()
            pg.display.update()

        pg.quit()

if __name__ == "__main__":
    game = Game()
    game.run()