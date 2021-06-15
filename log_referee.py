from typing import Optional

import othello


class LogReferee(othello.Referee):
    def cb_post_move(self, player: othello.Player,
                     action: Optional[othello.Action]) -> None:
        if action is None:
            print(f'{player} skips')
        else:
            print(f'{player} plays {action.repr}')

        for row in self.game.state.board.repr:
            print(row)

        print()

    def cb_game_end(self) -> None:
        if self.game.get_conclusion() is othello.DRAW:
            print('Draw!')
        else:
            print(f'{self.game.get_conclusion()} wins!')
