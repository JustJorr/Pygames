import pygame
from os.path import join

#import 
player_surf = pygame.image.load(join("5games-main", "space shooter", "images", "player.png")).convert_alpha()
star_surf =  pygame.image.load(join("5games-main","space shooter","images", "star.png")).convert_alpha()
meteor_surf = pygame.image.load(join("5games-main", "space shooter", "images", "meteor.png")).convert_alpha()
laser_surf = pygame.image.load(join("5games-main", "space shooter", "images", "laser.png")).convert_alpha()
explosion_frames = [pygame.image.load(join("5games-main", "space shooter", "images", "explosion", f"{i}.png")).convert_alpha() for i in range(21)]
font = pygame.font.Font(join('5games-main', 'space shooter', 'images', 'Oxanium-Bold.ttf'), 20)

#sounds
laser_sound = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "laser.wav"))
damage_sound = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "damage.ogg"))
game_music = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "game_music.wav"))
explosion_sound = pygame.mixer.Sound(join("5games-main", "space shooter", "audio", "explosion.wav"))
laser_sound.set_volume(0.5)
game_music.set_volume(0.5)
game_music.play(loops= 5)
