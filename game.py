"""
   Scythe's Secrets (Working Title)
   By Danny Peck dannytpeck@gmail.com
   https://github.com/dannytpeck/scythes-secrets

   Main Game File
"""

import pygame, sys, menu, room
from player import *

FPS = 60 # frames per second to update the DISPLAYSURF
WINWIDTH = 800 # width of the program's window, in pixels
WINHEIGHT = 800 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

# Colors
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)


def main():
    # Pygame initialization and basic set up of the global variables.
	pygame.init()
	FPSCLOCK = pygame.time.Clock()

    # Because the Surface object stored in DISPLAYSURF was returned
    # from the pygame.display.set_mode() function, this is the
    # Surface object that is drawn to the actual computer screen
    # when pygame.display.update() is called.
	DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))	

	# Set the title of the window
	pygame.display.set_caption("Scythe's Secrets")
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	
	total_level_width  = 1600
	total_level_height = 1600

	# Create a camera object
	camera = Camera(complex_camera, total_level_width, total_level_height)

	# Set the height and width of the DISPLAYSURF
	# DOUBLESCALEDISPLAYSURF = pygame.display.set_mode([total_level_width, total_level_height])
	# Used for 2x scaling
	# DISPLAYSURF = pygame.Surface((total_level_width / 2, total_level_height / 2)).convert()
	# DISPLAYSURF = pygame.display.set_mode([total_level_width, total_level_height])
	
	# Create the player object and set starting location
	player = Player(400, 750)
	movingsprites = pygame.sprite.Group()
	movingsprites.add(player)

	# Create the display object
	display = menu.Display(DISPLAYSURF)
	
	# Create all the rooms
	rooms = []
	rooms.append(room.Room1())
	rooms[0].build_room()
	
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

				# Player abilities, still being debugged	
				if event.key == pygame.K_a:
					player.build_skill(current_room)
				
				# Debug ability: destroy/create all walls in the room.
				if event.key == pygame.K_s:
					if current_room.wall_list:
						for block in current_room.wall_list:
							block.kill()
					else:
						current_room.build_room()

				if event.key == pygame.K_f:
					player.paint_skill(current_room)
						
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
		
		# scale = pygame.transform.scale		
				
		# --- Drawing ---

		camera.update(player) # Update camera

		# Draw everything else
		#DISPLAYSURF.blit(current_room.background.image, camera.apply(current_room.background))
		
		#DISPLAYSURF.fill(BLACK)

		for e in current_room.floor_list:
			DISPLAYSURF.blit(e.image, camera.apply(e))

		for e in movingsprites:
			DISPLAYSURF.blit(e.image, camera.apply(e))			
			
		for e in current_room.wall_list:
			DISPLAYSURF.blit(e.image, camera.apply(e))

		for e in current_room.loose_block_list:
			DISPLAYSURF.blit(e.image, camera.apply(e))			
			
		# scale(DISPLAYSURF, DOUBLESCALEDISPLAYSURF.get_size(), DOUBLESCALEDISPLAYSURF)			
			
		pygame.display.update() # redraw DISPLAYSURF to the screen.

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
    l = max(-(camera.width-WINWIDTH), l)    # stop scrolling at the right edge
    t = max(-(camera.height-WINHEIGHT), t)  # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return pygame.Rect(l, t, w, h)


def terminate():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()