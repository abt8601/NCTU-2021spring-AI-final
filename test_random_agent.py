import unittest

from random_agent import run_random_agents


class TestRandomAgent(unittest.TestCase):
    def test_random_agent(self):
        run_random_agents()
