import os, sys
import pygame
from pygame.locals import *
from helpers import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# Main Python class
class PyManMain:
	def __init__(self, width=640,height=480):
		# """Initialize"""
		# """Initialize PyGame"""
		pygame.init()
		# """Set the window Size"""
		self.width = width
		self.height = height
		# """Create the Screen"""
		self.screen = pygame.display.set_mode((self.width, self.height))

	def MainLoop(self):
		# """This is the Main Loop of the Game"""
		# """Load All of our Sprites"""
		self.LoadSprites()
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					sys.exit()
				elif event.type == KEYDOWN:
					if ((event.key == K_RIGHT)
					or (event.key == K_LEFT)
					or (event.key == K_UP)
					or (event.key == K_DOWN)):
						self.snake.move(event.key)
						# """Check for collision"""
						lstCols = pygame.sprite.spritecollide(self.snake, self.pellet_sprites, True)
						# """Update the amount of pellets eaten"""
						self.snake.pellets = self.snake.pellets + len(lstCols)
			self.screen.fill([0,0,0])
			if pygame.font:
				font = pygame.font.Font(None, 36)
				text = font.render("Pellets %s" % self.snake.pellets, 1, (255, 0, 0))
				textpos = text.get_rect(centerx=self.width/2)
				self.screen.blit(text, textpos)
			self.pellet_sprites.draw(self.screen)
			self.snake_sprites.draw(self.screen)
			pygame.display.flip()
			pygame.display.update()

	def LoadSprites(self):
		# """Load the sprites that we need"""
		self.snake = Snake()
		self.snake_sprites = pygame.sprite.RenderPlain((self.snake))

		# """figure out how many pellets we can display"""
		nNumHorizontal = int(self.width/64)
		nNumVertical = int(self.height/64)       
		# """Create the Pellet group"""
		self.pellet_sprites = pygame.sprite.Group()
		# """Create all of the pellets and add them to the pellet_sprites group"""
		for x in range(nNumHorizontal):
			for y in range(nNumVertical):
				self.pellet_sprites.add(Pellet(pygame.Rect(x*64, y*64, 64, 64)))

# """This is our snake that will move around the screen"""
class Snake(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) 
		self.image, self.rect = load_image('snake.png',-1)
		self.pellets = 0
		self.x_dist = 5
		self.y_dist = 5

	def move(self, key):
		# """Move your self in one of the 4 directions according to key"""
		# """Key is the pyGame define for either up,down,left, or right key we will adjust ourselves in that direction"""
		xMove = 0;
		yMove = 0;
		
		if (key == K_RIGHT):
			xMove = self.x_dist
		elif (key == K_LEFT):
			xMove = -self.x_dist
		elif (key == K_UP):
			yMove = -self.y_dist
		elif (key == K_DOWN):
			yMove = self.y_dist
		self.rect.move_ip(xMove,yMove);

class Pellet(pygame.sprite.Sprite):
	def __init__(self, rect=None):
		pygame.sprite.Sprite.__init__(self) 
		self.image, self.rect = load_image('pellet.png',-1)
		if rect != None:
			self.rect = rect

if __name__ == "__main__":
	MainWindow = PyManMain()
	MainWindow.MainLoop()