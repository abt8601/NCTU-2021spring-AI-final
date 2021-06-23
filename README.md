# NCTU-2021spring-AI-final
Final project of the course Introduction to Artificial Intelligence of NCTU

## Requirement

- Python 3.9 or newer

## Player vs AI
GUI code is modified from [johnafish's design](https://github.com/johnafish/othello)

```bash
python3 graphical_interface.py
```
![Screenshot 2021-06-21 23:57:05](https://user-images.githubusercontent.com/32272431/122792136-71e6d480-d2ec-11eb-953d-35ea803c2868.png)


## Python API Brief Description

This section serves as a quick overview of the Python API.
For details, refer to the documentation in the source code.

### Game Mechanics

Everything related to game mechanics reside in the [`othello`](othello.py) module.

#### `Game`

The `Game` class represents an Othello game.
It keeps track of the game state (the `state` field) and which player plays next (the `next_player` field).

The `play` method plays a given move on behalf of a given player.

```python
game = othello.Game()  # Initialise a new game.
game.play(othello.Player.DARK, othello.Action(othello.Coords.from_repr('d3')))  # Dark plays d3.
game.play(othello.Player.LIGHT, othello.Action(othello.Coords.from_repr('c5')))  # Light plays c5.
```

The `get_conclusion` method returns the conclusion of the game.
I.e., whether the game is still progressing, the game ends in a draw, or either player wins.

```python
game = othello.Game()
assert game.get_conclusion() is None  # The game is still progressing.
```

#### `State`

The `State` class represents the state of an Othello game.
It contains the current board configuration (the `board` field).

The `initial` static method returns the initial state.

The `get_legal_actions` method returns an iterable of all legal actions for a given player.

```python
state = othello.State.initial()
assert set(game.state.get_legal_actions(othello.Player.DARK)) == {othello.Action(othello.Coords.from_repr(a)) for a in ('d3', 'c4', 'f5', 'e6')}
```

The `perform_action` method performs a given action on behalf of a given player.
This is usually used in simulation (e.g. as used in search algorithms).
Note that this method returns a new state, rather than doing an in-place update.

```python
state = othello.State.initial()
next_state = state.perform_action(othello.player.DARK, othello.Action(othello.Coords.from_repr('d3')))  # Dark plays d3.
```

The `is_terminal` method checks if the state is terminal.

```python
state = othello.State.initial()
assert not state.is_terminal()
```

#### `Board`

The `Board` class represents a board configuration of an Othello game.
Refer to the documentation in the source code for its representation.

The `initial` static method returns the initial configuration.

The content of a particular square can be accessed by using the index operator.

```python
board = othello.Board.initial()
assert board[othello.Coords.from_repr('d4')] is othello.Player.DARK  # d4 has a dark piece.
assert board[othello.Coords.from_repr('d3')] is None  # d3 is empty.
```

The `set` method sets the content of a particular square.
Note that this method returns a new board, rather than doing an in-place update.

```python
board = othello.Board.initial()
assert board[othello.Coords.from_repr('d3')] is None
new_board = board.set(othello.Coords.from_repr('d3'), othello.player.LIGHT)
assert new_board[othello.Coords.from_repr('d3')] is othello.player.LIGHT
```

### `Agent` and `Referee`

These classes reside in the [`othello`](othello.py) module.

The `Agent` class is the base class for an agent. An agent inherits this class and override the `play` method.
See the [random agent](random_agent.py) for an example.

This class is used by the `Referee` class to automatically run the game.
The constructor of the `Referee` class takes two instances of `Agent`.
The `Referee` class contains an instance of `Game` (the `game` field) which handles all game logic.
All information related to the game can be accessed through it.

```python
referee = othello.Referee(dark_agent, light_agent)
referee.run()
print(referee.game.get_conclusion())  # Who wins the game?
```

The `Referee` class provides callbacks to be called at certain times. To attach callbacks, inherit this class.
See the [log referee](log_referee.py), which logs the game progress to stdout, for an example.
