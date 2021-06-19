import random
from typing import Optional

import othello
from log_referee import LogReferee


class ExpectimaxAgent(othello.Agent):
    def __init__(self, play_as: othello.Player) -> None:
        super().__init__()

        self.play_as = play_as

    def play(self, state: othello.State) -> Optional[othello.Action]:
        legal_actions = list(state.get_legal_actions(self.play_as))

        if legal_actions == []:
            return None
        else:
            self.depth = 2

            def expectimax(currentGameState, depth, player):
                if currentGameState.is_terminal():
                    return currentGameState.get_score(self.play_as)
                legal_actions = list(currentGameState.get_legal_actions(player))
                if len(legal_actions) == 0:
                    return currentGameState.get_score(self.play_as)
                scores = []
                if player != self.play_as:
                    if depth == self.depth:
                        scores = 0.0
                        for action in legal_actions:
                            childGameState = currentGameState.perform_action(player, action)
                            scores += currentGameState.get_score(self.play_as)
                        return scores / len(legal_actions)
                    else:
                        scores = 0.0
                        for action in legal_actions:
                            childGameState = currentGameState.perform_action(player, action)
                            scores += expectimax(childGameState, depth + 1, player.adversary)
                        return scores / len(legal_actions)
                else:
                    for action in legal_actions:
                        childGameState = currentGameState.perform_action(player, action)
                        scores.append(expectimax(childGameState, depth, player.adversary))
                    return max(scores)    

            scores = []
            # Choose one of the best actions
            for action in legal_actions:
                childgameState = state.perform_action(self.play_as, action)
                scores.append(expectimax(childgameState, 1, self.play_as.adversary))
            bestScore = max(scores)
            bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
            # Pick randomly among the best
            chosenIndex = random.choice(bestIndices) 
            
            return legal_actions[chosenIndex]


def run_expectimax_agents() -> None:
    referee = LogReferee(ExpectimaxAgent(othello.Player.DARK),
                         ExpectimaxAgent(othello.Player.LIGHT))
    referee.run()


if __name__ == '__main__':
    run_expectimax_agents()

