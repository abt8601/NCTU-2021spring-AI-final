from collections import defaultdict
from dataclasses import dataclass, field
from math import log, sqrt
import random
from typing import Optional

import othello
from log_referee import LogReferee


@dataclass(frozen=True)
class MCTSTreeData:
    win_count: float = field(default=0)
    play_count: int = field(default=0)

    def __post_init__(self) -> None:
        if self.win_count < 0:
            raise ValueError('invalid win_count')

        if self.play_count < 0:
            raise ValueError('invalid play_count')

        if self.win_count > self.play_count:
            raise ValueError('win_count > play_count')

    @property
    def win_rate(self) -> float:
        return 0 if self.play_count == 0 else self.win_count / self.play_count

    def register_win(self, delta_wc: float) -> 'MCTSTreeData':
        return MCTSTreeData(self.win_count + delta_wc, self.play_count + 1)


class MCTSAgent(othello.Agent):
    def __init__(self, play_as: othello.Player, n_iters: int =100,
                 c: float = sqrt(2)) -> None:
        super().__init__()

        self.play_as = play_as
        self.n_iters = n_iters
        self.c = c

        self.mcts_tree: defaultdict[tuple[othello.Player, othello.State],
                                    MCTSTreeData] \
            = defaultdict(lambda: MCTSTreeData())

    def play(self, state: othello.State) -> Optional[othello.Action]:
        for _ in range(self.n_iters):
            cur_state = state
            player = self.play_as.adversary
            visited = [(player, cur_state)]

            # Selection & Expansion.

            while cur_state.get_conclusion() is None:
                player = player.adversary
                legal_actions = list(cur_state.get_legal_actions(player))

                if legal_actions != []:
                    next_states = [cur_state.perform_action(
                        player, action) for action in legal_actions]
                    not_played_states \
                        = [s for s in next_states
                           if self.mcts_tree[player, s].play_count == 0]

                    if not_played_states == []:
                        log_n = log(sum(self.mcts_tree[player, s].play_count
                                        for s in next_states))

                        def ucb(s: othello.State) -> float:
                            wr = self.mcts_tree[player, s].win_rate
                            pc = self.mcts_tree[player, s].play_count
                            return wr + self.c * sqrt(log_n / pc)

                        cur_state = max(next_states, key=ucb)
                        visited.append((player, cur_state))
                    else:
                        # Removing type annotation causes error here.
                        cur_state: othello.State = random.choice(
                            not_played_states)
                        visited.append((player, cur_state))
                        break

            # Simulation.

            while (conclusion := cur_state.get_conclusion()) is None:
                player = player.adversary
                legal_actions = list(cur_state.get_legal_actions(player))

                if legal_actions != []:
                    next_states = [cur_state.perform_action(
                        player, action) for action in legal_actions]
                    cur_state = random.choice(next_states)

            # Backpropagation.

            for player, s in visited:
                if conclusion is othello.DRAW:
                    delta_wc = .5
                elif conclusion is player:
                    delta_wc = 1
                else:  # if conclusion is player.adversary
                    delta_wc = 0

                self.mcts_tree[player, s] \
                    = self.mcts_tree[player, s].register_win(delta_wc)

        legal_actions = list(state.get_legal_actions(self.play_as))

        if legal_actions == []:
            return None
        else:
            next_states = [state.perform_action(
                self.play_as, action) for action in legal_actions]
            chosen_action, _ \
                = max(zip(legal_actions, next_states),
                      key=lambda x: self.mcts_tree[self.play_as, x[1]].win_rate)
            return chosen_action


def run_mcts_agents() -> None:
    n_iters = 100

    referee = LogReferee(MCTSAgent(othello.Player.DARK, n_iters),
                         MCTSAgent(othello.Player.LIGHT, n_iters))
    referee.run()


if __name__ == '__main__':
    run_mcts_agents()
