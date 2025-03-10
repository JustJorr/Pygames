import pygame
import random
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__ (self, groups, surf):
        super(). __init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (WIDTH_SCREEN / 2, HEIGHT_SCREEN - 55))
        self.direction = pygame.Vector2()
        self.speed = 300

        #laser cooldwown
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown_duration = 1000

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = (int(keys[pygame.K_d] or int(keys[pygame.K_RIGHT]))) - (int(keys[pygame.K_a] or int(keys[pygame.K_LEFT])))
        self.direction.y = (int(keys[pygame.K_s] or int(keys[pygame.K_DOWN]))) - (int(keys[pygame.K_w] or int(keys[pygame.K_UP])))
        self.direction = self.direction.normalize() if self.direction  else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super(). __init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0, WIDTH_SCREEN), random.randint(0, HEIGHT_SCREEN)))

class Laser(pygame.sprite.Sprite):
    def __init__ (self, surf, pos, groups):
        super(). __init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)


#general settings
pygame.init()
WIDTH_SCREEN,HEIGHT_SCREEN = 1280, 600
display_screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("dummy")
running = True
clock = pygame.time.Clock()


#Load the images
player_surf = pygame.image.load(join("5games-main", "space shooter", "images", "player.png")).convert_alpha()
laser_surf = pygame.image.load(join("5games-main", "space shooter", "images", "laser.png")).convert_alpha()
meteor_surf = pygame.image.load(join("5games-main", "space shooter", "images", "meteor.png")).convert_alpha()
star_surf = pygame.image.load(join("5games-main", "space shooter", "images", "star.png")).convert_alpha()


#sprites
all_sprites = pygame.sprite.Group()
laser_sprite = pygame.sprite.Group()
for _ in range(20):
    Star(all_sprites, star_surf)
Player(all_sprites, player_surf)


#while loop
while running:
    #frame rate 
    dt = clock.tick(30) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #updating
    all_sprites.update(dt)

    #draw
    display_screen.fill("darkblue")
    all_sprites.draw(display_screen)

    pygame.display.update()

pygame.quit()
