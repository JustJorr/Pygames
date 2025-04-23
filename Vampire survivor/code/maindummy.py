from settings import *
from playerdummy import Player
from spritesdummy import *
from groupsdummy import AllSprites
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Dummy")
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_state = "playing"

        #cooldown gun
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown = 300

        #groups
        self.all_sprites = AllSprites()
        self.collison_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        #enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 1000)
        self.spawn_positions = []

        #lives
        self.lives = 3
        self.heart_surf = pygame.image.load(join("5games-main", "Vampire survivor", "images", "gun" ,"gun.png")).convert_alpha()
        self.heart_rect = self.heart_surf.get_frect()
        
        # Player invulnerability
        self.player_invulnerable = False
        self.invulnerability_time = 0
        self.invulnerability_duration = 3000  

        #setup
        self.load_images()
        self.setup()

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
            pos = self.gun.rect.center + self.gun.player_direction * 80
            Bullet((self.all_sprites, self.bullet_sprites), self.bullet_surf, pos, self.gun.player_direction)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def bullet_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown:
                self.can_shoot = True

    def invulnerability_timer(self):
        if self.player_invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerability_time >= self.invulnerability_duration:
                self.player_invulnerable = False

                # Reset player visibility
                self.player.image.set_alpha(255)

    def setup(self):
        map = load_pygame(join("5games-main", "Vampire survivor", "data", "maps", "world.tmx"))

        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite(self.all_sprites, image, (x * TILE_SIZE, y * TILE_SIZE))

        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite((self.all_sprites, self.collison_sprites), obj.image, (obj.x, obj.y))

        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprite(self.collison_sprites, pygame.Surface((obj.width, obj.height)), (obj.x, obj.y))

        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player(self.all_sprites, (obj.x, obj.y), self.collison_sprites)
                self.gun = Gun(self.all_sprites, self.player)
            else:
                self.spawn_positions.append([obj.x, obj.y])

    def draw_lives(self):
        for i in range(self.lives):
            self.heart_rect.x = 10 + i * (self.heart_rect.width + 5)
            self.heart_rect.y = 10
            self.screen.blit(self.heart_surf, self.heart_rect)

    def player_collision(self):
        # Only check for collisions if player is not invulnerable
        if not self.player_invulnerable:
            if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
                self.lives -= 1
                if self.lives > 0:
                    # Make player invulnerable
                    self.player_invulnerable = True
                    self.invulnerability_time = pygame.time.get_ticks()
                    # Make player slightly transparent to show invulnerability
                    self.player.image.set_alpha(150)
                else:
                    self.game_state = "game_over"

    def bullet_collision(self):
        if self.bullet_sprites:
            for sprite in self.bullet_sprites:
                bullet_collision = pygame.sprite.spritecollide(sprite, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if bullet_collision:
                    sprite.kill()
                    for sprite in bullet_collision:
                        sprite.destroy()

    def run(self):
        while self.running:
            dt = self.clock.tick(30) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy((self.all_sprites, self.enemy_sprites), random.choice(self.spawn_positions), self.collison_sprites, self.player, random.choice(list(self.enemy_frames.values())))

            #updating
            if self.game_state == "playing":
                self.all_sprites.update(dt)
                self.input()
                self.bullet_timer()
                self.invulnerability_timer() 
                self.player_collision()
                self.bullet_collision()

            #drawing
            if self.game_state == "playing":
                self.screen.fill("black")
                self.all_sprites.draw(self.player.rect.center)
                self.draw_lives()
                pygame.display.update()

            elif self.game_state == "game_over":
                self.screen.fill("black")
                font = pygame.font.Font(join('5games-main', 'space shooter', 'images', 'Oxanium-Bold.ttf'), 20)
                text_surf = font.render("You Died", True, ("red"))
                text_rect = text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
                self.screen.blit(text_surf, text_rect)
                pygame.draw.rect(self.screen, ("black"), text_rect.inflate(20, 10), 3, 10)
                pygame.display.update()
                pygame.time.wait(2000)
                self.running = False

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
