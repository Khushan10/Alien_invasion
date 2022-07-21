import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	# A class to manage bullets fired from ship

	def __init__(self, ai_setting, screen, ship):
		super(Bullet, self).__init__()
		self.screen = screen

		# Create a bullet at (0,0) and then change position
		self.rect = pygame.Rect(0,0,ai_setting.bullet_width,ai_setting.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top

		# Store bullet position as a decimal
		self.y = float(self.rect.y)

		self.color = ai_setting.bullet_color
		self.speed_factor = ai_setting.bullet_speed_factor

	def update(self):
		# Move bullet upward
		self.y -= self.speed_factor
		self.rect.y = self.y

	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)