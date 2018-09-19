from framework import GameState, ismcts

import random
import collections
from copy import deepcopy

class Domino:
	def __init__(self, a, b):
		self.vals = (a,b) if a < b else (b,a)

	def total_pips(self):
		return sum(self.vals)

	def __contains__(self, x):
		return x in self.vals

	def __eq__(self, x):
		if x is None:
			return False
		return x.vals == self.vals

	def __str__(self):
		return "|%i|%i|" % (self.vals[0], self.vals[1])

	def __repr__(self):
		return str(self.vals)

class DominoGameState(GameState):

	def __init__(self):
		self.ends = [None, None]
		self.player_to_move = random.randint(1,4)
		self.player_hands = {player : [] for player in range(1, 5)}
		self.history_deque = collections.deque(4 * [None], 4)

		self._deal()

	def get_next_player(self):
		""" Return the player to the left of the specified player
		"""
		return (self.player_to_move % 4) + 1

	def clone(self):
		""" Create a deep clone of this game state.
		"""
		# clone = DominoGameState()
		# clone.ends = self.ends
		# clone.player_to_move = self.player_to_move
		# clone.player_hands = self.player_hands
		# clone.history_deque = self.history_deque

		# return clone
		return deepcopy(self)

	def clone_and_randomize(self, observer):
		""" Create a deep clone of this game state, randomizing any information not visible to the specified observer player.
		"""
		clone = self.clone()

		hidden_dominoes = []
		for player in range(1,5):
			if player != observer:
				hidden_dominoes += self.player_hands[player]
		random.shuffle(hidden_dominoes)
		for player in range(1,5):
			if player != observer:
				hand_size= len(self.player_hands[player])
				clone.player_hands[player] = hidden_dominoes[:hand_size]
				hidden_dominoes = hidden_dominoes[hand_size:] 
		return clone

	def do_move(self, move):
		""" update a state by carrying out the given move.
		Must update player_to_move.
		"""
		self.history_deque.appendleft(move[0])
		if move[0] == Domino(-1,-1):
			pass
		else:
			if self.ends == [None, None]:
				self.ends[0] = move[0].vals[0]
				self.ends[1] = move[0].vals[1]
			else:
				other_side = move[0].vals[0] if move[0].vals[1] == self.ends[move[1]] else move[0].vals[1]
				self.ends[move[1]] = other_side
			self.player_hands[self.player_to_move].remove(move[0])

		self.player_to_move = self.get_next_player()

	def get_moves(self):
		""" Get all possible moves from this state.
		"""
		hand = self.player_hands[self.player_to_move]
		if not hand:
			return []
		if self.ends == [None, None]:
			return [(tile, None) for tile in hand]
		moves = []
		for tile in hand:
			if self.ends[0] in tile:
				moves.append((tile,0))
			if self.ends[1] in tile:
				moves.append((tile,1))
		if not moves:
			moves.append((Domino(-1,-1), None))
		return moves

	def get_result(self, player):
		""" Get the game result from the viewpoint of player. 
		"""
		return len(self.player_hands[player]) == 0 or len(self.player_hands[((player + 1) % 4) + 1]) == 0

	def is_end(self):
		empty_hand = any(len(hand) == 0 for hand in self.player_hands.values())
		all_passed = all(move == Domino(-1,-1) for move in self.history_deque)
		return empty_hand or all_passed

	@staticmethod
	def _get_tiles():
		""" Construct 28 unique tiles.
		"""
		return [Domino(i,j) for i in range(7) for j in range(i,7)]

	def _deal(self):
		dominoes = self._get_tiles()
		random.shuffle(dominoes)

		for player in range(1, 5):
			self.player_hands[player] = dominoes[:7]
			dominoes = dominoes[7:]

	def __str__(self):
		for player in range(1, 5):
			print("Player %i:" % (player))
			print(self.player_hands[player])
		print("\n")
		print("Board:")
		print(str(self.ends))

	def __repr__(self):
		""" Don't need this - but good style.
		"""
		raise NotImplementedError