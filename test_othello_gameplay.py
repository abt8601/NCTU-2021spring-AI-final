import unittest
import othello


class TestOthelloGameplay(unittest.TestCase):
    def test_gameplay(self):
        game = othello.Game()

        rep = ('........',
               '........',
               '........',
               '...OX...',
               '...XO...',
               '........',
               '........',
               '........')
        self.assertEqual(tuple(game.state.board.repr), rep)

        self.assertSetEqual(
            set(game.state.get_legal_actions(othello.Player.DARK)),
            {othello.Action(othello.Coords.from_repr(a))
             for a in ('d3', 'c4', 'f5', 'e6')})

        game.play(othello.Player.DARK,
                  othello.Action(othello.Coords.from_repr('d3')))

        rep = ('........',
               '........',
               '...X....',
               '...XX...',
               '...XO...',
               '........',
               '........',
               '........')
        self.assertEqual(tuple(game.state.board.repr), rep)

        self.assertSetEqual(
            set(game.state.get_legal_actions(othello.Player.LIGHT)),
            {othello.Action(othello.Coords.from_repr(a))
             for a in ('c3', 'e3', 'c5')})

        game.play(othello.Player.LIGHT,
                  othello.Action(othello.Coords.from_repr('c5')))

        rep = ('........',
               '........',
               '...X....',
               '...XX...',
               '..OOO...',
               '........',
               '........',
               '........')
        self.assertEqual(tuple(game.state.board.repr), rep)

    def test_endgame_1(self):
        rep = ('OOOOOOOO',
               'OOOOOOOO',
               'OOOOOOOO',
               'OOOOOOO.',
               'OOOOOO..',
               'OOOOOO.X',
               'OOOOOOO.',
               'OOOOOOOO')
        state = othello.State(othello.Board.from_repr(rep))

        self.assertSetEqual(set(state.get_legal_actions(othello.Player.DARK)),
                            set())
        self.assertSetEqual(set(state.get_legal_actions(othello.Player.LIGHT)),
                            set())

        self.assertIs(othello.Game(state).get_conclusion(),
                      othello.Player.LIGHT)

    def test_endgame_2(self):
        rep = ('.XXXXXXX',
               '.OOOOO.X',
               'OOOOOOOX',
               'OOOOOOOX',
               'OOOOOOOX',
               'OOOOOOOX',
               'OOOOOOOX',
               '.OOOOOO.')
        state = othello.State(othello.Board.from_repr(rep))

        self.assertSetEqual(set(state.get_legal_actions(othello.Player.DARK)),
                            set())
        self.assertSetEqual(set(state.get_legal_actions(othello.Player.LIGHT)),
                            set())

        self.assertIs(othello.Game(state).get_conclusion(),
                      othello.Player.LIGHT)

    def test_endgame_3(self):
        rep = ('....O...',
               '....OO..',
               'OOOOOOOX',
               '..OOOO.X',
               '..OOO..X',
               '........',
               '........',
               '........')
        state = othello.State(othello.Board.from_repr(rep))

        self.assertSetEqual(set(state.get_legal_actions(othello.Player.DARK)),
                            set())
        self.assertSetEqual(set(state.get_legal_actions(othello.Player.LIGHT)),
                            set())

        self.assertIs(othello.Game(state).get_conclusion(),
                      othello.Player.LIGHT)
