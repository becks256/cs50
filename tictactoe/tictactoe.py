"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


# S₀: Initial state (in our case, an empty 3X3 board)
def initial_state():
    """
    Returns starting state of the board.
    """
    return [
        [EMPTY, EMPTY, EMPTY], 
        [EMPTY, EMPTY, EMPTY], 
        [EMPTY, EMPTY, EMPTY]]


# Players(s): a function that, given a state s, returns which player’s turn it is (X or O).
def player(board):
    """
    Returns player who has the next turn on a board.
    """

    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


# Actions(s): a function that, given a state s, return all the legal moves in this state (what spots are free on the board).
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # get the empty cells on the board
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


# Result(s, a): a function that, given a state s and action a, returns a new state. This is the board that resulted from performing the action a on state s (making a move in the game).
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    (i, j) = action
    if board[i][j] == EMPTY:
        new_board = copy.deepcopy(board)
        new_board[i][j] = player(board)
        return new_board
    else:
        print (f"Invalid action: {action}")
        raise Exception("Invalid action")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # check horizontally, vertically and diagonally
    for i in range(3):

        # check horizontally
        if board[i][0] == board[i][1] == board[i][2] != None:
            return board[i][0]

        # check vertically
        if board[0][i] == board[1][i] == board[2][i] != None:
            return board[0][i]

    # check diagonally
    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != None:
        return board[0][2]

    return None


# Terminal(s): a function that, given a state s, checks whether this is the last step in the game, i.e. if someone won or there is a tie. Returns True if the game has ended, False otherwise.
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != None:
        return True
    if sum(row.count(EMPTY) for row in board) == 0:
        return True

    return False


# Utility(s): a function that, given a terminal state s, returns the utility value of the state: -1, 0, or 1.
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    w = winner(board)

    if w == X:
        return 1
    if w == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    Given a state s (board)

    The maximizing player picks action a in Actions(s) that produces the highest value of Min-Value(Result(s, a)).
    The minimizing player picks action a in Actions(s) that produces the lowest value of Max-Value(Result(s, a)).

    Function Max-Value(state)

    v = -∞

    if Terminal(state):

    ​ return Utility(state)

    for action in Actions(state):

    ​ v = Max(v, Min-Value(Result(state, action)))

    return v

    Function Min-Value(state):

    v = ∞

    if Terminal(state):

    ​ return Utility(state)

    for action in Actions(state):

    ​ v = Min(v, Max-Value(Result(state, action)))

    return v
    """

    def maxvalue(board):
        if terminal(board):
            return utility(board), None
        v = -math.inf
        best_action = None
        for action in actions(board):
            new_v, _ = minvalue(result(board, action))
            if new_v > v:
                v = new_v
                best_action = action
        return v, best_action

    def minvalue(board):
        if terminal(board):
            return utility(board), None
        v = math.inf
        best_action = None
        for action in actions(board):
            new_v, _ = maxvalue(result(board, action))
            if new_v < v:
                v = new_v
                best_action = action
        return v, best_action

    current_player = player(board)

    if current_player == X:
        _, best_action = maxvalue(board)
    else:
        _, best_action = minvalue(board)

    return best_action
