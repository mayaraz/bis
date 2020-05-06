from typing import List


class Game:
	DEAD = '0'
	LIVE = 'X'

	def __init__(self, board):
		self.board = board

	def _get_cell_state(self, i: int, j: int) -> str:
		"""
		Gets indexes of cell in the board and return it's new life state according the game rules
		:param i: row index
		:param j: column index
		:return: cell new life state
		"""
		neighbors = self._get_neighbors(i, j)
		live_cells_amount = neighbors.count(self.LIVE)
		if self.board[i][j] == self.LIVE:
			return self.LIVE if 2 <= live_cells_amount <= 3 else self.DEAD
		else:
			return self.LIVE if live_cells_amount == 3 else self.DEAD

	def _get_neighbors(self, i: int, j: int) -> List[str]:
		"""
		Gets cell indexes and returns list of it's neighbors values (life states)
		:param i: row index
		:param j: column index
		:return: neighbors list (str list)
		"""
		from_row = i - 1 if i != 0 else 0
		to_row = i + 2 if i != len(self.board) - 1 else len(self.board)

		from_column = j - 1 if j != 0 else 0
		to_column = j + 2 if j != len(self.board[j]) - 1 else len(self.board[j])

		neighbors = []
		for x in range(from_row, to_row):
			for y in range(from_column, to_column):
				if not (x == i and y == j):
					neighbors.append(self.board[x][y])

		return neighbors

	def _run_next_iteration(self) -> None:
		"""
		Sets new life state of all cells in board
		:return: None
		"""
		new_board = []
		for i in range(len(self.board)):
			row = []
			for j in range(len(self.board[0])):
				row.append(self._get_cell_state(i, j))
			new_board.append(row)
		self.board = new_board

	def print_board(self) -> None:
		"""
		prints current board
		:return: None
		"""
		for row in self.board:
			print(*row, sep='  ')

		print('___' * len(self.board))

	def run(self) -> None:
		"""
		Runs the game
		:return: None
		"""
		print('Game started')
		self.print_board()
		continue_running = True
		while continue_running:
			self._run_next_iteration()
			self.print_board()
			continue_running = input('Continue to next generation? [y]/n\n') != 'n'

		print('Finish game')


def main():
	game = Game(board=[
		['0', 'X', '0', '0', '0', '0', '0', '0', '0', '0'],
		['0', 'X', 'X', '0', '0', '0', '0', '0', '0', '0'],
		['0', 'X', '0', '0', '0', '0', '0', '0', '0', '0'],
		['0', '0', '0', 'X', '0', 'X', '0', '0', '0', '0'],
		['0', '0', '0', '0', 'X', '0', '0', '0', '0', '0'],
		['0', '0', '0', 'X', '0', 'X', '0', '0', '0', '0'],
		['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
		['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
		['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
		['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
	])
	game.run()


if __name__ == '__main__':
	main()
