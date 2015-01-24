"""
   Scythe's Secrets (Working Title)
   By Danny Peck dannytpeck@gmail.com
   https://github.com/dannytpeck/scythes-secrets

   Main Game File
"""

import pygame, sys, menu, room

from constants import *
from player import Player

class Game(object):
	''' The game object. Controls rendering the game and moving the player.
	'''
	def __init__(self):
		''' Sets up the initial game board, with the player at a set position.
			Once everything is set up, starts the game.
		'''
		pygame.display.set_caption("Scythe's Secrets")
		self.screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
		self.font = pygame.font.SysFont(None, 48)
		self.small_font = pygame.font.SysFont(None, 20)
		self.player = Player(400, 750)
		self.current_room = room.Room1()
		self.clock = pygame.time.Clock()
		# Create a camera object
		self.camera = Camera(complex_camera, TOTAL_LEVEL_WIDTH, TOTAL_LEVEL_HEIGHT)
		self.message = "Welcome to Scythe's Secrets!"
		self.display_alert = False
		self.run()
		
	def draw_alert(self, alert):
		''' Draws the alert box at the top 
		'''
		window = pygame.image.load('message window.png').convert()
		message = self.font.render(self.message, True, WHITE)
		
		self.screen.blit(window, (0, 0))
		self.screen.blit(message, (15, 15))

	def draw_darkness(self):
		pass
		''' Draws the darkness and shadows on the board. 0 is dark, 1 is in shadows,
	    	    2 is fully revealed.
		
		for row in range(ROWS):
			for col in range(COLUMNS):
				if self.map.cleared[row][col] == 0:
					pygame.draw.rect(self.screen, BLACK, (row*TILE_SIZE, col*TILE_SIZE, TILE_SIZE, TILE_SIZE)) 	
				if self.map.cleared[row][col] == 1:
					shadow = pygame.Surface((TILE_SIZE, TILE_SIZE))
					shadow.set_alpha(200)
					shadow.fill(BLACK)
					self.screen.blit(shadow, (row*TILE_SIZE, col*TILE_SIZE))
		'''

		
	def draw_floor(self):
		for i in self.current_room.floor_list:
			self.screen.blit(i.image, self.camera.apply(i))
		
	def draw_walls(self):
		for i in self.current_room.wall_list:
			self.screen.blit(i.image, self.camera.apply(i))
		
	def run(self):
		pygame.init()

		# Because the Surface object stored in DISPLAYSURF was returned
		# from the pygame.display.set_mode() function, this is the
		# Surface object that is drawn to the actual computer screen
		# when pygame.display.update() is called.
		DISPLAYSURF = self.screen
		
		# Set the title of the window
		pygame.display.set_caption("Scythe's Secrets")
		BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

		# Create the player object and set starting location
		player = Player(400, 750)

		movingsprites = pygame.sprite.Group()
		movingsprites.add(player)
		
		# Create all the rooms
		rooms = []
		rooms.append(room.Room1())
		rooms.append(room.Room2())
		rooms[0].build_room()

		self.current_room.build_room()
		
		done = False
		
		while not done:

			# --- Event Processing ---
			
			for event in pygame.event.get():
				# Player clicked the "X" at the corner of the window.
				if event.type == pygame.QUIT:
					sys.exit()

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
						player.build_skill(self.current_room)
					
					if event.key == pygame.K_s:
						self.message = "This is a sample dialog box!"

					if event.key == pygame.K_d:
						if self.display_alert == False:
							self.display_alert = True
						else:
							self.display_alert = False
						
					if event.key == pygame.K_f:
						player.paint_skill(self.current_room, DISPLAYSURF)
							
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

			player.move(self.current_room)	
			self.camera.update(player) # Update camera

			# If the player gets to the edge of the room, go to the next room
			if player.rect.y < 0:
				player.rect.y = TOTAL_LEVEL_HEIGHT-5
				self.current_room = rooms[0]
				self.current_room.build_room()
			
			if player.rect.y > TOTAL_LEVEL_HEIGHT:
				player.rect.y = 5
				self.current_room = rooms[1]
				self.current_room.build_room()
			
			# --- Drawing ---		

			self.draw_floor()

			for e in movingsprites:
				DISPLAYSURF.blit(e.image, self.camera.apply(e))			

			self.draw_walls()	
				
			if player.skillsprites:
				now = pygame.time.get_ticks()
				if now - player.last_skill_use >= player.skill_cooldown:
					for e in player.skillsprites:
						e.kill()
				for e in player.skillsprites:
					DISPLAYSURF.blit(e.image, self.camera.apply(e))					
				
			if self.current_room.loose_block_list:
				for e in self.current_room.loose_block_list:
					DISPLAYSURF.blit(e.image, self.camera.apply(e))			

			if self.display_alert == True:
				self.draw_alert("Hello.")
				
			pygame.display.update() # redraw DISPLAYSURF to the screen.

			self.clock.tick(FPS)
		
	
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
	
def main():
	while 1:
		pygame.init()
		game = Game()

if __name__ == "__main__":
    main()