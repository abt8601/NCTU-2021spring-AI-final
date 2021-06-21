import random
from typing import Optional
import othello
from log_referee import LogReferee
import evaluation

from random_agent import RandomAgent
from max_agent import MaxAgent
from minimax_agent import MinimaxAgent
from alpha_beta_agent import AlphaBetaAgent
from expectimax_agent import ExpectimaxAgent
from mcts_agent import MCTSAgent

class TestRandomAgent(unittest.TestCase):
    def test_random_agent(self):
    	referee = LogReferee(RandomAgent(othello.Player.DARK),
                         RandomAgent(othello.Player.LIGHT))
    	referee.run()
        othello.Referee(RandomAgent(othello.Player.DARK),
                        RandomAgent(othello.Player.LIGHT)).run()

class TestMaxAgent(unittest.TestCase):
    def test_max_agent(self):
        othello.Referee(MaxAgent(othello.Player.DARK),
                        MaxAgent(othello.Player.LIGHT)).run()

class TestMinimaxAgent(unittest.TestCase):
    def test_minimax_agent(self):
        othello.Referee(MinimaxAgent(othello.Player.DARK),
                        MinimaxAgent(othello.Player.LIGHT)).run()

class TestAlphaBetaAgent(unittest.TestCase):
    def test_alpha_beta_agent(self):
        othello.Referee(AlphaBetaAgent(othello.Player.DARK),
                        AlphaBetaAgent(othello.Player.LIGHT)).run()

class TestExpectimaxAgent(unittest.TestCase):
    def test_expectimax_agent(self):
        othello.Referee(ExpectimaxAgent(othello.Player.DARK),
                        ExpectimaxAgent(othello.Player.LIGHT)).run()

class TestMCTSAgent(unittest.TestCase):
    def test_mcts_agent(self):
        othello.Referee(MCTSAgent(othello.Player.DARK),
                        MCTSAgent(othello.Player.LIGHT)).run()