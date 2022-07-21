import pygame
from setting import Setting
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	# Intializing game and creating a screen
	pygame.init()
	ai_setting = Setting()
	screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
	pygame.display.set_caption("Alien Invasion")

	# Make a play button
	play_button = Button(ai_setting, screen, "Play")

	# Game stats
	stats = GameStats(ai_setting)

	# Scoreboard
	sb = Scoreboard(ai_setting, screen, stats)

	# Make a ship
	ship = Ship(ai_setting, screen)

	# Make a group to store bullets
	bullets = Group()

	# Make alien group
	aliens = Group()

	# Fleet of aliens
	gf.create_fleet(ai_setting, screen, ship, aliens)

	# Main loop for game
	while(True):
		gf.check_event(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets)
		if(stats.game_active):
			ship.update()
			gf.update_bullets(ai_setting, screen, stats, sb, ship, aliens, bullets)
			gf.update_aliens(ai_setting, screen, stats, sb, ship, aliens, bullets)
		gf.update_screen(ai_setting, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()