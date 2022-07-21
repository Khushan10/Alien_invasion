import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import sound_effects as se

def fire_bullet(ai_setting, screen, ship, bullets):
	# Create new bullet
	if(len(bullets) < ai_setting.bullet_allowed):
		new_bullet = Bullet(ai_setting, screen, ship)
		bullets.add(new_bullet)
		se.bullet_sound.play()


def check_keydown_events(event, ai_setting, screen, ship, bullets):
	# Key is pressed
	if(event.key == pygame.K_RIGHT):
		# Move ship right
		ship.moving_right = True
	elif(event.key == pygame.K_LEFT):
		# Move ship left
		ship.moving_left = True
	elif(event.key == pygame.K_SPACE):
		fire_bullet(ai_setting, screen, ship, bullets)
	elif(event.key == pygame.K_ESCAPE):
		sys.exit()
		
def check_keyup_events(event, ship):
	# Key is released
	if(event.key == pygame.K_RIGHT):
		ship.moving_right = False
	elif(event.key == pygame.K_LEFT):
		ship.moving_left = False

def check_event(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets):
	# Keyboard action
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			sys.exit()
		elif(event.type == pygame.KEYDOWN):
			check_keydown_events(event, ai_setting, screen, ship, bullets)
		elif(event.type == pygame.KEYUP):
			check_keyup_events(event, ship)
		elif(event.type == pygame.MOUSEBUTTONDOWN):
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	# Start new game
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if(button_clicked and not stats.game_active):
		# Reset game speed
		ai_setting.initialize_dynamic_setting()

		# Hide mouse cursor
		pygame.mouse.set_visible(False)

		# Reset game stats
		stats.reset_stats()
		stats.game_active = True

		# Reset scoreboard
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		aliens.empty()
		bullets.empty()

		create_fleet(ai_setting, screen, ship, aliens)
		ship.center_ship()

def update_screen(ai_setting, screen, stats, sb, ship, aliens, bullets, play_button):
	# Redraw screen everytime
	screen.fill(ai_setting.bg_color)

	# Redaw all bullets behind ship and aliens
	for bullt in bullets.sprites():
		bullt.draw_bullet()
	ship.blitme()
	aliens.draw(screen)

	# Draw scoreboard
	sb.show_score()

	# Draw play button
	if(not stats.game_active):
		play_button.draw_button()

	# Most recent screen
	pygame.display.flip()

def update_bullets(ai_setting, screen, stats, sb, ship, aliens, bullets):
	bullets.update()

	# Delete bullets passed screen
	for bullt in bullets.copy():
		if(bullt.rect.bottom <= 0):
			bullets.remove(bullt)

	check_bullet_alien_collision(ai_setting, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collision(ai_setting, screen, stats, sb, ship, aliens, bullets):
	# Destroy aliens and bullets
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

	if(collisions):
		for aliens in collisions.values():
			stats.score += ai_setting.alien_points*(len(aliens))
			sb.prep_score()
		check_high_score(stats, sb)
		se.alien_sound.play()

	# Create another fleet
	if(len(aliens) == 0):
		# Destroy old bullets
		bullets.empty()
		ai_setting.increase_speed()
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_setting, screen, ship, aliens)

def get_number_aliens_x(ai_setting, alien_width):
	available_space_x = ai_setting.screen_width - 2*alien_width
	return int(available_space_x/(2*alien_width))

def get_number_rows(ai_setting, ship_height, alien_height):
	available_space_y = (ai_setting.screen_height - (3*alien_height) - ship_height)
	number_rows = int(available_space_y/(2*alien_height))
	return number_rows

def create_alien(ai_setting, screen, aliens, alien_number, row_numbers):
	alin = Alien(ai_setting, screen)
	alien_width = alin.rect.width
	alin.x = alien_width + 2*alien_width*alien_number
	alin.rect.x = alin.x
	alin.rect.y = alin.rect.height + 2*alin.rect.height*row_numbers
	aliens.add(alin)

def create_fleet(ai_setting, screen, ship, aliens):
	alin = Alien(ai_setting, screen)
	number_aliens_x = get_number_aliens_x(ai_setting, alin.rect.width)
	number_rows = get_number_rows(ai_setting, ship.rect.height, alin.rect.height)

	# Create fleet of aliens
	for row_numbers in  range(number_rows):	
		for alien_number in range(number_aliens_x):
			create_alien(ai_setting, screen, aliens, alien_number, row_numbers)

def change_fleet_direction(ai_setting, aliens):
	for alin in aliens.sprites():
		alin.rect.y += ai_setting.fleet_drop_speed
	ai_setting.fleet_direction *= -1

def check_fleet_edges(ai_setting, aliens):
	for alin in aliens.sprites():
		if(alin.check_edges()):
			change_fleet_direction(ai_setting, aliens)
			break

def ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets):
	if(stats.ships_left > 0):
		# Reduce ship life by 1
		stats.ships_left -= 1

		# Update score
		sb.prep_ships()

		# Empty aliens and bullets
		aliens.empty()
		bullets.empty()

		# Create new fleet and center the ship
		create_fleet(ai_setting, screen, ship, aliens)
		ship.center_ship()

		# Pause game for few moments to set the player
		sleep(0.5)

	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_setting, screen, stats, sb, ship, aliens, bullets):
	screen_rect = screen.get_rect()
	for alin in aliens.sprites():
		if(alin.rect.bottom >= screen_rect.bottom):
			ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets)
			break

def update_aliens(ai_setting, screen, stats, sb, ship, aliens, bullets):
	check_fleet_edges(ai_setting, aliens)
	aliens.update()

	# Alien and ship collision
	if(pygame.sprite.spritecollideany(ship, aliens)):
		ship_hit(ai_setting, screen, stats, sb, ship, aliens, bullets)

	# Aliens hit the bottom
	check_aliens_bottom(ai_setting, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
	if(stats.score > stats.high_score):
		stats.high_score = stats.score
		sb.prep_high_score()