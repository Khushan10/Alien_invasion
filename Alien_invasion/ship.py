import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	def __init__(self, ai_setting ,screen):
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_setting = ai_setting

		# Load ship image
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		# Start ship at the bottom
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		# Store a decimal value for ship centre
		self.center = float(self.rect.centerx)

		# Movement flag
		self.moving_right = False
		self.moving_left = False

	def update(self):
		# Update ship position
		if(self.moving_right and self.rect.right < self.screen_rect.right):
			self.center += self.ai_setting.ship_speed_factor
		if(self.moving_left and self.rect.left > 0):
			self.center -= self.ai_setting.ship_speed_factor
		self.rect.centerx = self.center

	def blitme(self):
		# Draw ship at current location
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		self.center = self.screen_rect.centerx
