import pygame
import random
from os.path import join

#Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.original_surf = pygame.image.load(join("5games-main","space shooter","images", "player.png")).convert_alpha()
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = (LEBAR_LAYAR / 2, PANJANG_LAYAR / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldwon_direction = 400

        #mask
        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldwon_direction:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = (int(keys[pygame.K_RIGHT]) or int(keys[pygame.K_d])) - (int(keys[pygame.K_LEFT]) or int(keys[pygame.K_a]))
        self.direction.y = (int(keys[pygame.K_DOWN]) or int(keys[pygame.K_s])) - (int(keys[pygame.K_UP]) or int(keys[pygame.K_w]))
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        self.rect.clamp_ip((0, 0, LEBAR_LAYAR, PANJANG_LAYAR))

        recent_keys = pygame.key.get_just_pressed() 
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0, LEBAR_LAYAR), random.randint(0, PANJANG_LAYAR)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 10000
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5),1)
        self.speed = random.randint(100,200)
        self.rotation_speed = random.randint(20, 100)
        self.rotation = 0

        #mask
        #meteor_mask = pygame.mask.from_surface(self.image)
        #meteor_mask_surf = meteor_mask.to_surface()
        #self.image = meteor_mask_surf

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index) % len(self.frames)]
        else:
            self.kill()

def collisons():
    global running

    collision_sprites =  pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

def display_score():
    current_time = pygame.time.get_ticks() // 1000
    text_surf = font.render(str(current_time), True, ("white"))
    text_rect = text_surf.get_frect(midbottom = (LEBAR_LAYAR / 2, PANJANG_LAYAR - 50))
    layar.blit(text_surf, text_rect)
    pygame.draw.rect(layar, ("white"), text_rect.inflate(20,30).move(0,-3), 5, 10)


#general setup
pygame.init()
LEBAR_LAYAR, PANJANG_LAYAR = 1280, 640
layar = pygame.display.set_mode((LEBAR_LAYAR,PANJANG_LAYAR))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()

#import 
star_surf =  pygame.image.load(join("5games-main","space shooter","images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(join("5games-main", "space shooter", "images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(join("5games-main", "space shooter", "images", "laser.png")).convert_alpha()
font = pygame.font.Font(join('5games-main', 'space shooter', 'images', 'Oxanium-Bold.ttf'), 20)
explosion_frames = [pygame.image.load(join("5games-main", "space shooter", "images", "explosion", f"{i}.png")).convert_alpha() for i in range(21)]


#sounds
laser_sound = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "laser.wav"))
laser_sound.set_volume(0.5)
damage_sound = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "damage.ogg"))
game_music = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "game_music.wav"))
explosion_sound = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "explosion.wav"))
game_music.set_volume(0.5)
game_music.play(loops= 5)


#sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for _ in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


#Meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick(30) / 1000 
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = random.randint(0, LEBAR_LAYAR), random.randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

    #update
    all_sprites.update(dt)
    collisons()

    #draw the game
    layar.fill("darkblue")
    all_sprites.draw(layar)
    display_score()

    pygame.display.update()

pygame.quit()