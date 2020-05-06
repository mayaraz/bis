from typing import List

class Location:
	def __init__(self, row, column):
		self.row = row
		self.column = column


class IRobot:
	ON = 'on'
	OFF = 'off'
	RIGHT = 'right'
	LEFT = 'left'
	UP = 'up'
	DOWN = 'down'

	STATES = [ON, OFF]
	DIRECTIONS = [RIGHT, LEFT, UP, DOWN]

	EMPTY_BOARD = [
		['0', '0', '0', '0', '0'],
		['0', '0', '0', '0', '0'],
		['0', '0', '0', '0', '0'],
		['0', '0', '0', '0', '0'],
		['0', '0', '0', '0', '0']
	]

	def __init__(self):
		self._board = self.EMPTY_BOARD
		self._location = Location(0, 0)
		self._direction = None
		self._state = None

	def _get_instruction(self, instruction: str) -> any:
		"""
		Gets instruction, validates it and returns it converted to the right type
		:param instruction: user instruction
		:return: instruction
		"""
		if instruction in self.STATES or instruction in self.DIRECTIONS:
			return instruction
		elif instruction.isdigit():
			return int(instruction)
		raise ValueError()

	def _parse_instructions(self, instructions_input: str) -> List[str]:
		"""
		Parses user instructions
		:param instructions_input: user instructions
		:return: instructions list
		"""
		return [self._get_instruction(instruction) for instruction in instructions_input.split()]

	def _validate_step(self, step: tuple) -> None:
		"""
		Validates step is not out of range
		:param step: tuple of i, j indexes
		:return: None
		"""
		if not ((0 <= self._location.row + step[0] <= 4) and (0 <= self._location.column + step[1] <= 4)):
			raise IndexError()

	def _take_one_step(self) -> None:
		"""
		Takes one step, according to current direction and state
		:return: None
		"""
		if self._direction == self.RIGHT:
			step = (0, 1)
		elif self._direction == self.LEFT:
			step = (0, -1)
		elif self._direction == self.UP:
			step = (-1, 0)
		else:
			step = (1, 0)

		self._validate_step(step)
		self._location.row += step[0]
		self._location.column += step[1]

	def _take_steps(self, steps_amount: int) -> None:
		"""
		Gets steps amount and takes this amount of steps
		:param steps_amount: amount of steps
		:return: None
		"""
		for i in range(steps_amount):
			self._take_one_step()
			if self._state == self.ON:
				self._board[self._location.row][self._location.column] = 'X'

	def _run_instruction(self, instruction: str) -> None:
		"""
		Runs given instruction
		:param instruction: user instruction
		:return: None
		"""
		if instruction in self.STATES:
			self._state = instruction
		elif instruction in self.DIRECTIONS:
			self._direction = instruction
		elif isinstance(instruction, int):
			self._take_steps(instruction)
		else:
			raise ValueError

	def run(self, instructions_input: str) -> None:
		"""
		Gets instructions from user and runs all of them
		:param instructions_input: user instructions
		:return: None
		"""
		try:
			instructions = self._parse_instructions(instructions_input)
			for instruction in instructions:
				self._run_instruction(instruction)
			self.print_board()
		except ValueError:
			print('One of the given instructions is not allowed')
			print('Allowed instructions are:', *self.STATES, *self.DIRECTIONS,
			      'and any number indicates steps amount', sep='\n')
		except IndexError:
			print('IRobot cant get out of range, one of the instructions causing that.')

	def print_board(self) -> None:
		"""
		prints current board
		:return: None
		"""
		for row in self._board:
			print(*row, sep='  ')


def main():
	user_instructions = input('instructions: ')
	robot = IRobot()
	robot.run(user_instructions)


if __name__ == '__main__':
	main()

