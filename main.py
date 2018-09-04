from board import DominoGameState
from players import human

import random

state = DominoGameState()

while not state.is_end():
	m = human(state)
	state.do_move(m)

for player in range(1,5):
	print("player %i, %s" % (player, state.get_result(player)))