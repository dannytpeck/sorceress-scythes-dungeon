# Scythe's Secrets (Working Title)
# By Danny Peck dannytpeck@gmail.com
# https://github.com/dannytpeck/scythes-secrets
# Released under MIT license

import sys, menu, room, spritesheet, pygame
from pygame.locals import *

FPS = 60 # frames per second to update the DISPLAYSURF
WINWIDTH = 400 # width of the program's window, in pixels
WINHEIGHT = 400 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

# Colors
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)


def main():
	global FPSCLOCK, DISPLAYSURF

    # Pygame initialization and basic set up of the global variables.
	pygame.init()
	FPSCLOCK = pygame.time.Clock()

    # Because the Surface object stored in DISPLAYSURF was returned
    # from the pygame.display.set_mode() function, this is the
    # Surface object that is drawn to the actual computer screen
    # when pygame.display.update() is called.
	DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))	
	
	total_level_width  = 800
	total_level_height = 800

	# Create a camera object
	camera = Camera(complex_camera, total_level_width, total_level_height)

	# Set the height and width of the DISPLAYSURF
	DOUBLESCALEDISPLAYSURF = pygame.display.set_mode([total_level_width, total_level_height])
	# Used for 2x scaling
	DISPLAYSURF = pygame.Surface((total_level_width / 2, total_level_height / 2)).convert()
	# DISPLAYSURF = pygame.display.set_mode([total_level_width, total_level_height])

	# Set the title of the window
	pygame.display.set_caption("Scythe's Secrets")
	
	# Create the player object and set starting location
	player = Player(400, 750)
	movingsprites = pygame.sprite.Group()
	movingsprites.add(player)

	# Create the display object
	display = menu.Display(DISPLAYSURF)
	
	# Create all the rooms
	rooms = []
	rooms.append(room.Room1())
	rooms.append(room.Room2())
	rooms.append(room.Room3())
	rooms.append(room.Room4())
	rooms.append(room.Room5())
	
	current_room_no = 0
	current_room = rooms[current_room_no]

	done = False

	while not done:

		# --- Event Processing ---
		
		for event in pygame.event.get():
			# Player clicked the "X" at the corner of the window.
			if event.type == pygame.QUIT:
				terminate()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.go_left()
				if event.key == pygame.K_RIGHT:
					player.go_right()
				if event.key == pygame.K_UP:
					player.go_up()
				if event.key == pygame.K_DOWN:
					player.go_down()
				if event.key == pygame.K_a:
					display.dialog_box(["This is a dialog box."], DISPLAYSURF)				
					player.stop()
				# debug - if you press S, the player's sprite vanishes
				if event.key == pygame.K_s:
					for block in current_room.loose_wall_list:
						block.kill()
						
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
		
		player.move(current_room)
		
		scale = pygame.transform.scale		
				
		# --- Drawing ---

		camera.update(player) # Update camera

		# Draw everything else
		DISPLAYSURF.blit(current_room.background.image, camera.apply(current_room.background))
		
		for e in movingsprites:
			DISPLAYSURF.blit(e.image, camera.apply(e))
		
		for e in current_room.wall_list:
			DISPLAYSURF.blit(e.image, camera.apply(e))

		for e in current_room.loose_wall_list:
			DISPLAYSURF.blit(e.image, camera.apply(e))			
			
		scale(DISPLAYSURF, DOUBLESCALEDISPLAYSURF.get_size(), DOUBLESCALEDISPLAYSURF)			
			
		pygame.display.update() # draw DISPLAYSURF to the screen.
		FPSCLOCK.tick(FPS)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(-l+HALF_WINWIDTH, -t+HALF_WINHEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WINWIDTH, -t+HALF_WINHEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WINWIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WINHEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return pygame.Rect(l, t, w, h)

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
		sprite_sheet = spritesheet.SpriteSheet("player.png")

		# Load all the down facing images into a list
		image = sprite_sheet.get_image(0, 0, 32, 32)
		self.walking_frames_d.append(image)
		image = sprite_sheet.get_image(32, 0, 32, 32)
		self.walking_frames_d.append(image)
		image = sprite_sheet.get_image(64, 0, 32, 32)
		self.walking_frames_d.append(image)

		# Load all the left facing images into a list
		image = sprite_sheet.get_image(0, 32, 32, 32)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(32, 32, 32, 32)
		self.walking_frames_l.append(image)
		image = sprite_sheet.get_image(64, 32, 32, 32)
		self.walking_frames_l.append(image)

		# Load all the right facing images into a list
		image = sprite_sheet.get_image(0, 64, 32, 32)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(32, 64, 32, 32)
		self.walking_frames_r.append(image)
		image = sprite_sheet.get_image(64, 64, 32, 32)
		self.walking_frames_r.append(image)

		# Load all the up facing images into a list
		image = sprite_sheet.get_image(0, 96, 32, 32)
		self.walking_frames_u.append(image)
		image = sprite_sheet.get_image(32, 96, 32, 32)
		self.walking_frames_u.append(image)
		image = sprite_sheet.get_image(64, 96, 32, 32)
		self.walking_frames_u.append(image)		

		# Set the image the player starts with (right by default)
		self.image = self.walking_frames_r[0]

		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		
	# Player-controlled movement:
	def go_left(self):
		""" Called when the user hits the left arrow. """
		self.change_x = -3
		self.direction = "L"

	def go_right(self):
		""" Called when the user hits the right arrow. """
		self.change_x = 3
		self.direction = "R"

	def go_up(self):
		""" Called when the user hits the up arrow. """
		self.change_y = -3
		self.direction = "U"		
		
	def go_down(self):
		""" Called when the user hits the down arrow. """
		self.change_y = 3
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
		loose_block_hit_list = pygame.sprite.spritecollide(self, room.loose_wall_list, False)
		for block in loose_block_hit_list:

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
		loose_block_hit_list = pygame.sprite.spritecollide(self, room.loose_wall_list, False)
		for block in loose_block_hit_list:
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


def terminate():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()