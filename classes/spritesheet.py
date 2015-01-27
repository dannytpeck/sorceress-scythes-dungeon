"""
   Scythe's Secrets (Working Title)
   By Danny Peck dannytpeck@gmail.com
   https://github.com/dannytpeck/scythes-secrets

   Spritesheet Loading File
"""

import pygame, os.path

MAGENTA = ( 255,   0, 255)

# define configuration variables here
RESOURCES_DIR = 'data'

# make loading images a little easier
def load_image(filename):
    return pygame.image.load(os.path.join(RESOURCES_DIR, filename))

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = load_image(file_name)

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger sprite sheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming magenta works as the transparent color
        image.set_colorkey(MAGENTA)

        # Return the image
        return image
