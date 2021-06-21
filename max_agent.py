import random
from typing import Optional

import othello
from log_referee import LogReferee
import evaluation

class MaxAgent(othello.Agent):
    def __init__(self, play_as: othello.Player, eval_func=evaluation.heuristic_eval_comprehensive) -> None:
        super().__init__()

        self.play_as = play_as
        self.evaluation_function = lambda state: eval_func(state, self.play_as)

    def play(self, state: othello.State) -> Optional[othello.Action]:
        legal_actions = list(state.get_legal_actions(self.play_as))
        if legal_actions == []:
            return None
        else:
            # best_score = 0
            # best_action = legal_actions[0]
            # for action in legal_actions:
            #     next_state = state.perform_action(self.play_as, action)
            #     if next_state.get_score(self.play_as) > best_score:
            #         best_action = action
            option = []
            for action in legal_actions:
                next_state = state.perform_action(self.play_as, action)
                score = self.evaluation_function(next_state)
                option.append((action, score))
            best_action = max(option ,key=lambda item:item[1])[0]
            return best_action


def run_max_agents() -> None:
    referee = LogReferee(MaxAgent(othello.Player.DARK),
                         MaxAgent(othello.Player.LIGHT))
    referee.run()


if __name__ == '__main__':
    run_max_agents()
