import pygame
from os.path import join

# Load the images
player_surf = pygame.image.load(join("5games-main", "space shooter", "images", "player.png")).convert_alpha()
laser_surf = pygame.image.load(join("5games-main", "space shooter", "images", "laser.png")).convert_alpha()
meteor_surf = pygame.image.load(join("5games-main", "space shooter", "images", "meteor.png")).convert_alpha()
star_surf = pygame.image.load(join("5games-main", "space shooter", "images", "star.png")).convert_alpha()

# Create a dictionary to store the images
images = {
    "player": player_surf,
    "laser": laser_surf,
    "meteor": meteor_surf,
    "star": star_surf
}