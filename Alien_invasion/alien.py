import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	def __init__(self, ai_setting, screen):
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_setting = ai_setting

		# Load alien ship
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		# Start new alien at top left
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# Store exact position
		self.x = float(self.rect.x)

	def blitme(self):
		self.screen.blit(self.image, self.rect)

	def check_edges(self):
		screen_rect = self.screen.get_rect()
		if(self.rect.right >= screen_rect.right):
			return True
		elif(self.rect.left <= 0):
			return True

	def update(self):
		# Move alien to right
		self.x += (self.ai_setting.alien_speed_factor*self.ai_setting.fleet_direction)
		self.rect.x = self.x

