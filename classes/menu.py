"""
   Scythe's Secrets (Working Title)
   By Danny Peck dannytpeck@gmail.com
   https://github.com/dannytpeck/scythes-secrets

   Main Menu File
"""

import pygame, os.path, sys

from pygame.locals import *
from constants import * 

# simple wrapper to keep the screen resizeable
def init_screen(width, height):
    global temp_surface
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    temp_surface = pygame.Surface((width / 2, height / 2)).convert()
    return screen
    
# make loading images a little easier
def load_image(filename):
    return pygame.image.load(os.path.join(RESOURCES_DIR, filename))

def main():
    """ Main Program """

    # Set the height and width of the screen
    screen = pygame.display.set_mode([screen_width, screen_height])	    

    # Set the title of the window
    pygame.display.set_caption("Scythe's Secrets")
    
    # Create the menu object
    menu = Menu(screen)
    menu.run()

    
class Menu():
    """ This class is for the menu """
    item_selection = 0	

    # Initialize the Pygame library 
    pygame.init()	

    font = pygame.font.Font(None, 32)
	
    background_color = (51, 51, 51)
    text_color = (255, 255, 153)
    selection_color = (153, 102, 255)
	
    def __init__(self, screen):
        """ Constructor function """
        self.screen = screen

    def run(self):    
        display = Display(self.screen)
        clock = pygame.time.Clock()
        done = False
        
        while not done:
            for event in pygame.event.get():
                if event.type == QUIT: # If user clicked close
                    sys.exit()

                if event.type == VIDEORESIZE:
                    init_screen(event.w, event.h)                    
                    
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.change_selection(-1)
                    if event.key == K_DOWN:
                        self.change_selection(1)
                    if event.key == K_RETURN:
                        if self.get_selection() == 0:
                            print("Start New Game")
                            self.intro()
                        if self.get_selection() == 1:
                            print("Load Saved Game")
                            #if no saved games found:
                            display.dialog_box(["No save file found."], self.screen)
                        if self.get_selection() == 2:
                            print("Options & Controls")
                            #self.options()
                        if self.get_selection() == 3:
                            print("Credits")
                            #self.credits()
                        if self.get_selection() == 4:
                            print("Quit")
                            sys.exit()
                    if event.key == K_ESCAPE:
                        done = True                      
                        
            self.screen.fill(WHITE) # Draw white background
            self.draw() # Draw the menu

            FPS = 30
            clock.tick(FPS)		
            
            pygame.display.flip()               

    def intro(self):
        """ Display the scrolling text intro """
        
        x = 0
        y = self.screen.get_height()
        
        clock = pygame.time.Clock()

        # Load and set up graphics.
        intro_text_image = load_image("intro.png")
        intro_text_image.set_colorkey(WHITE)

        done = False
        
        while not done:
            for event in pygame.event.get(): # User did something
                if event.type == QUIT: # If user clicked close
                    sys.quit()
                
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        done = True
                    if event.key == K_ESCAPE:
                        done = True

            self.screen.fill(WHITE) # Draw white background

            self.screen.blit(intro_text_image, [x,y]) 
            # text crawls upward
            y -= 1
            
            FPS = 30
            clock.tick(FPS)		
            pygame.display.flip()


    def get_selection(self):
        return self.item_selection
		
    def change_selection(self, move):
        """ Change selected item on the menu """
        self.item_selection += move
		
        if self.item_selection < 0:
            self.item_selection = 4
			
        if self.item_selection > 4:
            self.item_selection = 0

    def draw(self):
        """ Draw the menu """
        screen_width  = self.screen.get_width()
        screen_height = self.screen.get_height()
		
        # Menu background
        square = pygame.Surface([400, 325])
        square.fill(self.background_color)
        self.screen.blit(square, [screen_width / 4, screen_height / 4])        

        # Menu text
        if self.item_selection == 0: 
            text = self.font.render("Start New Game", True, self.text_color, self.selection_color)
        else:
            text = self.font.render("Start New Game", True, self.text_color)
        self.screen.blit(text, [screen_width / 4 + 50, screen_height / 4 + 50])

        if self.item_selection == 1: 
            text = self.font.render("Load Saved Game", True, self.text_color, self.selection_color)
        else:
            text = self.font.render("Load Saved Game", True, self.text_color)
        self.screen.blit(text, [screen_width / 4 + 50, screen_height / 4 + 100])

        if self.item_selection == 2: 
            text = self.font.render("Options & Controls", True, self.text_color, self.selection_color)
        else:
            text = self.font.render("Options & Controls", True, self.text_color)
        self.screen.blit(text, [screen_width / 4 + 50, screen_height / 4 + 150])
		
        if self.item_selection == 3: 
            text = self.font.render("Credits", True, self.text_color, self.selection_color)
        else:
            text = self.font.render("Credits", True, self.text_color)
        self.screen.blit(text, [screen_width / 4 + 50, screen_height / 4 + 200])
		
        if self.item_selection == 4: 
            text = self.font.render("Quit", True, self.text_color, self.selection_color)
        else:
            text = self.font.render("Quit", True, self.text_color)
        self.screen.blit(text, [screen_width / 4 + 50, screen_height / 4 + 250])        
        
		
class Display():
    """ This class is for the HUD stuff """	
    background_color = (51, 51, 51)
    text_color = (255, 255, 153)
	
    def __init__(self, screen):
        """ Constructor function """
        self.screen = screen

    def draw_text(self, text_list, screen):
        f = pygame.font.Font(None, 32)

        # save the rendered text
        self.text_overlay = [f.render(i, 1, self.text_color) for i in text_list]		
		
        y = 0
        for text in self.text_overlay:
            screen.blit(text, (self.margin*2, self.margin*2+y))
            y += text.get_height()		
		
    def dialog_box(self, dialog, screen):
        """ Pop up a dialogue box on the screen """
        self.margin = 10
        screen_width  = self.screen.get_width()
        screen_height = self.screen.get_height()
		
        clock = pygame.time.Clock()	
		
        done = False
		
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    done = True 
			
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        done = True					
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    if event.key == pygame.K_a:
                        done = True
						
			# Make the box
            square = pygame.Surface([screen_width - self.margin * 2, 130])
            square.fill(self.background_color)
            screen.blit(square, [self.margin, self.margin])

            self.draw_text(dialog, screen)
			#self.draw_text(["This is line one of the text box", "and this is line two."], screen)
				
			# 60 fps
            clock.tick(60)		
            pygame.display.flip()	
	

if __name__ == "__main__":
    main()
	