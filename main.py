from board import DominoGameState
from players import human, greedy, rand
from framework import ismcts

import random

results = []
for i in range(30):
	state = DominoGameState()

	while not state.is_end():
		# m = human(state)
		if state.player_to_move % 2 == 0:
			m = ismcts(state, 5000, quiet=True)
		else:
			m = ismcts(state, 1000, quiet=True)
		state.do_move(m)

	results.append(state.get_result(2))
	print("wins:",results.count(True))
	print("losses:",results.count(False))
	print()

# for player in range(1,5):
# 	print("player %i, %s" % (player, state.get_result(player)))