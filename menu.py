import pygame
import game
 
# Constants

# Colors
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)

# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 800

class Menu():
	""" This class is for the menu """
	item_selection = 0	
	
	font_path = 'kenpixel.ttf'
	font_size = 32
	font = pygame.font.Font(font_path, font_size)
	
	background_color = (51, 51, 51)
	text_color = (255, 255, 153)
	selection_color = (153, 102, 255)
	
	def __init__(self, screen):
		""" Constructor function """
		self.screen = screen
	
	def set_colors(self, text, selection, background):
		""" Change the menu's colors """
		self.background_color = background
		self.text_color = text
		self.selection_color = selection
		
	def set_fontsize(self, font_size):
		""" Change the menu's font """
		self.font_size = font_size

	def get_selection(self):
		return self.item_selection
		
	def change_selection(self, move):
		""" Change selected item on the menu """
		self.item_selection += move
		
		if self.item_selection < 0:
			self.item_selection = 2
			
		if self.item_selection > 2:
			self.item_selection = 0

	def draw(self):
		""" Draw the menu """
		
		# Menu background
		square = pygame.Surface([400, 400])
		square.fill(self.background_color)
		self.screen.blit(square, [200, 225])

		# Menu text
		if self.item_selection == 0: 
			text = self.font.render("Start", True, self.text_color, self.selection_color)
		else:
			text = self.font.render("Start", True, self.text_color)
		self.screen.blit(text, [300, 300])

		if self.item_selection == 1: 
			text = self.font.render("Options", True, self.text_color, self.selection_color)
		else:
			text = self.font.render("Options", True, self.text_color)
		self.screen.blit(text, [300, 400])

		if self.item_selection == 2: 
			text = self.font.render("Quit", True, self.text_color, self.selection_color)
		else:
			text = self.font.render("Quit", True, self.text_color)
		self.screen.blit(text, [300, 500])

def intro(screen):
	done = False
	clock = pygame.time.Clock()
	font = pygame.font.Font('kenpixel.ttf', 20)
	x = 0
	y = 700

	# Load and set up graphics.
	player_image = pygame.image.load("intro.png").convert()
	player_image.set_colorkey(WHITE)
	
	while not done:
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done = True # Flag that we are done so we exit this loop
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					done = True
					game.main()
				if event.key == pygame.K_ESCAPE:
					done = True
					game.main()

		screen.fill(WHITE) # Draw white background

		screen.blit(player_image, [0, y])	
		
		# text crawls upward
		y -= 1
		
		# 30 fps
		clock.tick(60)		
		pygame.display.flip()
	
def main():
	""" Main Program """

	# Initialize the Pygame library 
	pygame.init()

	# Set the height and width of the screen
	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])	

	# Set the title of the window
	pygame.display.set_caption("Scythe's Secrets")

	# Create the menu object
	menu = Menu(screen)
	
	clock = pygame.time.Clock()

	done = False	
	
	while not done:
	
		# --- Main event loop
		for event in pygame.event.get(): # User did something
			if event.type == pygame.QUIT: # If user clicked close
				done = True # Flag that we are done so we exit this loop
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					menu.change_selection(-1)
				if event.key == pygame.K_DOWN:
					menu.change_selection(1)
				if event.key == pygame.K_RETURN:
					if menu.get_selection() == 0:
						print("Start Game!")
						intro(screen)
					if menu.get_selection() == 1:
						print("Options!")
					if menu.get_selection() == 2:
						done = True
				if event.key == pygame.K_ESCAPE:
					done = True
			
		# --- Game logic should go here
 
		# --- Drawing ---
		screen.fill(WHITE) # Draw white background
		menu.draw() # Draw the menu

		# Limit to 60 fps
		clock.tick(60)		
		
		# --- Go ahead and update the screen with what we've drawn.
		pygame.display.flip()
 
	pygame.quit()
	
if __name__ == "__main__":
    main()
	