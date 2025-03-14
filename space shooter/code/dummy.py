import pygame
import random
from os.path import join


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super(). __init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (WIDTH_SCREEN / 2, HEIGHT_SCREEN - 50))
        self.direction = pygame.Vector2()
        self.speed = 500

        #cooldown
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown_duration = 1000

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.can_shoot >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = (int(keys[pygame.K_RIGHT] or int(keys[pygame.K_d]))) - (int(keys[pygame.K_LEFT] or int(keys[pygame.K_a]))) 
        self.direction.y = (int(keys[pygame.K_DOWN] or int(keys[pygame.K_s]))) - (int(keys[pygame.K_UP] or int(keys[pygame.K_w]))) 
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        self.rect.clamp_ip((0,0, WIDTH_SCREEN, HEIGHT_SCREEN))

        recent_keys = pygame.key.get_just_pressed()
        if self.can_shoot and recent_keys[pygame.K_SPACE]:
            Laser((all_sprites, laser_sprite), self.rect.midtop, laser_surf)
            self.shoot_time = pygame.time.get_ticks()
            self.can_shoot = False

        self.laser_timer()

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0 :
            self.kill()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0, WIDTH_SCREEN), random.randint(0, HEIGHT_SCREEN)))

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf):
        super().__init__(groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5),1)
        self.speed = random.randint(100, 200)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 2500
        self.rotation = 0
        self.rotation_speed = random.randint(100, 300)

    def update(self, dt):
        self.rect.center += self.speed * self.direction * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, groups, pos, frames):
        super(). __init__(groups)
        self.frames = frames
        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frames_index += 20 * dt
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index) % len(self.frames)]
        else:
            self.kill()

def collision():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprite, True, pygame.sprite.collide_mask)
    if collision_sprites:
        player.kill()
        running = False

    for laser in laser_sprite:
        laser_collision = pygame.sprite.spritecollide(laser, meteor_sprite, True)
        if laser_collision:
            laser.kill()
            AnimatedExplosion(all_sprites, laser.rect.midtop, explosion_frames)


#general settings
pygame.init()
WIDTH_SCREEN, HEIGHT_SCREEN = 1280, 600
display_screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("Dummy")
clock = pygame.time.Clock()
running = True

#import 
player_surf = pygame.image.load(join("5games-main", "space shooter", "images", "player.png")).convert_alpha()
star_surf =  pygame.image.load(join("5games-main","space shooter","images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(join("5games-main", "space shooter", "images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(join("5games-main", "space shooter", "images", "laser.png")).convert_alpha()
explosion_frames = [pygame.image.load(join("5games-main", "space shooter", "images", "explosion", f"{i}.png")).convert_alpha() for i in range(21)]
font = pygame.font.Font(join('5games-main', 'space shooter', 'images', 'Oxanium-Bold.ttf'), 20)




#sprites
all_sprites = pygame.sprite.Group()
laser_sprite = pygame.sprite.Group()
meteor_sprite = pygame.sprite.Group()
for _ in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites, player_surf)


#meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)


#while true
while running:
    #frame rate
    dt = clock.tick(30) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == meteor_event:
            x, y = random.randint(0, WIDTH_SCREEN), random.randint(-200, -100)
            Meteor((all_sprites, meteor_sprite), (x,y), meteor_surf)

    #updating
    all_sprites.update(dt)
    collision()

    #drawing
    display_screen.fill("darkblue")
    all_sprites.draw(display_screen)

    pygame.display.update()

pygame.quit()
