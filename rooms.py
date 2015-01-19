import pygame

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
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 800

# 25 x 25 grid for drawing the room blocks
ROWS = 25
COLUMNS = 25

# Load graphics
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # change to the real resolution

class Wall(pygame.sprite.Sprite):
	"""This class represents walls in the dungeon"""

	def __init__(self, x, y, width, height, color):
		""" Constructor function """

		# Call the parent's constructor
		super().__init__()

		# Make a wall, of the size specified in the parameters
		self.image = pygame.Surface([width, height])
		self.image.fill(color)

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x

class Block(pygame.sprite.Sprite):
	"""This class represents blocks in the dungeon"""

	def __init__(self, x, y):
		""" Constructor function """

		# Call the parent's constructor
		super().__init__()

		# Set enemy to use wall image
		block_image = pygame.image.load("brick.png").convert()
		self.image = block_image

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x		
		
class Room(object):
	""" Base class for all rooms. """

	""" Each room has a list of walls, enemy sprites, and a grid """
	wall_list = None
	loose_wall_list = None
	enemy_sprites = None	
	grid = None
	background = None
	background_image = None
	
	def __init__(self):
		""" Constructor, create our lists. """
		self.wall_list = pygame.sprite.Group()
		self.loose_wall_list = pygame.sprite.Group()
		self.enemy_sprites = pygame.sprite.Group()
		self.grid = [[0 for x in range(ROWS)] for y in range(COLUMNS)]
		self.background = pygame.sprite.Sprite()
		
	def draw_grid(self):	
		""" This method places blocks anywhere a 1 and loose blocks anywhere a 2 is found in the grid. """
		loose_block_image = pygame.image.load("loosebrick.png").convert()
		
		for row in range(ROWS):
			for column in range(COLUMNS):
				if self.grid[row][column] == 2:
					block = Block(row * 32, column * 32)
					block.image = loose_block_image
					self.loose_wall_list.add(block)
				
				if self.grid[row][column] == 1:
					block = Block(row * 32, column * 32)
					self.wall_list.add(block)			

	def clear_room(self):
		wall_list = None
		enemy_sprites = None
		grid = None
	
# --- Dungeon Rooms ---	

class Room1(Room):
	"""This creates all the walls in room 1"""
	def __init__(self):
		Room.__init__(self)
		# Set up background image
		self.background_image = pygame.image.load("background.png").convert()
		self.background.image = self.background_image
		self.background.rect = self.background.image.get_rect()
		
		x = y = 0
		level = [
			"PPPPPPPPPPPPPPPPPPPPPPPPP",
			"P    P                  P",
			"P PP PPPPPPPPPPP PPPPPP P",
			"P P  P                P P",
			"P P PPP PPPPPPPPPPPPP P P",
			"P P P P         P   P P P",
			"P P P PPPPP P PPPPP P P P",
			"P P P       P       PPPPPP",
			"P P P       P       P   P",
			"P P P PPPPPPPPPPPPP P P P",
			"P P P             P P P P",
			"P P P PPPPPPPPPPPPP P P P",
			"P P P P     P       P P P",
			"P P PPP     P     P P P P",
			"P P P       P     P P P P",
			"P P P P           P P P  ",
			"P P P P           P P P P",
			"P P P P           P P P P",
			"P P P PPPPPPPPPPPPP P P P",
			"P P P        P      P P P",
			"P P PPPPPPPP P PPPPPP P P",
			"P P          P        P P",
			"P PPPPPPPPPPPPPPPPPPPPP P",
			"P           P           P",
			"PPPPPPPPPP  PPPPPPPPPPPPP",]

			# build the level
		for row in level:
			for col in row:
				if col == "P":
					block = Block(x, y)
					self.wall_list.add(block)			
				if col == "E":
					loose_block = Block(x, y)
					self.loose_wall_list.add(loose_block)
				x += 32
			y += 32
			x = 0		
					
class Room2(Room):
	"""This creates all the walls in room 2"""
	def __init__(self):
		Room.__init__(self)

		# Build walls
		for row in range(25):
			self.grid[row][0] = 1
			self.grid[row][24] = 1
			
		for column in range(11):
			self.grid[0][column] = 1
			self.grid[24][column] = 1		

		for column in range(14,25):
			self.grid[0][column] = 1
			self.grid[24][column] = 1	
		
		self.draw_grid()	
			

class Room3(Room):
	"""This creates all the walls in room 3"""
	def __init__(self):
		Room.__init__(self)

		# Build walls
		for row in range(25):
			self.grid[row][0] = 1
			self.grid[row][24] = 1
			
		for column in range(11):
			self.grid[0][column] = 1
			self.grid[24][column] = 1		

		for column in range(14,25):
			self.grid[0][column] = 1
			self.grid[24][column] = 1	
		
		self.draw_grid()	

		for x in range(100, 800, 100):
			for y in range(100, 800, 200):
				wall = Wall(x, y, 20, 50, RED)
				self.wall_list.add(wall)

class Room4(Room):
	"""This creates all the walls in room 4"""
	def __init__(self):
		Room.__init__(self)
 
		# Build walls
		for row in range(25):
			self.grid[row][0] = 1
			self.grid[row][24] = 1
			
		for column in range(11):
			self.grid[0][column] = 1
			self.grid[24][column] = 1		

		for column in range(14,25):
			self.grid[0][column] = 1
			self.grid[24][column] = 1	
		
		self.draw_grid()		

class Room5(Room):
	"""This creates all the walls in room 4"""
	def __init__(self):
		Room.__init__(self)

		# Build walls
		for row in range(25):
			self.grid[row][0] = 1

		for row in range(11):
			self.grid[row][24] = 1

		for row in range(14,25):
			self.grid[row][24] = 1	
			
		for column in range(25):
			self.grid[0][column] = 1
			self.grid[24][column] = 1		
        
		self.draw_grid()
			