from domino import Dominoes, Domino
from algorithms.p_negamax import ProbabilisticNegaMax
import random
from copy import deepcopy
import sys
from numpy.random import choice

from algorithms.ISMCTS import ismcts
import time
import argparse

PASS_STR = 'PASS'
PASS_DOMINO = Domino(-1,-1)

def ISMCTS_plays(game, tiles, player, time_limit=None):
    curr_game = game[player]
    actions = curr_game.possible_actions(0)
    if len(actions) == 1:
        for g in games:
            g.update(actions[0][0])
        print "ISMCTS move (only choice): " + str(actions[0][0])
        if not actions[0][0] == PASS_DOMINO:
            tiles[player].remove(actions[0][0])
    else:
        if time_limit:
            my_move = ismcts(curr_game, time_limit=time_limit, verbose=True, quiet=False)
        else:
            my_move = ismcts(curr_game, verbose=False, quiet=True)
        for g in games:
            g.update(my_move[0], placement=my_move[1])
        print "ISMCTS move: " + str(my_move[0])
        if not my_move[0] == PASS_DOMINO:
            tiles[player].remove(my_move[0])
    return tiles, None

def newSmartPlays(game, tiles, player):
    curr_game = game[player]
    actions = curr_game.possible_actions(0)
    if len(actions) == 1:
        for g in games:
            g.update(actions[0][0])
        print "move (only choice): " + str(actions[0][0])
        if not actions[0][0] == PASS_DOMINO:
            tiles[player].remove(actions[0][0])
        time_elapsed = None
    else:
        pnm = ProbabilisticNegaMax(curr_game)
        depth = int(5*(2**(1./3*int(len(curr_game.dominos_played)/4))))
        print "depth: ", depth
        max_move, max_expectation = None, None
        start_time = time.time()
        for a in actions:
            curr_expectation = calculate_expectation(curr_game, depth, a)
            if max_move is None or max_expectation < curr_expectation:
                max_move, max_expectation = a, curr_expectation
                print 'new max found with expectation: {}'.format(max_expectation)
        end_time = time.time()
        time_elapsed = end_time - start_time
        # max_move, max_score = pnm.p_negamax(6,0)
        for g in games:
            g.update(max_move[0], placement=max_move[1])
        print "move: " + str(max_move[0])
        if not max_move[0] == PASS_DOMINO:
            tiles[player].remove(max_move[0])
    return tiles, time_elapsed

def oldSmartPlays(game, tiles, player):
    curr_game = game[player]
    actions = curr_game.possible_actions(0)
    if len(actions) == 1:
        for g in games:
            g.update(actions[0][0])
        print "move (only choice): " + str(actions[0][0])
        if not actions[0][0] == PASS_DOMINO:
            tiles[player].remove(actions[0][0])
        time_elapsed = None
    else:
        pnm = ProbabilisticNegaMax(curr_game)
        depth = int(5*(2**(1./3*int(len(curr_game.dominos_played)/4))))
        print "depth: ", depth
        start_time = time.time()
        max_move, max_score = pnm.p_negamax_ab(depth, depth, -float("inf"), float("inf"), 0)
        # max_move, max_score = pnm.p_negamax(6,0)
        end_time = time.time()
        time_elapsed = end_time - start_time
        for g in games:
            g.update(max_move[0], placement=max_move[1])
        print "move: " + str(max_move[0])
        if not max_move[0] == PASS_DOMINO:
            tiles[player].remove(max_move[0])
    return tiles, time_elapsed

def greedyPlays(game, tiles, player):
    print "GREEDY"
    curr_game = game[player]
    actions = curr_game.possible_actions(0, placements_included=False)
    if len(actions) == 1:
        if len(curr_game.possible_actions(0, placements_included=True)) > 1:
            placement = random.choice((0,1))
            for g in games:
                g.update(actions[0], placement=placement)
        else:
            for g in games:
                g.update(actions[0])
        print "move (only choice): " + str(actions[0])
        if not actions[0] == PASS_DOMINO:
            tiles[player].remove(actions[0])
    else:
        domino, max_value = None, None
        for d in actions:
            if max_value == None or d.vals[1] + d.vals[0] > max_value:
                max_value = d.vals[1] + d.vals[0]
                domino = d
        if (curr_game.ends[0] in domino and curr_game.ends[1] in domino and curr_game.ends[0] != curr_game.ends[1]):
            placement = random.choice((0, 1))
            for g in games:
                g.update(domino, placement=placement)
        else:
            for g in games:
                g.update(domino)
        print "move: ", domino
        if not domino == PASS_DOMINO:
            tiles[player].remove(domino)
    return tiles, None

def randomPlays(game, tiles, player):
    print "RANDOM"
    curr_game = game[player]
    actions = curr_game.possible_actions(0, placements_included=False)
    if len(actions) == 1:
        if len(curr_game.possible_actions(0, placements_included=True)) > 1:
            placement = random.choice((0,1))
            for g in games:
                g.update(actions[0], placement=placement)
        else:
            for g in games:
                g.update(actions[0])
        print "move (only choice): " + str(actions[0])
        if not actions[0] == PASS_DOMINO:
            tiles[player].remove(actions[0])
    else:
        domino = random.choice(actions)
        if (curr_game.ends[0] in domino and curr_game.ends[1] in domino and curr_game.ends[0] != curr_game.ends[1]):
            placement = random.choice((0, 1))
            for g in games:
                g.update(domino, placement=placement)
        else:
            for g in games:
                g.update(domino)
        print "move: ", domino
        if not domino == PASS_DOMINO:
            tiles[player].remove(domino)
    return tiles, None

def calculate_expectation(game, depth, move, samples=50):
    exp_total = 0.0
    remaining_dominoes = make_dominoes()
    players = range(4)
    pnm = ProbabilisticNegaMax(game)
    game.make_probabilistic_move(0, move)
    for t in game.dominos_played:
        if not t == PASS_DOMINO:
            remaining_dominoes.remove(t)
    for _ in range(samples):
        curr_dominoes = list(remaining_dominoes)
        random.shuffle(curr_dominoes)
        old_probabilities = deepcopy(game.probabilities)
        while curr_dominoes:
            curr_domino = curr_dominoes.pop()
            curr_domino_probs = game.probabilities[curr_domino]
            curr_assignment = choice(players, p=curr_domino_probs)
            game._update_probs(curr_domino, curr_assignment)
        exp_total += -pnm.p_negamax_ab(depth, depth, -float('inf'), float('inf'), 1)[1]
        game.probabilities = old_probabilities
    game.undo_move(0, move)
    exp_total /= samples
    return exp_total

def make_dominoes():
    return set(Domino(i,j) for i in range(7) for j in range(i,7))

def setupGame(r):
    # print 'Welcome.'
    tiles = []
    for i in range(7):
        for j in range(i, 7):
            tiles.append((i, j))
    random.shuffle(tiles)
    my_tiles = tiles[:7]
    print 'Players are numbered as the following:'
    print '0 = me, 1 = opponent on my right, 2 = partner across from me, 3 = opponent on my left'
    print
    print 'Player 0 has: ', my_tiles
    players_tiles = {}
    players_tuples = [None]*4
    players_tiles[0] = set(map(lambda x:Domino(*x), my_tiles))
    players_tuples[0] = my_tiles
    for i in range(1, 4):
        this_players_tiles = tiles[7*i:7*(i+1)]
        print 'Player ' + str(i) + ' has: ', this_players_tiles
        players_tiles[i] = set(map(lambda x:Domino(*x), this_players_tiles))
        players_tuples[i] = this_players_tiles
    starter = r % 4
    print "Player " + str(starter) + " is starting."
    print
    return ((Dominoes(tiles, my_tiles, starter),
        Dominoes(tiles, players_tuples[1], (starter-1)%4),
        Dominoes(tiles, players_tuples[2], (starter-2)%4),
        Dominoes(tiles, players_tuples[3], (starter-3)%4)),
        players_tiles)

# def computeScore(game, players_tiles):
#     player_pips = [0]*4
#     # count tiles of each player
#     for t in game.my_tiles:
#         if t not in game.dominos_played:
#             player_pips[0] += sum(t.vals)
#     for i in range(1, 4):
#         for t in players_tiles[i]:
#             if t not in game.dominos_played:
#                 player_pips[i] += sum(t.vals)

#     for i in range(4):
#         print 'Player {} has pips {}'.format(i, player_pips[i])
#     if (player_pips[0] == 0 or player_pips[2] == 0 or
#         player_pips[0]+player_pips[2] < player_pips[1] + player_pips[3]):
#         print 'I win!'
#         return 'won'
#     if (player_pips[1] == 0 or player_pips[3] == 0 or
#         player_pips[0]+player_pips[2] > player_pips[1] + player_pips[3]):
#         print 'I lose :('
#         return 'lost'
#     if player_pips[0]+player_pips[2] == player_pips[1] + player_pips[3]:
#         print 'we tied?!'
#         return 'tie'
#     print "SCORES:"
#     print "smart + greedy", score_us
#     print "greedy + greedy", score_opp
#     if score_us < score_opp:
#         return "won"
#     elif score_opp < score_us:
#         return "lost"
#     else:
#         return "tie"
#     for t in game.my_tiles:
#         if t not in game.dominos_played:
#             score_us += sum(t.vals)
#     for i in range(1, 4):
#         for t in players_tiles[i]:
#             if t not in game.dominos_played:
#                 if i % 2 == 0:
#                     score_us += sum(t.vals)
#                 else:
#                     score_opp += sum(t.vals)
#     print 'score is : {}'.format(q)
#     return 'won' if q>0 else 'lost'

def computeScore(game, players_tiles):
    if (len(players_tiles[0]) == 0 or len(players_tiles[2]) == 0):
        print 'I win!'
        return 'won'
    if (len(players_tiles[1]) == 0 or len(players_tiles[3]) == 0):
        print 'I lose :('
        return 'lost'

    player_pips = [0]*4
    # count tiles of each player
    for t in game.my_tiles:
        if t not in game.dominos_played:
            player_pips[0] += sum(t.vals)
    for i in range(1, 4):
        for t in players_tiles[i]:
            if t not in game.dominos_played:
                player_pips[i] += sum(t.vals)

    for i in range(4):
        print 'Player {} has pips {}'.format(i, player_pips[i])

    if (player_pips[0]+player_pips[2] < player_pips[1] + player_pips[3]):
        print 'I win!'
        return 'won'
    if (player_pips[0]+player_pips[2] > player_pips[1] + player_pips[3]):
        print 'I lose :('
        return 'lost'
    if player_pips[0]+player_pips[2] == player_pips[1] + player_pips[3]:
        print 'we tied?!'
        return 'tie'
    print "SCORES:"
    print "smart + greedy", score_us
    print "greedy + greedy", score_opp
    if score_us < score_opp:
        return "won"
    elif score_opp < score_us:
        return "lost"
    else:
        return "tie"
    for t in game.my_tiles:
        if t not in game.dominos_played:
            score_us += sum(t.vals)
    for i in range(1, 4):
        for t in players_tiles[i]:
            if t not in game.dominos_played:
                if i % 2 == 0:
                    score_us += sum(t.vals)
                else:
                    score_opp += sum(t.vals)
    print 'score is : {}'.format(q)
    return 'won' if q>0 else 'lost'

def get_dominoes_list(game, player, player_tiles):
    if player == 0:
        my_tiles = []
        for t in game.my_tiles:
            if t not in game.dominos_played:
                my_tiles.append(t)
        return my_tiles
    return [t for t in player_tiles[player] if t not in game.dominos_played]
# random.seed(96)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--rounds", help="number of rounds to play", type=int, default=10)
    parser.add_argument("player1", help="greedy, random, IMS, PIMC, or ISMCTS")
    parser.add_argument("player2", help="greedy, random, IMS, PIMC, or ISMCTS")
    args = parser.parse_args()
    players = {
        "greedy" : greedyPlays,
        "random" : randomPlays,
        "ims" : oldSmartPlays,
        "pimc" : newSmartPlays,
        "ismcts" : ISMCTS_plays
    }
    player1 = players[args.player1.lower()]
    player2 = players[args.player2.lower()]
    results = []
    for r in range(args.rounds): #100
        print "---------------ROUND ", r,"---------------"
        # games, players_tiles = setupGame(r)
        games, players_tiles = setupGame(random.randint(0,3))
        time_elapsed = None
        while not games[0].is_end():
            player = games[0].curr_player
            print 'player: ', str(player)
            print 'time_elapsed: ', time_elapsed
            # tiles, recent_time_elapsed = oldSmartPlays(games, players_tiles, player) if player%2==1 else ISMCTS_plays(games, players_tiles, player, time_limit=time_elapsed) 
            tiles, recent_time_elapsed = player2(games, players_tiles, player) if player%2==1 else player1(games, players_tiles, player)
            # tiles, recent_time_elapsed = player2(games, players_tiles, player) if player%2==1 else ISMCTS_plays(games, players_tiles, player, time_limit=20)
            if recent_time_elapsed != None:
                time_elapsed = recent_time_elapsed
            print 'ends: ', games[0].ends
            print 'remaining dominoes: {}'.format(sorted(list(players_tiles[player])))
            print
        results.append(computeScore(games[0], players_tiles))
        print "Game ended."
    print "-------------------STATS-------------------"
    print "{} vs {}".format(args.player1,args.player2)
    print "Number of wins:", results.count("won")
    print "Number of losses:", results.count("lost")
    print "Number of ties:", results.count("tie")