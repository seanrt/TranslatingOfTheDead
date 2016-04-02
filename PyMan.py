import os, sys
import pygame
from pygame.locals import *
from helpers import *
from random import randint
import math

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ENEMYTEXT = ["one","two","three","four","five","six","seven","eight","nine","ten"]
NUMWORDS = 10
BASESPAWNRATE = 250
BASEMAXENEMIES = 5
BASEMINENEMYSPEED = 15
BASEMAXENEMYSPEED = 10

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
		# """Create the Screen"""
		self.screen = pygame.display.set_mode((self.width, self.height))

	def MainLoop(self):
		while 1:
			# Main variables
			self.alive = 1
			self.timer = 0
			self.score = 0
			self.level = 1
			self.spawnRate = BASESPAWNRATE
			self.minEnemySpeed = BASEMINENEMYSPEED
			self.maxEnemySpeed = BASEMAXENEMYSPEED
			self.maxEnemies = BASEMAXENEMIES
			self.enemyCount = 0
			self.text = ''
			# """Load All of our Sprites"""
			self.LoadSprites()

			# This is the main game state loop
			while self.alive:
				self.timer += 1
				scoreFont = pygame.font.Font(None, 36)

				# Here we get text inputs or quit the game
				for event in pygame.event.get():
					if event.type == pygame.QUIT: 
						sys.exit()
					elif event.type == KEYDOWN:
						if event.unicode.isalpha():
							self.text += event.unicode
						elif event.key == K_BACKSPACE:
							self.text = self.text[:-1]
						elif event.key == K_RETURN:
							for enemy in self.enemy_sprites:
								if enemy.text == self.text:
									enemy.boom()
									self.score += 1
							self.text = ""

				# Enemies are spawned randomly, up to a certain amount. They then move
				if self.enemyCount != self.maxEnemies:
					if randint(1,self.spawnRate) == self.spawnRate:
						self.spawnEnemy(randint(self.maxEnemySpeed,self.minEnemySpeed),ENEMYTEXT[randint(0,NUMWORDS-1)])
						self.enemyCount += 1
				for enemy in self.enemy_sprites:
					if (enemy.speed != 0) and (self.timer%enemy.speed == 0):
						enemy.move(self.base.rect.left,self.base.rect.top)
					elif enemy.speed == 0:
						enemy.shrink()
						if enemy.size < 10:
							self.enemy_sprites.remove(enemy)
				
				# self.enemyCount = len(self.enemy_sprites)

				# The screen is updated every run through the loop
				self.screen.fill([0,0,0])
				text = scoreFont.render("Level: %s" % self.level, 1, GREEN)
				textpos = text.get_rect()
				self.screen.blit(text, textpos)
				text = scoreFont.render("Score: %s" % self.score, 1, GREEN)
				textpos = text.get_rect(centery=self.height*0.07)
				self.screen.blit(text, textpos)
				text = scoreFont.render(self.text, 1, BLUE)
				textpos = text.get_rect(centerx=self.width/2,centery=self.height*0.95)
				self.screen.blit(text, textpos)

				for enemy in self.enemy_sprites:
					if enemy.speed != 0:
						text = scoreFont.render(enemy.text,1,RED)
						textpos = text.get_rect(centerx=enemy.rect.left,centery=enemy.rect.top)
						self.screen.blit(text,textpos)
				self.enemy_sprites.draw(self.screen)
				self.base_sprites.draw(self.screen)

				pygame.display.flip()

				# Here we move to the next level
				if (self.enemyCount == self.maxEnemies) and (len(self.enemy_sprites) == 0):
					self.levelUp()

				# A collision ends the game
				if pygame.sprite.spritecollide(self.base,self.enemy_sprites, True):
					self.alive = 0

			# This is for the end of the game
			font = pygame.font.Font(None, 80)
			text = font.render("Game Over", 1, RED)
			textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
			self.screen.blit(text, textpos)
			font = pygame.font.Font(None, 36)
			text = font.render("Press enter to play again", 1, RED)
			textpos = text.get_rect(centerx=self.width/2,centery=self.height/2+40)
			self.screen.blit(text, textpos)
			pygame.display.flip()

			# We restart the game if enter is pressed
			while self.alive == 0:
				for event in pygame.event.get():
					if event.type == pygame.QUIT: 
						sys.exit()
					elif event.type == KEYDOWN:
						if event.key == K_RETURN:
							self.alive = 1


	def LoadSprites(self):
		self.enemy_sprites = pygame.sprite.Group()

		# Find the bottom left of the screen and put the base there
		self.base = Base()
		self.base.rect.move_ip(self.baseWidth,self.baseHeight)
		self.base_sprites = pygame.sprite.RenderPlain((self.base))

	def spawnEnemy(self,speed,text):
		flag = randint(0,1)
		if flag:	# Here the enemy spawns along the top
			h = 0
			w = randint(int(self.width*0.1),int(self.width*0.9))
		else:		# Here the enemy spawns along the right
			w = int(self.width*0.95)
			h = randint(0,self.height)
		self.enemy_sprites.add(Enemy(speed,text,pygame.Rect(w, h, w, h)))

	def levelUp(self):
		self.level += 1
		self.enemyCount = 0
		self.maxEnemies += 3
		self.maxEnemySpeed = max(1,self.maxEnemySpeed-3)
		self.minEnemySpeed = max(5,self.minEnemySpeed-1)
		self.spawnRate = max(50,int(self.spawnRate*0.8))

class Enemy(pygame.sprite.Sprite):
	def __init__(self, speed, text, rect=None):
		pygame.sprite.Sprite.__init__(self) 
		self.image, self.rect = load_image('snake.png',-1)
		self.speed = speed
		self.text = text
		self.size = 64
		if rect != None:
			self.rect = rect

	def move(self, baseX, baseY):		
		xDif = baseX - self.rect.left
		yDif = baseY - self.rect.top
		diagonal = math.sqrt(xDif*xDif+yDif*yDif)

		if diagonal != 0:
			xMove = 3*xDif/diagonal
			yMove = 3*yDif/diagonal
		else:
			xMove = 0
			yMove = 0

		self.rect.move_ip(xMove,yMove);

	def boom(self):
		self.image = load_image('deadsnake.png',-1)[0]
		self.speed = 0

	def shrink(self):
		self.size = int(self.size*0.9)
		self.image = pygame.transform.scale(self.image, (self.size, self.size))

class Base(pygame.sprite.Sprite):
	def __init__(self, rect=None):
		pygame.sprite.Sprite.__init__(self) 
		self.image, self.rect = load_image('pellet.png',-1)
		if rect != None:
			self.rect = rect

if __name__ == "__main__":
	MainWindow = PyManMain()
	MainWindow.MainLoop()