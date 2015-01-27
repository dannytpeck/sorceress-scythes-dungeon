"""
   Scythe's Secrets (Working Title)
   By Danny Peck dannytpeck@gmail.com
   https://github.com/dannytpeck/scythes-secrets

   Main Game File
"""

import pygame, pytmx, pyscroll, os.path, sys

sys.path.append("classes")

import spritesheet

from pyscroll.util import PyscrollGroup
from pygame.locals import *


# define configuration variables here
RESOURCES_DIR = 'data'

PLAYER_MOVE_SPEED = 200            # pixels per second
MAP_FILENAME = 'hedgemaze.tmx'

# used for 2x scaling
temp_surface = None

# simple wrapper to keep the screen resizeable
def init_screen(width, height):
    global temp_surface
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    temp_surface = pygame.Surface((width / 2, height / 2)).convert()
    return screen

# make loading maps a little easier
def get_map(filename):
    return os.path.join(RESOURCES_DIR, filename)

# make loading images a little easier
def load_image(filename):
    return pygame.image.load(os.path.join(RESOURCES_DIR, filename))


class Player(pygame.sprite.Sprite):
	""" Our Player Character

	The Player Character has three collision rects, one for the whole sprite "rect" and
	"old_rect", and another to check collisions with walls, called "feet".

	The position list is used because pygame rects are inaccurate for
	positioning sprites; because the values they get are 'rounded down' to
	as integers, the sprite would move faster moving left or up.

	Feet is 1/2 as wide as the normal rect, and 8 pixels tall.  This size size
	allows the top of the sprite to overlap walls.

	There is also an old_rect that is used to reposition the sprite if it
	collides with level walls.
	"""
	# This holds the walk animation images for the player.
	walking_frames_l = []
	walking_frames_r = []
	walking_frames_u = []
	walking_frames_d = []	

	# Player facing direction defaults to right.
	direction = "R"

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.velocity = [0, 0]
		self._position = [0, 0]
		self._old_position = self.position

		# Choose a sprite sheet to use
		sprite_sheet = spritesheet.SpriteSheet("player.png")

		SPRITEHEIGHT = 32
		SPRITEWIDTH = 32
	
		# Load all the down facing images into a list
		image = sprite_sheet.get_image(0, 0, SPRITEWIDTH, SPRITEHEIGHT)
		self.walking_frames_d.append(image)
		image = sprite_sheet.get_image(SPRITEWIDTH, 0, SPRITEWIDTH, SPRITEHEIGHT)
		self.walking_frames_d.append(image)
		image = sprite_sheet.get_image(SPRITEWIDTH*2, 0, SPRITEWIDTH, SPRITEHEIGHT)
		self.walking_frames_d.append(image)

		# Load all the left facing images into a list
		image = sprite_sheet.get_image(0, SPRITEHEIGHT, SPRITEWIDTH, SPRITEHEIGHT)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(SPRITEWIDTH, SPRITEHEIGHT, SPRITEWIDTH, SPRITEHEIGHT)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(SPRITEWIDTH*2, SPRITEHEIGHT, SPRITEWIDTH, SPRITEHEIGHT)
		self.walking_frames_l.append(image)

		# Load all the right facing images into a list
		image = sprite_sheet.get_image(0, SPRITEHEIGHT*2, SPRITEWIDTH, SPRITEHEIGHT)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(SPRITEWIDTH, SPRITEHEIGHT*2, SPRITEWIDTH, SPRITEHEIGHT)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(SPRITEWIDTH*2, SPRITEHEIGHT*2, SPRITEWIDTH, SPRITEHEIGHT)
		self.walking_frames_r.append(image)

		# Load all the up facing images into a list
		image = sprite_sheet.get_image(0, SPRITEHEIGHT*3, SPRITEWIDTH, SPRITEHEIGHT)
		self.walking_frames_u.append(image)
		image = sprite_sheet.get_image(SPRITEWIDTH, SPRITEHEIGHT*3, SPRITEWIDTH, SPRITEHEIGHT)
		self.walking_frames_u.append(image)
		image = sprite_sheet.get_image(SPRITEWIDTH*2, SPRITEHEIGHT*3, SPRITEWIDTH, SPRITEHEIGHT)
		self.walking_frames_u.append(image)		

		# Set the image the player starts with (right by default)
		self.image = self.walking_frames_r[0]			

		self.rect = self.image.get_rect()
		self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)
		
	@property
	def position(self):
		return list(self._position)

	@position.setter
	def position(self, value):
		self._position = list(value)

	def update(self, dt):
		self._old_position = self._position[:]
		self._position[0] += self.velocity[0] * dt
		self._position[1] += self.velocity[1] * dt
		self.rect.topleft = self._position
		self.feet.midbottom = self.rect.midbottom

		'''# Cycle through the walking animation
		if self.velocity[0] == 0 and self.velocity[1]:
			if self.velocity[1] < 0:
				self.direction = "U"
			else:
				self.direction = "D"
				
		if self.velocity[1] == 0 and self.velocity[0]:
			if self.velocity[0] < 0:
				self.direction = "L"
			else:
				self.direction = "R"						
		'''
		
		if self.direction == "U" or self.direction == "D":
			pos = self.rect.y
		else:
			pos = self.rect.x	
	
		if self.direction == "U":
			frame = (pos // 30) % len(self.walking_frames_u)
			self.image = self.walking_frames_u[frame]		
		if self.direction == "D":
			frame = (pos // 30) % len(self.walking_frames_d)
			self.image = self.walking_frames_d[frame]			
		if self.direction == "L":
			frame = (pos // 30) % len(self.walking_frames_l)
			self.image = self.walking_frames_l[frame]      
		if self.direction == "R":
			frame = (pos // 30) % len(self.walking_frames_r)
			self.image = self.walking_frames_r[frame]	

	def move_back(self, dt):
		""" If called after an update, the sprite can move back
		"""
		self._position = self._old_position
		self.rect.topleft = self._position
		self.feet.midbottom = self.rect.midbottom

class Game(object):
    """ This class is a basic game.

    This class will load data, create a pyscroll group, a player object.
    It also reads input and moves the Player around the map.
    Finally, it uses a pyscroll group to render the map and Player.
    """
    filename = get_map(MAP_FILENAME)

    def __init__(self):

        # true while running
        self.running = False

        # load data from pytmx
        tmx_data = pytmx.load_pygame(self.filename)

        # setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = list()
        for object in tmx_data.objects:
            self.walls.append(pygame.Rect(
                object.x, object.y,
                object.width, object.height))

        # create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)

        w, h = screen.get_size()

        # create new renderer (camera)
        # clamp_camera is used to prevent the map from scrolling past the edge
        self.map_layer = pyscroll.BufferedRenderer(map_data, (w/2, h/2), clamp_camera=True)

        # pyscroll supports layered rendering.  our map has 3 'under' layers
        # layers begin with 0, so the layers are 0, 1, and 2.
        # since we want the sprite to be on top of layer 1, we set the default
        # layer for sprites as 1
        self.group = pyscroll.util.PyscrollGroup(map_layer=self.map_layer, default_layer=2)
		
        self.player = Player()

        # put the player in the center of the map
        self.player.position = self.map_layer.rect.center

        # add our player to the group
        self.group.add(self.player)

    def draw(self, surface):

        # center the map/screen on our Player
        self.group.center(self.player.rect.center)

        # draw the map and all sprites
        self.group.draw(surface)

    def handle_input(self):
        """ Handle pygame input events
        """
        event = pygame.event.poll()
        while event:
            if event.type == QUIT:
                self.running = False
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    break

            # this will be handled if the window is resized
            elif event.type == VIDEORESIZE:
                init_screen(event.w, event.h)
                self.map_layer.set_size((event.w / 2, event.h / 2))

            event = pygame.event.poll()

        # using get_pressed is slightly less accurate than testing for events
        # but is much easier to use.
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            self.player.velocity[1] = -PLAYER_MOVE_SPEED
            self.player.direction = "U"
        elif pressed[K_DOWN]:
            self.player.velocity[1] = PLAYER_MOVE_SPEED
            self.player.direction = "D"
        else:
            self.player.velocity[1] = 0

        if pressed[K_LEFT]:
            self.player.velocity[0] = -PLAYER_MOVE_SPEED
            self.player.direction = "L"
        elif pressed[K_RIGHT]:
            self.player.velocity[0] = PLAYER_MOVE_SPEED
            self.player.direction = "R"
        else:
            self.player.velocity[0] = 0

    def update(self, dt):
        """ Tasks that occur over time should be handled here
        """
        self.group.update(dt)

        # check if the sprite's feet are colliding with wall
        # sprite must have a rect called feet, and move_back method,
        # otherwise this will fail
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back(dt)

    def run(self):
        """ Run the game loop
        """
        clock = pygame.time.Clock()
        fps = 60
        scale = pygame.transform.scale
        self.running = True

        try:
            while self.running:
                dt = clock.tick(fps) / 1000.

                self.handle_input()
                self.update(dt)
                self.draw(temp_surface)
                scale(temp_surface, screen.get_size(), screen)
                pygame.display.flip()

        except KeyboardInterrupt:
            self.running = False


if __name__ == "__main__":
    pygame.init()
    screen = init_screen(800, 600)
    pygame.display.set_caption("Scythe's Secrets")

    try:
        game = Game()
        game.run()
    except:
        pygame.quit()
        raise
