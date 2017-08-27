"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
from game_agent import MinimaxPlayer

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)

        player1 = MinimaxPlayer()
		player2 = MinimaxPlayer()
		game = Board(player1, player2)

		game.apply_move((2, 3))
		game.apply_move((0, 5))

		m1 = player1.get_move(game, 5)
		game.apply_move(m1)
		m2 = player2.get_move(game, 6)

		game.apply_move(m2)


	def test_1(self):
		self.
if __name__ == '__main__':
    unittest.main()
