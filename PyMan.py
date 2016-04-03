import os, sys
import pygame
from pygame.locals import *
from helpers import *
from random import randint
import math
import time

# if not pygame.font: print 'Warning, fonts disabled'
# if not pygame.mixer: print 'Warning, sound disabled'

SCREENWIDTH = 800
SCREENHEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BASESPAWNRATE = 250
BASEMAXENEMIES = 5
BASEMINENEMYSPEED = 15
BASEMAXENEMYSPEED = 10
LEVELUPDELAY = 3

# Main Python class
class PyManMain:
	def __init__(self, width=SCREENWIDTH,height=SCREENHEIGHT):
		# Initialize PyGame
		pygame.init()
		# Set the window Size
		self.width = width
		self.height = height
		# Set the base position
		self.baseWidth = int(self.width/2-50)
		self.baseHeight = int(self.height*0.79)
		# Create the Screen
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.bg = pygame.image.load(os.path.join('data', 'bg.png'))
		self.start = 1
		# Get all of the words and their translations
		self.enemyText = {}
		self.numWords = 0
		self.getWords()
		self.highScore = 0

	def MainLoop(self):
		while self.start:
			self.startingScreen()
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					sys.exit()
				elif event.type == KEYDOWN:
					if event.key == K_RETURN:
						self.start = 0

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

			self.loadSprites()

			# This is the main game state loop
			while self.alive:
				self.timer += 1

				# The high score is constantly updated
				if self.score > self.highScore:
					self.highScore = self.score
				# Here we get text inputs or quit the game
				self.getInput()
				# Enemies are spawned randomly and then move
				self.spawnEnemies()
				self.moveEnemies()
				# The screen is updated every run through the loop
				self.updateScreen()
				pygame.display.flip()
				# Here we move to the next level
				if (self.enemyCount == self.maxEnemies) and (len(self.enemy_sprites) == 0):
					self.levelUp()
				# A collision ends the game
				if pygame.sprite.spritecollide(self.base,self.enemy_sprites, True):
					self.gameOver()

			# We restart the game if enter is pressed
			while self.alive == 0:
				for event in pygame.event.get():
					if event.type == pygame.QUIT: 
						sys.exit()
					elif event.type == KEYDOWN:
						if event.key == K_RETURN:
							self.alive = 1

	# This collects all the words and their translations, storing them in a dictionary
	def getWords(self):
		with open ("words.txt", "r") as myfile:
		# with open ("japanesewords.txt", "r") as myfile:
			data = myfile.readlines()
			for line in data:
				text, key = line[:-1].split()
				self.enemyText[key] = text
				self.numWords += 1

	def loadSprites(self):
		# Find the bottom left of the screen and put the base there
		self.base = Base()
		self.base.rect.move_ip(self.baseWidth,self.baseHeight)
		self.base_sprites = pygame.sprite.RenderPlain((self.base))
		self.enemy_sprites = pygame.sprite.Group()

	# This grabs both the keyboard input or the closing of the window
	def getInput(self):
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
						if enemy.key == self.text:
							enemy.boom()
							self.score += 1
					self.text = ""

	# This method fills the screen with all the current sprites and text
	def updateScreen(self):
		# This draws the background and the text
		self.screen.blit(self.bg, (0, 0))
		scoreFont = pygame.font.Font(None, 36)
		text = scoreFont.render("Level: %s" % self.level, 1, WHITE)
		textpos = text.get_rect()
		self.screen.blit(text, textpos)
		text = scoreFont.render("Score: %s" % self.score, 1, WHITE)
		textpos = text.get_rect(centery=33)
		self.screen.blit(text, textpos)
		text = scoreFont.render("High Score: %s" % self.highScore, 1, WHITE)
		textpos = text.get_rect(centery=53)
		self.screen.blit(text, textpos)
		text = scoreFont.render(self.text, 1, WHITE)
		textpos = text.get_rect(centerx=self.width/2,centery=self.height*0.975)
		self.screen.blit(text, textpos)

		# Now we draw the sprites
		for enemy in self.enemy_sprites:
			if enemy.speed != 0:
				text = scoreFont.render(enemy.text,1,enemy.textColour)
				textpos = text.get_rect(centerx=enemy.rect.left+15,centery=enemy.rect.top-5)
				self.screen.blit(text,textpos)
		self.enemy_sprites.draw(self.screen)
		self.base_sprites.draw(self.screen)

	# This method paints the starting screen
	def startingScreen(self):
		# self.screen.fill([0,0,0])
		self.screen.blit(self.bg, (0, 0))
		font = pygame.font.Font(None, 80)
		text = font.render("TRANSLATING OF THE DEAD", 1, BLACK)
		textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
		self.screen.blit(text, textpos)
		font = pygame.font.Font(None, 36)
		text = font.render("PRESS ENTER TO START", 1, BLACK)
		textpos = text.get_rect(centerx=self.width/2,centery=self.height/2+40)
		self.screen.blit(text, textpos)
		font = pygame.font.Font(None, 24)
		text = font.render("Stop the ghosts by typing out their corresponding French/English translation", 1, BLACK)
		textpos = text.get_rect(centerx=self.width/2,centery=self.height*0.9)
		self.screen.blit(text, textpos)
		pygame.display.flip()

	# Enemies can spawn based on the RNG
	def spawnEnemies(self):
		if self.enemyCount != self.maxEnemies:
			if randint(1,self.spawnRate) == self.spawnRate:
				text, key = self.enemyText.items()[randint(0,self.numWords-1)]
				if randint(0,1):
					text, key = key, text
				self.spawnEnemy(randint(self.maxEnemySpeed,self.minEnemySpeed),text,key)
				self.enemyCount += 1

	def spawnEnemy(self,speed,text,key):
		spawnPoint = randint(0,2)
		if spawnPoint == 0:	# Here the enemy spawns along the top
			h = 0
			w = randint(int(self.width*0.1),int(self.width*0.9))
		elif spawnPoint == 1:		# Here the enemy spawns along the right
			w = int(self.width*0.95)
			h = randint(0,self.height)
		else: # Here the enemy spawns along the left
			w = int(self.width*0.05)
			h = randint(0,self.height)
		self.enemy_sprites.add(Enemy(speed,text,key,pygame.Rect(w, h, w, h)))

	# The enemies move towards the base over time
	def moveEnemies(self):
		for enemy in self.enemy_sprites:
			if (enemy.speed != 0) and (self.timer%enemy.speed == 0):
				enemy.move(self.base.rect.left,self.base.rect.top)
			elif enemy.speed == 0:
				enemy.shrink()
				if enemy.size < 5:
					self.enemy_sprites.remove(enemy)

	# When a level is completed, the enemy parameters are updated
	def levelUp(self):
		self.updateScreen()
		font = pygame.font.Font(None, 40)
		text = font.render("LEVEL UP!", 1, BLACK)
		textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
		self.screen.blit(text, textpos)
		pygame.display.flip()
		time.sleep(LEVELUPDELAY)
		self.level += 1
		self.enemyCount = 0
		self.maxEnemies += 3
		self.maxEnemySpeed = max(1,self.maxEnemySpeed-3)
		self.minEnemySpeed = max(5,self.minEnemySpeed-1)
		self.spawnRate = max(50,int(self.spawnRate*0.8))

	# The game over screen does not get painted over until enter is pressed in the main loop
	def gameOver(self):
		self.alive = 0
		font = pygame.font.Font(None, 80)
		text = font.render("GAME OVER", 1, BLACK)
		textpos = text.get_rect(centerx=self.width/2,centery=self.height/2)
		self.screen.blit(text, textpos)
		font = pygame.font.Font(None, 36)
		text = font.render("Press enter to play again", 1, BLACK)
		textpos = text.get_rect(centerx=self.width/2,centery=self.height/2+40)
		self.screen.blit(text, textpos)
		pygame.display.flip()

class Enemy(pygame.sprite.Sprite):
	def __init__(self, speed, text, key, rect=None):
		pygame.sprite.Sprite.__init__(self) 
		self.image, self.rect = load_image('boo-3.png',-1)
		self.speed = speed
		self.text = text
		self.key = key
		self.size = 64
		self.textColour = (randint(0,255),randint(0,255),randint(0,255))
		if rect != None:
			self.rect = rect
		# We flip the image if it is on the left side
		if self.rect.left < SCREENWIDTH/2:
			self.image = pygame.transform.flip(self.image,1,0)

	# The enemy moves in a diagonal path toward the base
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

	# This destroys the enemy. Setting its speed to 0 is used to indicate that it was destroyed
	def boom(self):
		self.image = load_image('boo-2.png',-1)[0]
		# We flip the image if it is on the left side
		if self.rect.left < SCREENWIDTH/2:
			self.image = pygame.transform.flip(self.image,1,0)
		self.speed = 0

	# Destroyed enemies keep shrinking until a certain point where they are deleted
	def shrink(self):
		self.size = int(self.size*0.975)
		self.image = pygame.transform.scale(self.image, (self.size, self.size))

class Base(pygame.sprite.Sprite):
	def __init__(self, rect=None):
		pygame.sprite.Sprite.__init__(self) 
		self.image, self.rect = load_image('house.png',-1)
		if rect != None:
			self.rect = rect

if __name__ == "__main__":
	MainWindow = PyManMain()
	MainWindow.MainLoop()