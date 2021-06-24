import random
from typing import Optional

import othello
from log_referee import LogReferee
import evaluation

class MinimaxAgent(othello.Agent):
    def __init__(self, play_as: othello.Player, search_depth: int =2, eval_func=evaluation.heuristic_eval_comprehensive) -> None:
        super().__init__()

        self.play_as = play_as
        self.depth = search_depth
        self.evaluation_function = lambda state: eval_func(state, self.play_as)

    def play(self, state: othello.State) -> Optional[othello.Action]:
        legal_actions = list(state.get_legal_actions(self.play_as))
        if legal_actions == []:
            return None
        else:
            def minimax(currentGameState, depth, player):
                if currentGameState.is_terminal():
                    return self.evaluation_function(currentGameState)
                legal_actions = list(currentGameState.get_legal_actions(player))

                scores = []
                if player != self.play_as:
                    if depth == self.depth:
                        if len(legal_actions) == 0:
                            return self.evaluation_function(currentGameState)
                        for action in legal_actions:
                            childGameState = currentGameState.perform_action(player, action)
                            scores.append(self.evaluation_function(currentGameState))
                        return min(scores)
                    else:
                        if len(legal_actions) == 0:
                            return minimax(currentGameState, depth + 1, player.adversary)
                        for action in legal_actions:
                            childGameState = currentGameState.perform_action(player, action)
                            scores.append(minimax(childGameState, depth + 1, player.adversary))
                        return min(scores)
                else:
                    if len(legal_actions) == 0:
                        return minimax(currentGameState, depth, player.adversary)
                    for action in legal_actions:
                        childGameState = currentGameState.perform_action(player, action)
                        scores.append(minimax(childGameState, depth, player.adversary))
                    return max(scores)    

            scores = []
            # Choose one of the best actions
            for action in legal_actions:
                childgameState = state.perform_action(self.play_as, action)
                scores.append(minimax(childgameState, 1, self.play_as.adversary))
            bestScore = max(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            # Pick randomly among the best
            chosenIndex = random.choice(bestIndices) 
            
            return legal_actions[chosenIndex]

def run_minimax_agents() -> None:
    referee = LogReferee(MinimaxAgent(othello.Player.DARK),
                         MinimaxAgent(othello.Player.LIGHT))
    referee.run()

if __name__ == '__main__':
    run_minimax_agents()
