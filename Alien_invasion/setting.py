class Setting():
	# A class to stroe settings
	
	def __init__(self):
		#Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)

		# Ship setting
		self.ship_limit = 3

		# Bullet setting
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullet_allowed = 3

		# Alien setting
		self.fleet_drop_speed = 10

		# How quickly game speeds up
		self.speedup_scale = 1.1

		# How quickly alien points increase
		self.score_scale = 1.1

		self.initialize_dynamic_setting()

	def initialize_dynamic_setting(self):
		# Setting that changes throught the game
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 1.5
		self.alien_speed_factor = 0.4

		# Fleet direction 1 represent right and -1 represent left
		self.fleet_direction = 1

		# Scoring
		self.alien_points = 10

	def increase_speed(self):
		# Everyones speed increases except bullets to give challenge
		self.ship_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= 1

		self.alien_points = int(self.alien_points*self.score_scale)
