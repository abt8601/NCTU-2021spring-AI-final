import random
from typing import Optional
import othello
from log_referee import LogReferee
import evaluation


class AlphaBetaAgent(othello.Agent):
    def __init__(self, play_as: othello.Player, search_depth: int =4, eval_func=evaluation.heuristic_eval_comprehensive) -> None:
        super().__init__()

        self.play_as = play_as
        self.depth = search_depth
        self.evaluation_function = lambda state: eval_func(state, self.play_as)
    def play(self, state: othello.State) -> Optional[othello.Action]:
        
        def minmax(gameState: othello.State, agent: othello.Player, depth: int, alpha: float, beta: float) -> float:
            if depth == 0 or gameState.is_terminal() :
                return self.evaluation_function(gameState)
            
            moves = gameState.get_legal_actions(agent)
            # when there is no action , this node has only 1 child, no search is needed
            if moves is None:
                return minmax(gameState, agent.adversary, depth-1, alpha, beta)
            
            v = None
            if agent == self.play_as: # max node
                v = float('-inf')
                for m in moves:
                    nextState = gameState.perform_action(agent,m)
                    nextAgent = agent.adversary
                    nextDepth = depth-1
                    score = minmax(nextState , nextAgent, nextDepth, alpha, beta)
                    v = max(v, score)
                    alpha = max(alpha, v)
                    if v > beta:
                        break
            else: # min Node
                v = float('inf')
                for m in moves:
                    nextState = gameState.perform_action(agent,m)
                    nextAgent = agent.adversary
                    nextDepth = depth-1
                    score = minmax(nextState , nextAgent, nextDepth, alpha, beta)
                    v = min(v, score)
                    beta = min(beta, v)
                    if v < alpha:
                        break
            return v

        moves = list(state.get_legal_actions(self.play_as))

        if len(moves) == 0:
            return None

        max_score = float('-inf')
        best_move = moves[0]
        for m in moves:
            score = minmax(state.perform_action(self.play_as,m), self.play_as.adversary ,  2*self.depth - 1, max_score, float('inf'))
            if score > max_score:
                best_move = m
                max_score = score
        return best_move



def run_alpha_beta_agents() -> None:
    referee = LogReferee(AlphaBetaAgent(othello.Player.DARK),
                         AlphaBetaAgent(othello.Player.LIGHT))
    referee.run()


if __name__ == '__main__':
    run_alpha_beta_agents()
