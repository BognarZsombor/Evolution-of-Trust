import pygame
import sys
import abc
import random
import time
import math
import threading
from copy import deepcopy

class Person(abc.ABC):

	persons = []
	radius = 10
	speed = 5
	screen = None

	#colors
	c_red = (179, 27, 0)
	c_green = (0, 179, 18)
	c_black = (0, 0, 0)
	c_pink = (227, 0, 227)
	c_blue = (0, 181, 217)

	def __init__(self, color, pos, dir):
		self.dir = dir
		self.pos = pos
		self.collide = False
		self.last_collided = None
		self.color = color
		Person.persons.append(self)

	def draw(self, color):
		pygame.draw.circle(Person.screen, color, (self.pos[0], self.pos[1]), Person.radius)

	def new_dir(self):
		new_dir = random.randrange(0, 3)
		# right turn
		if new_dir == 0:
			self.dir[0], self.dir[1] = -self.dir[1], self.dir[0]
		# left turn
		elif new_dir == 1:
			self.dir[0], self.dir[1] = self.dir[1], -self.dir[0]
		# else go forward the same way -> no change

	def move(self):
		self.out_of_map()
		self.pos[0] += self.dir[0] * Person.speed
		self.pos[1] += self.dir[1] * Person.speed

	def out_of_map(self):
		# left
		x, y = Person.screen.get_size()
		if self.pos[0] + self.dir[0] * Person.speed + Person.radius > x:
			self.dir[0], self.dir[1] = -self.dir[0], -self.dir[1]
		# right
		elif self.pos[0] + self.dir[0] * Person.speed - Person.radius < 0:
			self.dir[0], self.dir[1] = -self.dir[0], -self.dir[1]
		# top
		if self.pos[1] + self.dir[1] * Person.speed + Person.radius > y:
			self.dir[0], self.dir[1] = -self.dir[0], -self.dir[1]
		# bottom
		elif self.pos[1] + self.dir[1] * Person.speed - Person.radius < 0:
			self.dir[0], self.dir[1] = -self.dir[0], -self.dir[1]

	def move_in_one(self):
		if not self.collide:
			self.new_dir()
			self.move()
			self.draw(self.color)
			t1 = threading.Thread(target=self.collision, args=[3])
			t1.start()
		else:
			self.draw(self.color)

	def collision(self, num):
		for x in Person.persons:
			if x != self and self.last_collided != x and not x.collide:
				if math.sqrt((self.pos[0] - x.pos[0]) ** 2 + (self.pos[1] - x.pos[1]) ** 2) < Person.radius * 2:
					self.last_collided = x
					self.collide = True
					x.last_collided = self
					x.collide = True
					self.check_points(x, 10)
					x.check_points(self, 10)

					time.sleep(num)
					self.collide = False
					x.collide = False
					self.dir[0], self.dir[1] = -self.dir[0], -self.dir[1]
					x.dir[0], x.dir[1] = -x.dir[0], -x.dir[1]

	@abc.abstractmethod
	def check_points(self, x, num):
		"""child method"""

	@staticmethod
	def check_evolution(time_v = 30):
		while len(Person.persons) > 0:
			time.sleep(time_v)
			num = round(len(Person.persons)/10)
			best_num = sorted(Person.persons, key=lambda x: x.points, reverse=True)[:num]
			print(f"Best: {best_num}")
			worst_num = sorted(Person.persons, key=lambda x: x.points, reverse=False)[:num]
			print(f"Worst: {worst_num[::-1]}\n")

			for x in best_num:
				x.__class__([random.randrange(50,450), random.randrange(50,450)])
			for x in worst_num:
				Person.persons.remove(x)
				x.__class__.persons.remove(x)

			for x in Person.persons:
				x.points = 0

			Black.points = 0
			Pink.points = 0
			Blue.points = 0
			# change when adding new person

class Black(Person):

	persons = []
	points = 0

	def __init__(self, pos = [10, 10], dir = [0, 1], points = 0):
		super(Black, self).__init__(Person.c_black, pos, dir)
		self.points = points
		Black.persons.append(self)

	def __str__(self):
		return f"Black; {self.points}p; {self.pos}"

	def __repr__(self):
		return f"Black; {self.points}p; {self.pos}"

	def check_points(self, x, num):
		if x.__class__.__name__ == "Black":
			self.points += 0 * num
			Black.points += 0 * num
		elif x.__class__.__name__ == "Pink":
			self.points += 3 * num
			Black.points += 3 * num
		elif x.__class__.__name__ == "Blue":
			self.points += 3 + 0 * num
			Pink.points += 3 + 0 * num
	# change when adding new person

class Pink(Person):

	persons = []
	points = 0

	def __init__(self, pos = [10, 10], dir = [0, 1], points = 0):
		super(Pink, self).__init__(Person.c_pink, pos, dir)
		self.points = points
		Pink.persons.append(self)

	def __str__(self):
		return f"Pink; {self.points}p; {self.pos}"

	def __repr__(self):
		return f"Pink; {self.points}p; {self.pos}"

	def check_points(self, x, num):
		if x.__class__.__name__ == "Black":
			self.points += -1 * num
			Pink.points += -1 * num
		elif x.__class__.__name__ == "Pink":
			self.points += 2 * num
			Pink.points += 2 * num
		elif x.__class__.__name__ == "Blue":
			self.points += 2 * num
			Pink.points += 2 * num
	# change when adding new person

class Blue(Person):

	persons = []
	points = 0

	def __init__(self, pos = [10, 10], dir = [0, 1], points = 0):
		super(Blue, self).__init__(Person.c_blue, pos, dir)
		# change when adding new person
		self.points = points
		Blue.persons.append(self)
		# change when adding new person

	def __str__(self):
		return f"Blue; {self.points}p; {self.pos}"

	def __repr__(self):
		return f"Blue; {self.points}p; {self.pos}"

	def check_points(self, x, num):
		if x.__class__.__name__ == "Black":
			self.points += -3 + 0 * num
			Blue.points += -3 + 0 * num
		elif x.__class__.__name__ == "Pink":
			self.points += 2 * num
			Blue.points += 2 * num
		elif x.__class__.__name__ == "Blue":
			self.points += 2 * num
			Blue.points += 2 * num
	# change when adding new person

def exit():
	for x in Person.persons:
		del x
	pygame.quit()
	sys.exit()

def main():
	# init
	pygame.init()
	screen = pygame.display.set_mode((500,500), pygame.RESIZABLE)
	pygame.display.set_caption("Evolution of Trust Simulation")
	pygame.font.init()
	font = pygame.font.SysFont('Times New Roman', 18)
	Person.screen = screen

	# prepare
	actual_person = None
	prepare = True
	while prepare:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					actual_person = Black
				if event.key == pygame.K_s:
					actual_person = Pink
				if event.key == pygame.K_d:
					actual_person = Blue
		# change when adding new person
				if event.key == pygame.K_c:
					actual_person = None
				if event.key == pygame.K_r:
					prepare = False
			if event.type == pygame.MOUSEBUTTONUP and actual_person != None:
				pos = list(pygame.mouse.get_pos())
				actual_person(pos)
			if event.type == pygame.VIDEORESIZE:
				scr_size = event.size
				screen = pygame.display.set_mode(scr_size, pygame.RESIZABLE)

		screen.fill((255,255,255))
		text_surface = font.render(f"Press 'A' for 'Black' person", False, Person.c_black)
		screen.blit(text_surface, (5, 0))
		text_surface = font.render(f"Press 'S' for 'Pink' person", False, Person.c_black)
		screen.blit(text_surface, (5, 20))
		text_surface = font.render(f"Press 'D' for 'Blue' person", False, Person.c_black)
		screen.blit(text_surface, (5, 40))
		# change when adding new person

		for person in Person.persons:
			person.draw(person.color)

		pygame.display.flip()

	# simulation
	t1 = threading.Thread(target=Person.persons[0].check_evolution, args=[10])
	t1.daemon = True
	t1.start()

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

		screen.fill((255,255,255))
		text_surface = font.render(f"{Black.points} points for 'Black'", False, Person.c_black)
		screen.blit(text_surface, (5, 0))
		text_surface = font.render(f"{Pink.points} points for 'Pink'", False, Person.c_black)
		screen.blit(text_surface, (5, 20))
		text_surface = font.render(f"{Blue.points} points for 'Blue'", False, Person.c_black)
		screen.blit(text_surface, (5, 40))
		text_surface = font.render(f"{len(Black.persons)} 'Black' person", False, Person.c_black)
		screen.blit(text_surface, (5, 60))
		text_surface = font.render(f"{len(Pink.persons)} 'Pink' person", False, Person.c_black)
		screen.blit(text_surface, (5, 80))
		text_surface = font.render(f"{len(Blue.persons)} 'Blue' person", False, Person.c_black)
		screen.blit(text_surface, (5, 100))
		# change when adding new person

		for person in Person.persons:
			person.move_in_one()

		pygame.display.flip()

		#time.sleep(1/10)

	exit()

main()
