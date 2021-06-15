import unittest

import othello
from random_agent import RandomAgent


class TestRandomAgent(unittest.TestCase):
    def test_random_agent(self):
        othello.Referee(RandomAgent(othello.Player.DARK),
                        RandomAgent(othello.Player.LIGHT)).run()
