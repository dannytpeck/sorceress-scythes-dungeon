import pygame
from spritesheet import *
from rooms import *

# Global constants

# Colors
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)

# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 800

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

		# Choose a sprite sheet to use
		sprite_sheet = SpriteSheet("mage.png")

		# Load all the up facing images into a list
		image = sprite_sheet.get_image(0, 0, 32, 36)
		self.walking_frames_u.append(image)
		image = sprite_sheet.get_image(32, 0, 32, 36)
		self.walking_frames_u.append(image)
		image = sprite_sheet.get_image(64, 0, 32, 36)
		self.walking_frames_u.append(image)

		# Load all the right facing images into a list
		image = sprite_sheet.get_image(0, 36, 32, 36)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(32, 36, 32, 36)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(64, 36, 32, 36)
		self.walking_frames_r.append(image)

		# Load all the down facing images into a list
		image = sprite_sheet.get_image(0, 72, 32, 36)
		self.walking_frames_d.append(image)
		image = sprite_sheet.get_image(32, 72, 32, 36)
		self.walking_frames_d.append(image)
		image = sprite_sheet.get_image(64, 72, 32, 36)
		self.walking_frames_d.append(image)

		# Load all the left facing images into a list
		image = sprite_sheet.get_image(0, 108, 32, 36)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(32, 108, 32, 36)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(64, 108, 32, 36)
		self.walking_frames_l.append(image)		

		# Set the image the player starts with (right by default)
		self.image = self.walking_frames_r[0]

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		
	# Player-controlled movement:
	def go_left(self):
		""" Called when the user hits the left arrow. """
		self.change_x = -5
		self.direction = "L"

	def go_right(self):
		""" Called when the user hits the right arrow. """
		self.change_x = 5
		self.direction = "R"

	def go_up(self):
		""" Called when the user hits the up arrow. """
		self.change_y = -5
		self.direction = "U"		
		
	def go_down(self):
		""" Called when the user hits the down arrow. """
		self.change_y = 5
		self.direction = "D"
				
	def move(self, walls):
		""" Move the player. """
		
		# Move up/down
		self.rect.y += self.change_y

		# Did this update cause us to hit a wall?
		block_hit_list = pygame.sprite.spritecollide(self, walls, False)
		for block in block_hit_list:

			# Reset our position based on the top/bottom of the object.
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
			else:
				self.rect.top = block.rect.bottom
				
		# Move left/right
		self.rect.x += self.change_x

		# Did this update cause us to hit a wall?
		block_hit_list = pygame.sprite.spritecollide(self, walls, False)
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
			
def main():
	""" Main Program """

	# Initialize the Pygame library 
	pygame.init()

	# Set the height and width of the screen
	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
	
	# Set the title of the window
	# pygame.display.set_caption("Scythe's Secrets")
	
	# Load and set up graphics
	background_image = pygame.image.load("background.png").convert()	

	# Create the player object and set starting location
	player = Player(50, 50)
	movingsprites = pygame.sprite.Group()
	movingsprites.add(player)
	
	# Create all the rooms
	rooms = []
	rooms.append(Room1())
	rooms.append(Room2())
	rooms.append(Room3())
	rooms.append(Room4())
	rooms.append(Room5())
	
	current_room_no = 0
	current_room = rooms[current_room_no]

	clock = pygame.time.Clock()

	done = False

	while not done:

		# --- Event Processing ---

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.go_left()
				if event.key == pygame.K_RIGHT:
					player.go_right()
				if event.key == pygame.K_UP:
					player.go_up()
				if event.key == pygame.K_DOWN:
					player.go_down()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and player.change_x < 0:
					player.change_x = 0
				if event.key == pygame.K_RIGHT and player.change_x > 0:
					player.change_x = 0
				if event.key == pygame.K_UP and player.change_y < 0:
					player.change_y = 0
				if event.key == pygame.K_DOWN and player.change_y > 0:
					player.change_y = 0

		# --- Game Logic ---
		
		player.move(current_room.wall_list)

		# West room exits
		if player.rect.x < 0:
			if current_room_no == 0:
				current_room_no = 3
				current_room = rooms[current_room_no]
				player.rect.x = SCREEN_WIDTH - 10
			elif current_room_no == 3:
				current_room_no = 2
				current_room = rooms[current_room_no]
				player.rect.x = SCREEN_WIDTH - 10
			elif current_room_no == 2:
				current_room_no = 1
				current_room = rooms[current_room_no]
				player.rect.x = SCREEN_WIDTH - 10				
			else:
				current_room_no = 0
				current_room = rooms[current_room_no]
				player.rect.x = SCREEN_WIDTH - 10

		# East room exits
		if player.rect.x > SCREEN_WIDTH:
			if current_room_no == 0:
				current_room_no = 1
				current_room = rooms[current_room_no]
				player.rect.x = 0
			elif current_room_no == 1:
				current_room_no = 2
				current_room = rooms[current_room_no]
				player.rect.x = 0
			elif current_room_no == 2:
				current_room_no = 3
				current_room = rooms[current_room_no]
				player.rect.x = 0				
			else:
				current_room_no = 0
				current_room = rooms[current_room_no]
				player.rect.x = 0
				
		# North room exits
		if player.rect.y < 0:
			if current_room_no == 0:
				current_room_no = 4
				current_room = rooms[current_room_no]
				player.rect.y = SCREEN_HEIGHT - 10			

		# South room exits
		if player.rect.y > SCREEN_HEIGHT:
			if current_room_no == 4:
				current_room_no = 0
				current_room = rooms[current_room_no]
				player.rect.y = 0	
			else:
				current_room_no = 0
				current_room = rooms[current_room_no]
				player.rect.y = 0
				
		# --- Drawing ---
		screen.fill(BLACK) # Draw black background
		screen.blit(background_image, [0,0]) # Draw background image
		
		current_room.wall_list.draw(screen) # Draw walls
		movingsprites.draw(screen) # Draw moving sprites i.e. the player

		# Limit to 60 fps
		clock.tick(60)

		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()

	#pygame.quit()

if __name__ == "__main__":
    main()
