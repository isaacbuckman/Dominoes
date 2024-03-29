class ZeroSumGame():
    def __init__(self):
        pass
    def is_end(self):
        raise NotImplemented()
    def make_move(self, player, move):
        raise NotImplemented()
    def undo_move(self, player, move):
        raise NotImplemented()
    def possible_actions(self, player):
        raise NotImplemented()
    def evaluate(self, player):
        raise NotImplemented()
    def get_next_player(self, player):
        raise NotImplemented()

MAX_SCORE = 1000
class NegaMax:
    def __init__(self, curr_game, MAX_DEPTH = 10):
        self.curr_game = curr_game
        assert isinstance(curr_game, ZeroSumGame)

    def negamax(self, depth, player):
        cg = self.curr_game
        if depth==0 or cg.is_end():
            return None, cg.evaluate(player)

        max_move, max_score = None, None
        for move in cg.possible_actions(player):
            cg.make_move(player, move)
            curr_move, curr_score = self.negamax(depth-1, cg.get_next_player(player))
            curr_score = -curr_score
            if max_score is None or curr_score > max_score:
                max_move, max_score = move, curr_score
            cg.undo_move(player, move)
        return max_move, max_score

    def negamax_ab(self, depth, alpha, beta, player):
        # TODO: alpha-beta pruning
        cg = self.curr_game
        if depth==0 or cg.is_end():
            return None, cg.evaluate(player)

        max_move, max_score = None, None
        for move in cg.possible_actions(player):
            #cop = deepcopy(cg)
            cg.make_move(player, move)

            curr_move, curr_score = self.negamax_ab(depth-1, -beta, -alpha, cg.get_next_player(player))
            curr_score = -curr_score

            if max_score is None or curr_score > max_score:
                max_move, max_score = move, curr_score
            alpha = max(alpha, curr_score)
            cg.undo_move(player, move)
            if alpha >= beta:
                break
            #cop.is_equal(cg)
        return max_move, max_score
