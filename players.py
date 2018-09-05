import random

def human(game_state):
	print("---------Player %i------------" % (game_state.player_to_move))
	print("board:")
	print(game_state.ends)
	print('\n') 
	print(game_state.player_hands[game_state.player_to_move])
	moves = game_state.get_moves()
	print(moves)

	index = int(input("Array index of move:      "))
	return moves[index]

def greedy(game_state):
	max, max_value = None, None
	for move in game_state.get_moves():
		if max_value == None or move[0].total_pips() > max_value:
			max = move
			max_value = move[0].total_pips()
	return max

def rand(game_state):
	return random.choice(game_state.get_moves())