from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frames_index = "down", 0
        self.image = pygame.image.load(join("5games-main", "Vampire survivor", "images", "player", "down", "0.png")).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-65, -90)

        #movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def load_images(self):
        self.frames = {"up" : [], "down" : [], "right" : [], "left" : []}

        for state in self.frames.keys():
            for main_folder, sub_folder, file_names in walk(join("5games-main", "Vampire survivor", "images", "player", state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: name.split(".")[0]):
                        full_path = join(main_folder, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.direction.x > 0 : self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0 : self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0 : self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0 : self.hitbox_rect.bottom = sprite.rect.top

    def animate(self, dt):
        #get state
        if self.direction.x != 0:
            self.state = "right" if self.direction.x > 0 else "left"
        if self.direction.y != 0:
            self.state = "down" if self.direction.y > 0 else "up"

        #animate
        self.frames_index = self.frames_index + 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frames_index) % len(self.frames[self.state])]

    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt) 



