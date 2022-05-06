import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 750, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UFO Revised")

os.system("mpv ode_to_joy.webm")

## Load Images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player's player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

## Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))

# Player's laser
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Load bg
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

class Ship:
	def __init__(self, x, y, health=100):
		self.x = x
		self.y = y
		self.health = health
		self.ship_img = None
		self.laser_img = None
		self.lasers = []
		self.cool_down_counter = 0

	def draw(self, window):
		window.blit(self.ship_img, (self.x, self.y))

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()

class Player(Ship):
	def __init__(self, x, y, health=100):
		super().__init__(x, y, health)
		self.ship_img = YELLOW_SPACE_SHIP
		self.laser_img = YELLOW_LASER
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.max_health = health

class Enemy(Ship):
	COLOR_MAP = {
		"red": (RED_SPACE_SHIP, RED_LASER),
		"green": (GREEN_SPACE_SHIP, GREEN_SPACE_SHIP),
		"blue": (BLUE_SPACE_SHIP, BLUE_SPACE_SHIP)
	}
	def __init__(self, x, y, color, health=100):
		super().__init__(x, y, health)
		self.ship_img, self.laser_img = self.COLOR_MAP[color]
		self.mask = pygame.mask.from_surface(self.ship_img)

	def move(self, vel):
		self.y += vel

def main():
	run = True
	FPS = 20
	level = 0
	lives = 5
	main_font = pygame.font.SysFont("comicsans", 50)
	lost_font = pygame.font.SysFont("comicsans", 50)
	enemies = []
	wave_length = 5
	enemy_vel = 5
	player_vel = 10
	player = Player(300, 650)
	clock = pygame.time.Clock()
	lost = False

	def redraw_window():
		WIN.blit(BG, (0,0))
		# Draw info(lives, levels, etc.)
		lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
		level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
		WIN.blit(lives_label, (10, 10))
		WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
		for enemy in enemies:
			enemy.draw(WIN)

		player.draw(WIN)

		if lost:
			lost_label = lost_font.render("You Lost :(", 1, (255, 255, 255))
			WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

		pygame.display.update()

	while run:
		clock.tick(FPS)

		if lives <= 0 or player.health <=0:
			lost = True

		if len(enemies) == 0:
			level += 1
			wave_length += 5
			for i in range(wave_length):
				enemy = Enemy(random.randrange(0, WIDTH-100), random.randrange(-1500*level, -100), random.choice(["red", "blue", "green"]))
				enemies.append(enemy)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] or keys[pygame.K_h] or keys[pygame.K_LEFT] and player.x - player_vel > 0:
			player.x -= player_vel
		
		if keys[pygame.K_d] or keys[pygame.K_l] or keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
			player.x += player_vel

		if keys[pygame.K_w] or keys[pygame.K_k] or keys[pygame.K_UP] and player.y - player_vel > 0:
			player.y -= player_vel
		
		if keys[pygame.K_s] or keys[pygame.K_j] or keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < HEIGHT:
			player.y += player_vel

		for enemy in enemies[:]:
			enemy.move(enemy_vel)
			if enemy.y + enemy.get_height() > HEIGHT:
				enemies.remove(enemy)

		redraw_window()
main()