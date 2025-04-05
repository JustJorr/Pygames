import pygame.time
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
        self.all_sprites = AllSprites()
        self.collision_sprite = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        #gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown_duration = 300

        #enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 1000)
        self.spawn_positions = []

        #setup
        self.setup()
        self.load_images()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join("5games-main", "Vampire survivor", "images", "gun", "bullet.png")).convert_alpha()

        folders = list(walk(join("5games-main", "Vampire survivor", "images", "enemies")))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join("5games-main", "Vampire survivor", "images", "enemies", folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key=lambda name: int(name.split(".")[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

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
            else:
                self.spawn_positions.append([obj.x, obj.y])

    def bullet_collision(self):
        if self.bullet_sprites:
            for sprite in self.bullet_sprites:
                bullet_collision = pygame.sprite.spritecollide(sprite, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if bullet_collision:
                    sprite.kill()
                    for sprite in bullet_collision:
                        sprite.destroy()

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.player.kill()

    def run(self):
        #while loop
        while self.running:
            #dt
            dt = self.clock.tick(30) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy((self.all_sprites, self.enemy_sprites), random.choice(self.spawn_positions), self.collision_sprite, random.choice(list(self.enemy_frames.values())), self.player)

            #updating
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()

            #drawing
            self.display_screen.fill("black")
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
