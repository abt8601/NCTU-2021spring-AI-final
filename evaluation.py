import othello 

def heuristic_eval_number(state:othello.State, player: othello.Player):
        if player is othello.Player.DARK:
            return f'{state.board.dark_board:b}'.count('1')
        elif player is othello.Player.LIGHT:
            return f'{state.board.light_board:b}'.count('1')

def heuristic_eval_edge(state:othello.State, player: othello.Player):
    n_edge = 0
    edge_point = []
    for i in range(2, 8):
        edge_point.append('a' + str(i))
        edge_point.append('h' + str(i))
    for char in range(ord('b'), ord('h')):
        edge_point.append(chr(char) + '1')
        edge_point.append(chr(char) + '8')
    for point in edge_point:
        if state.board[Coords.from_repr(point)] is player:
            n_edge += 1
    return n_edge

def heuristic_eval_corner(state:othello.State, player: othello.Player):
    n_corner = 0
    for point in ['a1', 'a8', 'h1', 'h8']:
        if state.board[Coords.from_repr(point)] is player:
            n_corner += 1
    return n_corner

def heuristic_eval_n_action(state:othello.State, player: othello.Player):
    return len(list(state.get_legal_actions(player)))

def heuristic_eval_adversary_n_action(state:othello.State, player: othello.Player):
    return -len(list(state.get_legal_actions(player.adversary)))

def heuristic_eval_comprehensive(state:othello.State, player: othello.Player):
	return state.get_score(player)