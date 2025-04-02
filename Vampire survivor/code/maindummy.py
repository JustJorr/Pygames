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
        self.all_sprites = AllSprites()
        self.collision_sprite = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        #gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown_duration = 300

        #setup
        self.setup()
        self.load_images()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join("5games-main", "Vampire survivor", "images", "gun", "bullet.png")).convert_alpha()

    def input(self):
        if pygame.mouse.get_just_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet((self.all_sprites, self.bullet_sprites), self.bullet_surf, pos, self.gun.player_direction)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def setup(self):
        map = load_pygame(join("5games-main", "Vampire survivor", "data", "maps", "world.tmx"))

        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite(self.all_sprites, (x * TILE_SIZE, y * TILE_SIZE), image)

        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite((self.all_sprites, self.collision_sprite), (obj.x, obj.y), obj.image)

        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprite(self.collision_sprite, (obj.x, obj.y), pygame.Surface((obj.width, obj.height)))

        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprite)
                self.gun = Gun(self.player, self.all_sprites)

    def run(self):
        #while loop
        while self.running:
            #dt
            dt = self.clock.tick(30) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #updating
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)

            #drawing
            self.display_screen.fill("black")
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
