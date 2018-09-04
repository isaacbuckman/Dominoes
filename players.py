def human(game_state):
	print("---------Player %i------------" % (game_state.player_to_move))
	print("board:")
	print(game_state.ends)
	print('\n') 
	print(game_state.player_hands[game_state.player_to_move])
	moves = game_state.get_moves()
	print(moves)

	index = int(input("type index of array      "))
	return moves[index]
