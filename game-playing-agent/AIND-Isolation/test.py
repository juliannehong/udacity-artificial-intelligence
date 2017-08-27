from isolation import Board
from game_agent import MinimaxPlayer, AlphaBetaPlayer

# create an isolation board (by default 7x7)
def test1():
	player1 = MinimaxPlayer()
	player2 = MinimaxPlayer()
	game = Board(player1, player2)
	# game.apply_move((1,1))
	# game.apply_move((2,2))
	# print (game._board_state)
	# print(game.to_string())
	# print(len(game._board_state))

	explored = [9,11,12,14,15,16,17,20,24,25,29,30,33,38,39,44]
	for i in explored:
		game._board_state[i] = 1
	game._board_state[-1] = 17
	game._board_state[-2] = 9


	# game.apply_move((5, 3)) # player 1
	# game.apply_move((4, 2)) # player 2

	print (game.to_string())
	moves = game.get_legal_moves()
	print(moves)
	for m in moves:
		fm = game.forecast_move(m).get_legal_moves()
		print (str(m) + " -->" + str(fm))

	# player 1
	for m in moves:
		print (str(m) + " --> " + str(player1.score(game.forecast_move(m), player1)))
	print (player1.get_move(game, 6))

def test2():
	player1 = AlphaBetaPlayer()
	player2 = AlphaBetaPlayer()
	game = Board(player1, player2, 9, 9)
	game._board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 22]
	#print(player1.get_move(game, 6))
	
	moves = game.get_legal_moves()
	for m in moves:
		fm = game.forecast_move(m).get_legal_moves()
		print (str(m) + " -->" + str(fm) + str(player1.score(game.forecast_move(m),player1)))
	print (player1.get_move(game, 6))

if __name__ == "__main__":
	test2()
