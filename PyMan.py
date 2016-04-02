import os, sys
import pygame
from pygame.locals import *
from helpers import *
from random import randint
import math

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# Main Python class
class PyManMain:
	def __init__(self, width=800,height=600):
		# """Initialize PyGame"""
		pygame.init()
		# """Set the window Size"""
		self.width = width
		self.height = height
		# Set the base position
		self.baseWidth = int(self.width*(-0.025))
		self.baseHeight = int(self.height*0.925)
		# Main variables
		self.alive = 1
		self.timer = 0
		self.score = 0
		self.spawnRate = 250
		self.enemyCount = 0
		self.enemyMax = 10
		self.enemySpeedMin = 5
		# """Create the Screen"""
		self.screen = pygame.display.set_mode((self.width, self.height))

	def MainLoop(self):
		# """This is the Main Loop of the Game"""
		# """Load All of our Sprites"""
		self.LoadSprites()
		while self.alive:
			self.timer += 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					sys.exit()

			# Enemies are spawned randomly, up to a certain amount. They then move
			if self.enemyCount != self.enemyMax:
				if randint(1,self.spawnRate) == self.spawnRate:
					self.spawnEnemy(randint(self.enemySpeedMin,10))
					self.enemyCount += 1
			for enemy in self.enemy_sprites:
				if self.timer%enemy.speed == 0:
					enemy.move(self.base.rect.left,self.base.rect.top)
			
			self.screen.fill([0,0,0])
			font = pygame.font.Font(None, 36)
			text = font.render("Enemies %s" % self.enemyCount, 1, (255, 0, 0))
			textpos = text.get_rect(centerx=self.width/2)
			self.screen.blit(text, textpos)
				# self.screen.blit(font.render("Test",1,(255,255,255)),text.get_rect(centerx=w,centery=h))
			self.enemy_sprites.draw(self.screen)
			self.base_sprites.draw(self.screen)
			pygame.display.flip()

			# A collision ends the game
			if pygame.sprite.spritecollide(self.base,self.enemy_sprites, True):
				self.alive = 0

		# This is for the end of the game
		font = pygame.font.Font(None, 80)
		text = font.render("Game Over", 1, (255, 0, 0))
		textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
		self.screen.blit(text, textpos)
		pygame.display.flip()
		while 1:
			pass

	def LoadSprites(self):
		# """Load the sprites that we need"""
		# self.snake = Snake()
		# self.snake_sprites = pygame.sprite.RenderPlain((self.snake))

		# """figure out how many pellets we can display"""
		# nNumHorizontal = int(self.width/64)
		# nNumVertical = int(self.height/64)       
		# """Create the Pellet group"""
		# self.pellet_sprites = pygame.sprite.Group()
		# # """Create all of the pellets and add them to the pellet_sprites group"""
		# for x in range(nNumHorizontal):
		# 	for y in range(nNumVertical):
		# 		self.pellet_sprites.add(Pellet(pygame.Rect(x*64, y*64, 64, 64)))

		self.enemy_sprites = pygame.sprite.Group()

		# Find the bottom left of the screen and put the base there
		self.base = Base()
		self.base.rect.move_ip(self.baseWidth,self.baseHeight)
		self.base_sprites = pygame.sprite.RenderPlain((self.base))

	def spawnEnemy(self,speed):
		flag = randint(0,1)
		if flag:	# Here the enemy spawns along the top
			h = 0
			w = randint(0,int(self.width*0.9))
		else:		# Here the enemy spawns along the right
			w = int(self.width*0.95)
			h = randint(0,self.height)
		self.enemy_sprites.add(Enemy(speed,pygame.Rect(w, h, w, h)))

# """This is our snake that will move around the screen"""
class Enemy(pygame.sprite.Sprite):
	def __init__(self, speed, rect=None):
		pygame.sprite.Sprite.__init__(self) 
		self.image, self.rect = load_image('snake.png',-1)
		self.speed = speed
		if rect != None:
			self.rect = rect

	def move(self, baseX, baseY):
		# """Move your self in one of the 4 directions according to key"""
		# """Key is the pyGame define for either up,down,left, or right key we will adjust ourselves in that direction"""
		
		xDif = baseX - self.rect.left
		yDif = baseY - self.rect.top
		diagonal = math.sqrt(xDif*xDif+yDif*yDif)

		if diagonal != 0:
			xMove = 3*xDif/diagonal
			yMove = 3*yDif/diagonal
		else:
			xMove = 0
			yMove = 0
		# if self.rect.left > baseX:
		# 	xMove = -1
		# elif self.rect.left < baseX:
		# 	xMove = 1
		# else:
		# 	xMove = 0
		# if self.rect.top > baseY:
		# 	yMove = -1
		# elif self.rect.top < baseY:
		# 	yMove = 1
		# else:
		# 	yMove = 0



		# if (key == K_RIGHT):
		# 	xMove = self.x_dist
		# elif (key == K_LEFT):
		# 	xMove = -self.x_dist
		# elif (key == K_UP):
		# 	yMove = -self.y_dist
		# elif (key == K_DOWN):
		# 	yMove = self.y_dist
		self.rect.move_ip(xMove,yMove);

class Base(pygame.sprite.Sprite):
	def __init__(self, rect=None):
		pygame.sprite.Sprite.__init__(self) 
		self.image, self.rect = load_image('pellet.png',-1)
		if rect != None:
			self.rect = rect

if __name__ == "__main__":
	MainWindow = PyManMain()
	MainWindow.MainLoop()