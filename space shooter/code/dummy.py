import pygame as pg
import random
from os.path import join


#classes
class Player(pg.sprite.Sprite):
    def __init__(self, surf, groups):
        super(). __init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (WIDTH_SCREEN / 2, HEIGHT_SCREEN - 55))
        self.direction = pg.Vector2()
        self.speed = 400

        #laser_cooldown
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pg.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pg.key.get_pressed()
        self.direction.x = (int(keys[pg.K_RIGHT] or int(keys[pg.K_d]))) - (int(keys[pg.K_LEFT] or int(keys[pg.K_s])))
        self.direction.y = (int(keys[pg.K_DOWN] or int(keys[pg.K_s]))) - (int(keys[pg.K_UP] or int(keys[pg.K_w])))
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        self.rect.clamp_ip((0,0, WIDTH_SCREEN, HEIGHT_SCREEN))

        recent_keys = pg.key.get_just_pressed()
        if self.can_shoot and recent_keys[pg.K_SPACE]:
            Laser(self.rect.midtop, (laser_sprite, all_sprites), laser_surf)
            self.shoot_time = pg.time.get_ticks()
            self.can_shoot = False

        self.laser_timer()

class Laser(pg.sprite.Sprite):
    def __init__(self, pos, groups, surf):
        super(). __init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Star(pg.sprite.Sprite):
    def __init__(self, groups, surf):
        super(). __init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0, WIDTH_SCREEN), random.randint(0, HEIGHT_SCREEN)))

class Meteor(pg.sprite.Sprite):
    def __init__(self, pos, groups, surf):
        super().__init__(groups)
        self.orginial_surf = surf
        self.image = self.orginial_surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pg.time.get_ticks()
        self.lifetime = 2500
        self.direction = pg.Vector2(random.uniform(-0.5, 0.5),1)
        self.speed = random.randint(200, 500)
        self.rotation = 0
        self.rotation_speed = random.randint(100, 300)

    def update(self, dt):
        self.rect.center += self.speed * self.direction * dt
        if pg.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pg.transform.rotozoom(self.orginial_surf, self.rotation,1)
        self.rect = self.image.get_frect(center = self.rect.center)



#general settings
pg.init()
WIDTH_SCREEN, HEIGHT_SCREEN = 1280, 600
display_screen = pg.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pg.display.set_caption("Dummy")
clock = pg.time.Clock()
running = True


# Load the images
player_surf = pg.image.load(join("5games-main", "space shooter", "images", "player.png")).convert_alpha()
laser_surf = pg.image.load(join("5games-main", "space shooter", "images", "laser.png")).convert_alpha()
meteor_surf = pg.image.load(join("5games-main", "space shooter", "images", "meteor.png")).convert_alpha()
star_surf = pg.image.load(join("5games-main", "space shooter", "images", "star.png")).convert_alpha()


#sprites
all_sprites = pg.sprite.Group()
meteor_sprite = pg.sprite.Group()
laser_sprite = pg.sprite.Group()
for _ in range(20):
    Star(all_sprites, star_surf)
Player(player_surf, all_sprites)


#meteor event
meteor_event = pg.event.custom_type()
pg.time.set_timer(meteor_event, 500)


#while loop
while running:
    #frame rate
    dt = clock.tick(30) / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = random.randint(0, WIDTH_SCREEN), random.randint(-200, -100)
            Meteor((x, y), all_sprites, meteor_surf)

    #updating
    all_sprites.update(dt)

    #drawing
    display_screen.fill("darkblue")
    all_sprites.draw(display_screen)

    pg.display.update()

pg.quit()
