"""
   Scythe's Secrets (Working Title)
   By Danny Peck dannytpeck@gmail.com
   https://github.com/dannytpeck/scythes-secrets

   Dungeon Room File
"""

import random, pygame

# Global constants

# Colors
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
RED     = ( 255,   0,   0)
GREEN   = (   0, 255,   0)
BLUE    = (   0,   0, 255)
CYAN    = (   0, 255, 255)
MAGENTA = ( 255,   0, 255)
YELLOW  = ( 255, 255,   0)
CRIMSON = (  35,   0,   0)

# Screen dimensions
WINWIDTH  = 800
WINHEIGHT = 800

BLOCKSIZE = 64

ROWS = int(WINHEIGHT / BLOCKSIZE)
COLUMNS = int(WINWIDTH / BLOCKSIZE)

# Load graphics
pygame.init()

screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT)) # change to the real resolution

class Wall(pygame.sprite.Sprite):
	"""This class represents wall blocks in the dungeon"""

	# Build an array containing the Surface objects returned by pygame.image.load() 
	dark_brick_walls = [pygame.image.load('walls/brick_dark0.png').convert(),
						pygame.image.load('walls/brick_dark1.png').convert(),
						pygame.image.load('walls/brick_dark2.png').convert(),
						pygame.image.load('walls/brick_dark3.png').convert()]

	def __init__(self, x, y):
		""" Constructor function """

		# Call the parent's constructor
		super().__init__()

		# Set the appearance of the wall block
		wall_index = random.randint(0,3)
		wall_image = self.dark_brick_walls[wall_index]
		self.image = wall_image

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x		

class Loose_Block(pygame.sprite.Sprite):
	"""This class represents loose blocks in the dungeon"""

	# Build an array containing the Surface objects returned by pygame.image.load() 
	loose_blocks = [pygame.image.load('blocks/stone_dark0.png').convert()]

	def __init__(self, x, y):
		""" Constructor function """

		# Call the parent's constructor
		super().__init__()

		# Set the appearance of the wall block
		loose_block_index = 0
		loose_block_image = self.loose_blocks[loose_block_index]
		self.image = loose_block_image

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x	
		
class Floor(pygame.sprite.Sprite):
	"""This class represents floor blocks in the dungeon, which will display in the background"""

	# Build an array containing the Surface objects returned by pygame.image.load() 
	grey_dirt_floors = [pygame.image.load('floors/grey_dirt0.png').convert(),
						pygame.image.load('floors/grey_dirt1.png').convert(),
						pygame.image.load('floors/grey_dirt2.png').convert(),
						pygame.image.load('floors/grey_dirt3.png').convert(),
						pygame.image.load('floors/grey_dirt4.png').convert()]

	def __init__(self, x, y):
		""" Constructor function """

		# Call the parent's constructor
		super().__init__()

		# Set the appearance of the wall block
		floor_index = random.randint(0,4)
		floor_image = self.grey_dirt_floors[floor_index]
		self.image = floor_image

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x				
		
class Room(object):
	""" Base class for all rooms. """

	""" Each room has a list of wall and floor sprites """
	wall_list = None
	floor_list = None
	loose_block_list = None
	background = None
	background_image = None

	def __init__(self):
		""" Constructor, create our lists. """
		self.wall_list = pygame.sprite.Group()
		self.floor_list = pygame.sprite.Group()
		self.loose_block_list = pygame.sprite.Group()
		#self.grid = [[0 for x in range(ROWS)] for y in range(COLUMNS)]
		self.background = pygame.sprite.Sprite()
	
	def clear_room(self):
		wall_list = None


class Room1(Room):
	"""This class builds the first room"""
	def __init__(self):
		Room.__init__(self)
	
	def build_room(self):
		x = y = 0
		level = [
			"PPPPPPPPPPPPPPPPPPPPPPPPP",
			"P                       P",
			"P PPPPPPPPPPPPPPPPPPPPP P",
			"P P                   P P",
			"P P PPPPPPPPPPPPPPPPP P P",
			"P P P               P P P",
			"P P P PPPPPP PPPPPP P P P",
			"P P P P           P P P P",
			"P P P P           P P P P",
			"P P P P           P P P P",
			"P P P P           P P P P",
			"P P P P           P P P P",
			"P P P P           P P P P",
			"P P P P           P P P P",
			"P P P P           P P P P",
			"P P P               P P P",
			"P P   P           P   P P",
			"P PPPPP     L     PPPPP P",
			"P                       P",
			"P                       P",
			"P                       P",
			"P                       P",
			"P                       P",
			"P                       P",			
			"PPPPPPPPPPP   PPPPPPPPPPP",]

		# build the level
		for row in level:
			for col in row:			
				floor = Floor(x, y)
				self.floor_list.add(floor)
				if col == "P":
					wall = Wall(x, y)
					self.wall_list.add(wall)
				if col == "L":
					loose_block = Loose_Block(x, y)
					self.loose_block_list.add(loose_block)
				x += BLOCKSIZE
			y += BLOCKSIZE
			x = 0

			
class Room2(Room):
	"""This class builds the second room"""
	def __init__(self):
		Room.__init__(self)
	
	def build_room(self):
		x = y = 0
		level = [
			"PPPPPPPPPPP   PPPPPPPPPPP",
			"PPPPPPPPPPP   PPPPPPPPPPP",
			"P                       P",
			"P                       P",
			"P                       P",
			"P                       P",
			"P     PPPPPP PPPPPP     P",
			"P     P           P     P",
			"P     P           P     P",
			"P     P           P     P",
			"P     P           P     P",
			"P     P           P     P",
			"P     P           P     P",
			"P     P           P     P",
			"P     P           P     P",
			"P     P           P     P",
			"P     P           P     P",
			"P     P           P     P",
			"P     P           P     P",
			"P     PPPPPP PPPPPP     P",
			"P                       P",
			"P                       P",
			"P                       P",
			"P                       P",			
			"PPPPPPPPPPPPPPPPPPPPPPPPP",]

		# build the level
		for row in level:
			for col in row:			
				floor = Floor(x, y)
				self.floor_list.add(floor)
				if col == "P":
					wall = Wall(x, y)
					self.wall_list.add(wall)
				if col == "L":
					loose_block = Loose_Block(x, y)
					self.loose_block_list.add(loose_block)
				x += BLOCKSIZE
			y += BLOCKSIZE
			x = 0		