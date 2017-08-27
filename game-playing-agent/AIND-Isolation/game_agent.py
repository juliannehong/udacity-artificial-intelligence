"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    own_y, own_x = game.get_player_location(player)
    opp_y, opp_x = game.get_player_location(game.get_opponent(player))
    
    moves =  float(own_moves - 2*opp_moves)
    #moves = float(own_moves)
    dist = float((own_x - opp_x)**2 + (own_y - opp_y)**2)

    return moves + dist


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")


    own_y, own_x = game.get_player_location(player)
    opp_y, opp_x = game.get_player_location(game.get_opponent(player))
    return float((own_x - opp_x)**2 + (own_y - opp_y)**2)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")


    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - 2*opp_moves)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=5, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game. 

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        def min_value(self, game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if (game.utility(self) != 0):
                return game.utility(self)
            if (depth == 0):
                return self.score(game, self)
            v = float("inf")
            v = min(max_value(self, game.forecast_move(m), depth-1) for m in game.get_legal_moves())
            return v

        def max_value(self, game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if (game.utility(self) != 0):
                return game.utility(self)
            if (depth == 0):
                return self.score(game, self)
            v = float("-inf")
            v = max(min_value(self, game.forecast_move(m), depth-1) for m in game.get_legal_moves())
            return v
 
        f = lambda x : min_value(self, game.forecast_move(x), depth-1)
        if len(game.get_legal_moves()) > 0:
            return max(game.get_legal_moves(), key = f)
        else:
            return (-1, -1)



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        # self.time_left = time_left

        # # TODO: finish this function!
        # raise NotImplementedError
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            for depth in range(0, 100):
                best_move = self.alphabeta(game, depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
       
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        def max_value(self, game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if game.utility(self) != 0:
                return (game.utility(self), game.get_player_location(self))
            if (depth == 0):
                return (self.score(game, self), game.get_player_location(self))
            v = (float("-inf"), (-1, -1))
            for m in game.get_legal_moves():
                tv, _= max(v, min_value(self, game.forecast_move(m), depth-1, alpha, beta))
                if (tv != v[0]):
                    v = (tv, m)
                if (v[0] >= beta):
                    return v
                alpha = max(alpha, v[0])
            return v

        def min_value(self, game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if game.utility(self) != 0:
                return (game.utility(self), game.get_player_location(self))
            if (depth == 0):
                return (self.score(game, self), game.get_player_location(self))
            v = (float("inf"), (-1, -1))
            for m in game.get_legal_moves():
                tv, _ = min(v, max_value(self, game.forecast_move(m), depth-1, alpha, beta))
                if (tv != v[0]):
                    v = (tv, m)
                if (v[0] <= alpha):
                    return v
                beta = min(beta, v[0])

            return v

        _, m = max_value(self, game, depth, alpha, beta)
        return m
