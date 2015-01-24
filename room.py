"""
   Scythe's Secrets (Working Title)
   By Danny Peck dannytpeck@gmail.com
   https://github.com/dannytpeck/scythes-secrets

   Dungeon Room File
"""

import random, pygame

from constants import *

# Load graphics
pygame.init()
screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

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

class LooseBlock(pygame.sprite.Sprite):
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

	#""" Each room has a list of wall and floor sprites """
	#wall_list = None
	#floor_list = None
	#loose_block_list = None
	#TOTAL_LEVEL_WIDTH = 0
	#TOTAL_LEVEL_HEIGHT = 0
	#background = None
	#background_image = None

	def __init__(self):
		""" Constructor, create our lists. """
		self.wall_list = pygame.sprite.Group()
		self.floor_list = pygame.sprite.Group()
		self.loose_block_list = pygame.sprite.Group()

		self.total_width = 0
		self.total_height = 0
		self.rows = 0
		self.columns = 0
		
		self.level = ["PPP",
					  "P P",
					  "PPP"]

		#self.grid = [[0 for x in range(ROWS)] for y in range(COLUMNS)]
		#self.background = pygame.sprite.Sprite()

	def calculate_grid(self):
		self.rows = len(self.level)
		self.columns = len(self.level[0])
		self.total_width = self.columns * TILESIZE
		self.total_height = self.rows * TILESIZE
		#Sanity check
		print(self.total_width, self.total_height, self.rows, self.columns)
		
	def clear_room(self):
		wall_list = None


class Room1(Room):
	"""This class builds the first room"""
	def __init__(self):
		# Call the parent's constructor
		super().__init__()

		self.level = [
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

		self.calculate_grid()
		
	def build_room(self):
		x = y = 0

		# build the level
		for row in self.level:
			for col in row:			
				floor = Floor(x, y)
				self.floor_list.add(floor)
				if col == "P":
					wall = Wall(x, y)
					self.wall_list.add(wall)
				if col == "L":
					loose_block = LooseBlock(x, y)
					self.loose_block_list.add(loose_block)
				x += TILESIZE
			y += TILESIZE
			x = 0

			
class Room2(Room):
	"""This class builds the second room"""
	def __init__(self):
		Room.__init__(self)

		self.level = [
			"PPPPP   PPPPP",
			"P           P",
			"P           P",
			"P       PPPPP",
			"P           P",
			"P           P",
			"P           P",
			"PPPPP       P",
			"P           P",
			"P           P",
			"P           P",
			"P           P",
			"PPPPPPPPPPPPP",]

		self.calculate_grid()	
		
	def build_room(self):
		x = y = 0
		
		# build the level
		for row in self.level:
			for col in row:			
				floor = Floor(x, y)
				self.floor_list.add(floor)
				if col == "P":
					wall = Wall(x, y)
					self.wall_list.add(wall)
				if col == "L":
					loose_block = Loose_Block(x, y)
					self.loose_block_list.add(loose_block)
				x += TILESIZE
			y += TILESIZE
			x = 0		
