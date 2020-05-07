from __future__ import annotations
from abc import ABC, abstractmethod
import random


class BearHuntException(Exception):
	"""
	base class for all BearHunt exceptions
	"""
	pass


class WorldAlreadyBeenGenerated(BearHuntException):
	pass


class Location:
	def __init__(self, i: int, j: int):
		self.i = i
		self.j = j

	def __add__(self, other: tuple) -> Location:
		"""
		Gets a tuple represents the delta between current location to wanted location and creates the wanted location
		:param other: tuple (i, j) represents the delta between current location to wanted location
		:return: wanted location
		"""
		self.i += other[0]
		self.j += other[1]
		return Location(self.i + other[0], self.j + other[1])

	def __eq__(self, other: Location) -> bool:
		"""
		Checks whether the locations are identical
		:param other: other location
		:return: True if other represents same location as self, False otherwise
		"""
		return self.i == other.i and self.j == other.j

	def __repr__(self):
		return f'<Location ({self.i}, {self.j})>'


class Entity(ABC):
	def __init__(self, location):
		self.location = location


class Food(Entity):
	@abstractmethod
	def be_eaten_by_a_bear(self, bear):
		pass


class Honey(Food):
	LIFE_POINTS = 5

	def be_eaten_by_a_bear(self, bear: Bear) -> bool:
		"""
		Gets a bear, if it should eat honey changes its life points and returns True, else returns False
		:param bear: a bear
		:return: True if honey has been eaten, False otherwise
		"""
		if bear.should_eat_honey():
			bear.change_life_points(self.LIFE_POINTS)
			bear.ate_honey = True
			return True
		return False


class Bear(Entity):
	class _DIRECTIONS:
		NORTH = (-1, 0)
		SOUTH = (1, 0)
		EAST = (0, -1)
		WEST = (0, 1)
		ALL = [NORTH, SOUTH, EAST, WEST]

	TURN_LIFE_POINTS = 1

	def __init__(self, name: str, location: Location = None, activity: float = None, smell: float = None,
	             impulsiveness: float = None, cowardice: float = None):
		"""
		A bear object
		:param name: bear's name
		:param location: bear's location
		:param activity: bear's activity value - if None, sets a random value
		:param smell: bear's smell value - if None, sets a random value
		:param impulsiveness: bear's impulsiveness value - if None, sets a random value
		:param cowardice: bear's cowardice value - if None, sets a random value
		"""
		super(Bear, self).__init__(location)
		self._name = name
		self._direction = None
		self._life_points = 100
		self.activity = self._get_characteristic(activity)
		self.smell = self._get_characteristic(smell)
		self.impulsiveness = self._get_characteristic(impulsiveness)
		self.cowardice = self._get_characteristic(cowardice)
		self.ate_honey = False

	@staticmethod
	def _get_characteristic(characteristic: float) -> float:
		"""
		Random bear characteristic value (a number between 1 to 0) if given characteristic is None, else return characteristic
		:param characteristic: characteristic value
		:return: random or given characteristic
		"""
		if characteristic is None:
			return random.random()
		return characteristic

	def change_life_points(self, delta: int) -> None:
		"""
		Gets number of points (can be negative number) to add to self life point and adds it.
		Validates life_points won't get over 100 points
		:param delta: life points to add
		:return: None
		"""
		life_points = self._life_points + delta
		self._life_points = life_points if life_points <= 100 else 100

	def start_a_turn(self) -> None:
		"""
		Starts a turn. Decreases constant value of life points
		:return: None
		"""
		self.change_life_points(self.TURN_LIFE_POINTS * (-1))

	@staticmethod
	def make_a_decision(characteristic_value: float) -> bool:
		"""
		Gets characteristic value, returns True if random number is lower than given characteristic_value, else returns False
		:param characteristic_value: a bear characteristic value
		:return: True if the decision is Yes, False if the decision is No
		"""
		return random.random() <= characteristic_value

	def should_move(self) -> bool:
		"""
		Decides whether to move or not
		:return: True if answer is Yes, False if answer is No
		"""
		if self.ate_honey:
			self.ate_honey = False
			return self.make_a_decision(self.activity * (1 / 3))
		return self.make_a_decision(self.activity)

	def should_eat_honey(self) -> bool:
		"""
		Decides whether to eat honey or not
		:return: True if answer is Yes, False if answer is No
		"""
		return self.make_a_decision(self.smell)

	def should_fight(self) -> bool:
		"""
		Decides whether to fight or not
		:return: True if answer is Yes, False if answer is No
		"""
		return self.make_a_decision(self.impulsiveness)

	def should_avoid_fight(self) -> bool:
		"""
		Decides whether to avoid a fight or not
		:return: True if answer is Yes, False if answer is No
		"""
		return self.make_a_decision(self.cowardice)

	def give_points_for_fight_avoidance(self, other_bear: Bear) -> None:
		"""
		Gets another bear, decreases self life points by 10 percents, increases other bear life points by 10 percents.
		:param other_bear: other bear to give points
		:return: None
		"""
		points = int(self._life_points * 0.1)
		self._life_points -= points
		other_bear.change_life_points(points)

	def _fix_location(self, board_size: int) -> None:
		"""
		Fix location if bear is out of range
		:param board_size: size of the board
		:return: None
		"""
		if self.location.i > board_size - 1:
			self.location.i = 0
		elif self.location.i < 0:
			self.location.i = board_size - 1

		if self.location.j > board_size - 1:
			self.location.j = 0
		elif self.location.j < 0:
			self.location.j = board_size - 1

	def is_dead(self) -> bool:
		"""
		Checks if bear is dead. Bear is dead if its life points number is lower than 0
		:return: True if the bear is dead, False if its alive
		"""
		return self._life_points <= 0

	def move(self, board_size: int) -> None:
		"""
		If bear should move, moves the bear to its wanted location
		:param board_size: size of the board
		:return: None
		"""
		if self.should_move():
			if self._direction is None:
				self._direction = random.choice(self._DIRECTIONS.ALL)
			self.location += self._direction
			self._fix_location(board_size)
		else:
			self._direction = None

	def random_fight_number(self) -> int:
		"""
		random a fight number between 0 and self life points
		:return: life number
		"""
		return random.randint(0, self._life_points)

	def fight(self, other_bear: Bear) -> bool:
		"""
		Gets a bear and performs a fight.
		:param other_bear: bear to fight
		:return: True if self won, False if the given bear won
		"""
		self_number = None
		other_number = None
		while self_number == other_number:
			self_number = self.random_fight_number()
			other_number = other_bear.random_fight_number()

		if self_number > other_number:
			other_bear.change_life_points(self_number * (-1))
			self.change_life_points(other_number)
			return True

		self.change_life_points(other_number * (-1))
		other_bear.change_life_points(self_number)
		return False

	def _get_child_characteristic_value(self, other_bear: Bear, characteristic: str) -> float:
		"""
		Generates a child characteristic.
		:param other_bear: other parent
		:param characteristic: the *name* of wanted characteristic ('activity', 'smell', ...)
		:return: child characteristic value
		"""
		return getattr(random.choice([self, other_bear]), characteristic) + random.gauss(0, 0.01)

	def create_new_bear(self, name: str, other_bear: Bear) -> Bear:
		"""
		Creates a new bear that its parents are self and given other_bear
		:param name: child name
		:param other_bear: another parent
		:return: child bear
		"""
		return Bear(
			name=name,
			activity=self._get_child_characteristic_value(other_bear, 'activity'),
			smell=self._get_child_characteristic_value(other_bear, 'smell'),
			impulsiveness=self._get_child_characteristic_value(other_bear, 'impulsiveness'),
			cowardice=self._get_child_characteristic_value(other_bear, 'cowardice')
		)

	def __repr__(self):
		return f"""< Bear {self._name}: life points: {self._life_points}
	activity: {self.activity}
	smell: {self.smell}
	impulsiveness: {self.impulsiveness}
	cowardice: {self.cowardice} >"""


class Game:
	_BEARS_UNITS = 1
	_HONEY_UNITS = 2

	CHARS = {
		Bear: 'B',
		Honey: 'H',
		type(None): '0'
	}

	def __init__(self, size: int):
		"""
		Game object.
		:param size: board size
		"""
		self._size = size
		self._bears = []
		self._foods = []

	def generate_new_world(self, bears: list) -> None:
		"""
		Gets bears and places them and their food on the board
		:param bears: list of bears
		:return: None
		"""
		bears_amount = len(bears) * self._BEARS_UNITS
		honey_jars_amount = len(bears) * self._HONEY_UNITS
		entities_amount = bears_amount + honey_jars_amount
		if entities_amount > self._size ** 2:
			raise ValueError('number of entities cannot be higher than number of cells')

		if self._bears:
			raise WorldAlreadyBeenGenerated(f'existing bears: {self._bears}')

		self._bears = bears
		for bear in self._bears:
			bear.location = self._random_empty_cell()

		for _ in range(honey_jars_amount):
			self._foods.append(Honey(location=self._random_empty_cell()))

	def _get_entity(self, location: Location, except_entity: Entity = None) -> Entity:
		"""
		Finds the entity that takes the given location
		:param location: location of cell
		:param except_entity: if given, checks that the entity that was found is not 'except_entity'
		:return: entity placed on given location
		"""
		for entity in self._bears + self._foods:
			if entity.location == location and entity != except_entity:
				return entity

	def _is_empty_cell(self, location: Location) -> bool:
		"""
		Checks if a cell is empty or not
		:param location: cell location
		:return: True if its an empty cell, False if there is an entity placed on given locaiton
		"""
		return location not in [entity.location for entity in self._bears + self._foods if entity.location]

	def _random_empty_cell(self) -> Location:
		"""
		Randoms an empty cell location
		:return: empty location
		"""
		location = None
		while location is None or not self._is_empty_cell(location):
			location = Location(random.randint(0, self._size - 1), random.randint(0, self._size - 1))

		return location

	def _two_bears_fight(self, bear1: Bear, bear2: Bear) -> None:
		"""
		Gets two bears and performs a fight between them
		:param bear1: one bear
		:param bear2: another bear
		:return: None
		"""
		bear1_avoided = bear1.should_avoid_fight()
		bear2_avoided = bear2.should_avoid_fight()
		if bear1_avoided and bear2_avoided:
			bear1.location = self._random_empty_cell()
			bear2.location = self._random_empty_cell()
		elif bear1_avoided:
			bear1.give_points_for_fight_avoidance(bear2)
			bear1.location = self._random_empty_cell()
		elif bear2_avoided:
			bear2.give_points_for_fight_avoidance(bear1)
			bear2.location = self._random_empty_cell()
		else:
			bear1_won = bear1.fight(bear2)
			if bear1_won:
				bear2.location = self._random_empty_cell()
			else:
				bear1.location = self._random_empty_cell()

	def make_a_bear_turn(self, bear: Bear) -> None:
		"""
		Gets a bear and does its turn according to BearHunt rules
		:param bear: a bear
		:return: None
		"""
		bear.move(self._size)
		entity = self._get_entity(bear.location, except_entity=bear)

		if isinstance(entity, Bear):
			self._two_bears_fight(bear, entity)
			if entity.is_dead():
				self._bears.remove(entity)
		elif isinstance(entity, Food):
			if entity.be_eaten_by_a_bear(bear):
				self._foods.remove(entity)

		if bear.is_dead():
			self._bears.remove(bear)

	def play(self, rounds: int) -> list:
		"""
		Runs a game round as many times as given
		:param rounds: times to run the game
		:return: list of bears (the winners)
		"""
		for _ in range(rounds):
			for bear in self._bears:
				self.make_a_bear_turn(bear)
		return self._bears

	def print_world(self) -> None:
		"""
		prints the game board
		:return:
		"""
		for i in range(self._size):
			for j in range(self._size):
				entity = self._get_entity(Location(i, j))
				print(self.CHARS[type(entity)], ' ', end='')
			print()
		print('___' * self._size)


def main():
	bears = [Bear(f'{i}') for i in range(20)]
	print(*bears, sep='\n')
	game = Game(10)
	game.generate_new_world(bears)
	game.print_world()
	winners = game.play(1000)
	game.print_world()
	print(*winners, sep='\n')
	if len(winners) > 3:
		print('Next generation game:')
		winners.sort(key=lambda bear: bear._life_points, reverse=True)
		b1 = winners[0].create_new_bear('b1', winners[1])
		b2 = winners[2].create_new_bear('b2', winners[3])
		game = Game(3)
		game.generate_new_world([b1, b2])
		game.print_world()
		winners = game.play(400)
		game.print_world()
		print(*winners, sep='\n')


if __name__ == '__main__':
	main()
