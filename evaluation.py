import othello 

def simpleEval (s:othello.State, p:othello.Player):
    return s.get_score(p)