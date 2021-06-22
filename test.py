import random
from typing import Optional
import othello
from log_referee import LogReferee
import evaluation
import unittest

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

class TestMaxAgent(unittest.TestCase):
	def test_max_agent(self):
		referee = LogReferee(MaxAgent(othello.Player.DARK),
							 MaxAgent(othello.Player.LIGHT))
		referee.run()

class TestMinimaxAgent(unittest.TestCase):
	def test_minimax_agent(self):
		referee = LogReferee(MinimaxAgent(othello.Player.DARK),
							 MinimaxAgent(othello.Player.LIGHT))
		referee.run()

class TestAlphaBetaAgent(unittest.TestCase):
	def test_alpha_beta_agent(self):
		referee = LogReferee(AlphaBetaAgent(othello.Player.DARK),
							 AlphaBetaAgent(othello.Player.LIGHT))
		referee.run()

class TestExpectimaxAgent(unittest.TestCase):
	def test_expectimax_agent(self):
		referee = LogReferee(ExpectimaxAgent(othello.Player.DARK),
							 ExpectimaxAgent(othello.Player.LIGHT))
		referee.run()

class TestMCTSAgent(unittest.TestCase):
	def test_mcts_agent(self):
		n_iters = 100

		referee = LogReferee(MCTSAgent(othello.Player.DARK, n_iters),
							 MCTSAgent(othello.Player.LIGHT, n_iters))
		referee.run()
	
class TestAgent(unittest.TestCase):
	def __init__(self, agent1_id=0, agent2_id=0, search_depth_1: int =2, search_depth_2: int =2, 
				 eval_func=evaluation.heuristic_eval_comprehensive) -> None:
		super().__init__()

		self.agent1_id = agent1_id
		self.agent2_id = agent2_id
		self.eval_func = eval_func
		self.search_depth_1 = search_depth_1
		self.search_depth_2 = search_depth_2

	def test_agent(self):
		agents_1 = [RandomAgent(othello.Player.DARK), 
					MaxAgent(othello.Player.DARK, self.eval_func), 
					MinimaxAgent(othello.Player.DARK, eval_func=self.eval_func),
					AlphaBetaAgent(othello.Player.DARK, eval_func=self.eval_func), 
					ExpectimaxAgent(othello.Player.DARK, eval_func=self.eval_func), 
					MCTSAgent(othello.Player.DARK)]
		agents_2 = [RandomAgent(othello.Player.LIGHT), 
					MaxAgent(othello.Player.LIGHT, self.eval_func), 
					MinimaxAgent(othello.Player.LIGHT, eval_func=self.eval_func),
					AlphaBetaAgent(othello.Player.LIGHT, eval_func=self.eval_func), 
					ExpectimaxAgent(othello.Player.LIGHT, eval_func=self.eval_func), 
					MCTSAgent(othello.Player.LIGHT)]
		referee = LogReferee(agents_1[self.agent1_id],
							 agents_2[self.agent2_id])
		referee.run()

if __name__ == '__main__':
	for i in range(6):
		for j in range(6):
			print('i =', i, '\tj =', j)
			TestAgent(i, j).test_agent()
		print()

