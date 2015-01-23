"""
   Scythe's Secrets (Working Title)
   By Danny Peck dannytpeck@gmail.com
   https://github.com/dannytpeck/scythes-secrets

   Player File
"""

import pygame

# Define some colors
BLACK = (  0,   0,   0)

class Player(pygame.sprite.Sprite):
	""" This class is for the player-controlled character. """

	# Set speed vector
	change_x = 0
	change_y = 0

	# This holds the walk animation images for the player.
	walking_frames_l = []
	walking_frames_r = []
	walking_frames_u = []
	walking_frames_d = []	

	# Player facing direction defaults to right.
	direction = "R"
	
	def __init__(self, x, y):
		""" Constructor function """

		# Call the parent's constructor
		super().__init__()

		# Set beginning mana to 5
		self.mana = 5
		
		# Choose a sprite sheet to use
		sprite_sheet = SpriteSheet("player.png")

		SPRITEHEIGHT = 60
		SPRITEWIDTH = 60
	
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

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		
		# Create rect for player sprite, set it to 28px x 28px
		# self.rect = pygame.Rect(x, y, 31, 31)
		
	# Player-controlled movement:
	speed = 5
	
	def go_left(self):
		""" Called when the user hits the left arrow. """
		self.change_x = -self.speed
		self.direction = "L"

	def go_right(self):
		""" Called when the user hits the right arrow. """
		self.change_x = self.speed
		self.direction = "R"

	def go_up(self):
		""" Called when the user hits the up arrow. """
		self.change_y = -self.speed
		self.direction = "U"		
		
	def go_down(self):
		""" Called when the user hits the down arrow. """
		self.change_y = self.speed
		self.direction = "D"

	def stop(self):
		""" Stops all movement """
		self.change_x = 0
		self.change_y = 0

	def move(self, room):
		""" Move the player. """
		
		# Move up/down
		self.rect.y += self.change_y

		# Did this update cause us to hit a wall?
		block_hit_list = pygame.sprite.spritecollide(self, room.wall_list, False)
		for block in block_hit_list:
			# Reset our position based on the top/bottom of the object.
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
			else:
				self.rect.top = block.rect.bottom
		block_hit_list = pygame.sprite.spritecollide(self, room.loose_block_list, False)
		for block in block_hit_list:
			# Reset our position based on the top/bottom of the object.
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
			else:
				self.rect.top = block.rect.bottom
				
		# Move left/right
		self.rect.x += self.change_x

		# Did this update cause us to hit a wall?
		block_hit_list = pygame.sprite.spritecollide(self, room.wall_list, False)
		for block in block_hit_list:
			# Reset our position based on the left/right of the object.
			if self.change_x > 0:
				self.rect.right = block.rect.left
			else:
				# Otherwise if we are moving left, do the opposite.
				self.rect.left = block.rect.right		
		block_hit_list = pygame.sprite.spritecollide(self, room.loose_block_list, False)
		for block in block_hit_list:
			# Reset our position based on the left/right of the object.
			if self.change_x > 0:
				self.rect.right = block.rect.left
			else:
				# Otherwise if we are moving left, do the opposite.
				self.rect.left = block.rect.right		

				
		# Cycle through the walking animation
		if self.change_x == 0 and self.change_y:
			if self.change_y < 0:
				self.direction = "U"
			else:
				self.direction = "D"
				
		if self.change_y == 0 and self.change_x:
			if self.change_x < 0:
				self.direction = "L"
			else:
				self.direction = "R"				

		# Kinda hack-y here, ideally find a better solution.
		if self.direction == "U" or self.direction == "D":
			if self.rect.top == 32 or self.rect.bottom == 768:
				pos = self.rect.x
			else:
				pos = self.rect.y
		else:
			if self.rect.left == 32 or self.rect.right == 768:
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
	
	# Block removal ability
	def paint_skill(self, room):
		
		# Create an invisible paintbrush sprite for collision with other sprites
		paintbrush = pygame.sprite.Sprite()
		# Make the paintbrush to the right of the player and 15x15 in size.
		paintbrush.rect = pygame.Rect(self.rect.x + 60, self.rect.y + 30, 15, 15)
		
		if self.mana:
			# Test for collisions with the wall list, destroy walls
			block_hit_list = pygame.sprite.spritecollide(paintbrush, room.wall_list, True)
			self.mana -= 1
		else:
			print("Out of mana!")
			
		# Change collided blocks into a different wall appearance.
		#for block in block_hit_list:
		#	block_image = pygame.image.load('loosebrick.png').convert()
		#	block.image = block_image			

	# Ability to push loose blocks around
	def build_skill(self, room):
		
		# Create an invisible hammer tool sprite for collision with other sprites
		hammer = pygame.sprite.Sprite()
		# Make the build tool to the right of the player and 15x15 in size.
		
		if self.direction == "U":
			hammer.rect = pygame.Rect(self.rect.x + 30, self.rect.y - 5, 15, 15)
		if self.direction == "D":
			hammer.rect = pygame.Rect(self.rect.x + 30, self.rect.y + 60, 15, 15)
		if self.direction == "L":
			hammer.rect = pygame.Rect(self.rect.x - 5, self.rect.y + 30, 15, 15)			
		if self.direction == "R":
			hammer.rect = pygame.Rect(self.rect.x + 60, self.rect.y + 30, 15, 15)			
			
		block_hit_list = pygame.sprite.spritecollide(hammer, room.loose_block_list, False)
		
		for block in block_hit_list:
			if self.direction == "U":
				block.rect.y -= 64
			if self.direction == "D":
				block.rect.y += 64
			if self.direction == "L":
				block.rect.x -= 64
			if self.direction == "R":
				block.rect.x += 64

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()


    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(BLACK)

        # Return the image
        return image