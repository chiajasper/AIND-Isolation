"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest
from time import time
import isolation
import game_agent
from sample_players import GreedyPlayer

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)
        self.score_count = 0
        self.start = False
        self.listx = set()
        self.player_01 = None

    def time_left(self, allowedTime = 2000000.):
        future = time() + allowedTime
        def timer():
            return future - time()

        return timer
    #
    # def test_minMax(self):
    #     board = self.game = isolation.Board(game_agent.MinimaxPlayer(score_fn=game_agent.custom_score), GreedyPlayer())
    #     print(board.play(200000))
    #
    #     return True


    def score(self, game, player):
        self.score_count += 1
        if self.start and player == self.player_01:
            self.listx.add((game.get_player_location(player), game.get_player_location(game.get_opponent(player))))
        return 1.

    # def test_min_max(self):
    #     board = self.game = isolation.Board(player_1=game_agent.MinimaxPlayer(search_depth=2, score_fn=self.score), player_2 = GreedyPlayer(), width = 11, height = 11)
    #     board.mock(((2,1),(2,3),(2,4),(2,5),(4,2),(4,4),(4,5),(4,6),(5,7),(5,8),(6,3),(7,2),(7,3),(7,4),(7,7),(7,8),(8,2),(8,4),(8,5),(8,6),(5,3),(5,2)))
    #
    #     print(board.to_string())
    #     self.start = True
    #     board.active_player.get_move(board, self.time_left())
    #     print(self.score_count)
    #     #184 or 190


#       0   1   2   3   4   5   6   7   8   9   10
# 0   |   |   |   |   |   |   |   |   |   |   |   |
# 1   |   |   |   |   |   |   |   |   |   |   |   |
# 2   |   | - |   | - | - | - |   |   |   |   |   |
# 3   |   | y | x | y | x |   |   |   |   |   |   |
# 4   | y | x | - |   | - | - | - |   |   |   |   |
# 5   |   |   | 2 | 1 |   |   |   | - | - |   |   |
# 6   | y | x |   | - | y | x |   |   |   |   |   |
# 7   |   | y | - | - | - |   |   | - | - |   |   |
# 8   |   |   | - |   | - | - | - |   |   |   |   |
# 9   |   |   |   |   |   |   |   |   |   |   |   |
# 10  |   |   |   |   |   |   |   |   |   |   |   |
    def test_min_max2(self):
        self.player_01 = game_agent.MinimaxPlayer(search_depth=4, score_fn=self.score)
        board = self.game = isolation.Board(player_1= self.player_01, player_2 = GreedyPlayer(), width = 11, height = 11)
        board.mock(((1,2),(4,2),(4,3),(7,3),(5,4),(4,4),(3,4),(2,4),(6,5),(5,5),(2,5),(7,6),(6,6),(2,6),(7,7),(6,7),(5,7),(3,7),(2,7),(8,8),(7,8),(5,8),(4,8),(3,8),(8,9),(3,9),(8,7),(6,8)))
        print(board.to_string())
        self.start = True
        board.active_player.time_left = self.time_left()
        board.active_player.minimax(board, depth=4)
        print(self.listx)
        print(len(self.listx))
# Heuristic: center_distance
# Depth limit: 4
# Initial Board State:
#       0   1   2   3   4   5   6   7   8   9   10
# 0   |   |   |   |   |   |   |   |   |   |   |   |
# 1   |   |   | - |   |   |   |   |   |   |   |   |
# 2   |   |   |   |   | - | - | - | - |   |   |   |
# 3   |   |   |   |   | - |   |   | - | - | - |   |
# 4   |   |   | - | - | - |   |   |   | - |   |   |
# 5   |   |   |   |   | - | - |   | - | - |   |   |
# 6   |   |   |   |   |   | - | - | - | 2 |   |   |
# 7   |   |   |   | - |   |   | - | - | - |   |   |
# 8   |   |   |   |   |   |   |   | 1 | - | - |   |
# 9   |   |   |   |   |   |   |   |   |   |   |   |
# 10  |   |   |   |   |   |   |   |   |   |   |   |


if __name__ == '__main__':
    unittest.main()
