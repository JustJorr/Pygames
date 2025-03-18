import pygame
import random
from os.path import join


#classes
class Player(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super(). __init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (WIDTH_SCREEN / 2, HEIGHT_SCREEN - 55))
        self.direction = pygame.Vector2()
        self.speed = 500

        #cooldown laser
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown_duration = 1000

    def event_item(self):
        self.speed += 500

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = (int(keys[pygame.K_RIGHT] or int(keys[pygame.K_d]))) - (int(keys[pygame.K_LEFT] or int(keys[pygame.K_a])))
        self.direction.y = (int(keys[pygame.K_DOWN] or int(keys[pygame.K_s]))) - (int(keys[pygame.K_UP] or int(keys[pygame.K_w])))
        self.rect.center += self.direction * self.speed * dt
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.clamp_ip((0,0, WIDTH_SCREEN, HEIGHT_SCREEN))

        recent_keys = pygame.key.get_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites, laser_sprite), laser_surf, self.rect.midtop)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

        self.laser_timer()


class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super(). __init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        laser_sound.play()

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0, WIDTH_SCREEN), random.randint(0, HEIGHT_SCREEN)))


class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.original_image = surf
        self.image = self.original_image
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(100, 200)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 4500

        #rotation
        self.rotation = 0
        self.rotation_speed = random.randint(100, 150)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)


class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, groups, frames, pos):
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


class EventItem(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super(). __init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.rect.centery += 100 * dt
        if self.rect.top > HEIGHT_SCREEN:
            self.kill()


def collision():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprite, True, pygame.sprite.collide_mask)
    if collision_sprites :
        player.kill()
        explosion_sound.play()

    for item in event_item_sprite:
        item_collision = pygame.sprite.collide_mask(player, item)
        if item_collision:
            player.event_item()
            item.kill()

    for laser in laser_sprite:
        laser_collision = pygame.sprite.spritecollide(laser, meteor_sprite, True)
        if laser_collision:
            laser.kill()
            AnimatedExplosion(all_sprites, explosion_frames, laser.rect.midtop)
            explosion_sound.play()



def display_score():
    current_time = pygame.time.get_ticks() // 1000
    text_surf = font.render(str(current_time), True, ("white"))
    text_rect = text_surf.get_frect(center = (50, 50))
    display_screen.blit(text_surf, text_rect)
    pygame.draw.rect(display_screen, ("black"), text_rect.inflate(30, 20).move(0, -5), 5, 10)


#general settings
pygame.init()
WIDTH_SCREEN, HEIGHT_SCREEN = 1280, 600
display_screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("dummy")
clock = pygame.time.Clock()
running = True


#import 
player_surf = pygame.image.load(join("5games-main", "space shooter", "images", "player.png")).convert_alpha()
star_surf =  pygame.image.load(join("5games-main","space shooter","images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(join("5games-main", "space shooter", "images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(join("5games-main", "space shooter", "images", "laser.png")).convert_alpha()
event_item_surf = pygame.image.load(join("5games-main", "space shooter", "Craftpix", "PNG", "Bonus_Items", "Hero_Movement_Debuff.png")).convert_alpha()
event_item_surf = pygame.transform.smoothscale(event_item_surf, (50,50))
explosion_frames = [pygame.image.load(join("5games-main", "space shooter", "images", "explosion", f"{i}.png")).convert_alpha() for i in range(21)]
font = pygame.font.Font(join('5games-main', 'space shooter', 'images', 'Oxanium-Bold.ttf'), 40)


#sounds
laser_sound = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "laser.wav"))
damage_sound = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "damage.ogg"))
game_music = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "game_music.wav"))
explosion_sound = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "explosion.wav"))
laser_sound.set_volume(0.5)
game_music.set_volume(0.5)
game_music.play(loops= 5)


#sprites
all_sprites = pygame.sprite.Group()
laser_sprite = pygame.sprite.Group()
meteor_sprite = pygame.sprite.Group()
event_item_sprite = pygame.sprite.Group()
for _ in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites, player_surf)


#meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)


#bonus item event
event_item = pygame.event.custom_type()
pygame.time.set_timer(event_item, 10000)


#while loop
while running:
    #frame rate
    dt = clock.tick(30) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == meteor_event:
            x, y = random.randint(0, HEIGHT_SCREEN), random.randint(-100, -50)
            Meteor((all_sprites, meteor_sprite), meteor_surf, (x, y))

        if event.type == event_item:
            x, y = random.randint(0, WIDTH_SCREEN), random.randint(-100, 50)
            EventItem((all_sprites, event_item_sprite), event_item_surf, (x, y))

    #updating
    all_sprites.update(dt)
    collision()

    #drawing
    display_screen.fill("darkblue")
    all_sprites.draw(display_screen)
    display_score()

    pygame.display.update()

pygame.quit()
