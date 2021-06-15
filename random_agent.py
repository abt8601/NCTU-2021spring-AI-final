import random
from typing import Optional

import othello
from log_referee import LogReferee


class RandomAgent(othello.Agent):
    def __init__(self, play_as: othello.Player) -> None:
        super().__init__()

        self.play_as = play_as

    def play(self, state: othello.State) -> Optional[othello.Action]:
        legal_actions = list(state.get_legal_actions(self.play_as))

        if legal_actions == []:
            return None
        else:
            return random.choice(legal_actions)


def run_random_agents() -> None:
    referee = LogReferee(RandomAgent(othello.Player.DARK),
                         RandomAgent(othello.Player.LIGHT))
    referee.run()


if __name__ == '__main__':
    run_random_agents()
