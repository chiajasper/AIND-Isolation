"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def cross_product(list_1, list_2):
    z = zip(list_1, list_2)
    return sum( x * y for x, y in z)

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
    alpha = 1
    fn_1 = len(game.get_legal_moves(player))
    beta = -1
    fn_2 = len(game.get_legal_moves(game.get_opponent(player)))
    return float(cross_product([alpha, beta], [fn_1, fn_2]))


def custom_score_2(game, player):
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
    alpha = 0
    fn_1 = len(game.get_legal_moves(player))
    beta = 0
    fn_2 = len(game.get_legal_moves(game.get_opponent(player)))
    gamma = 1
    # how close player's move is to center_distance
    fn_3 = math.sqrt(pow(game.get_player_location(player)[0] - game.width/2 , 2) + pow(game.get_player_location(player)[1] - game.height/2 , 2))
    return float(cross_product([alpha, beta, gamma], [fn_1, fn_2, fn_3]))

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
    alpha = 100
    my_moves = len(game.get_legal_moves(player)) / 8.
    fn_1 = math.log( my_moves if my_moves != 0 else 1 ,10)
    beta = 140
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player))) / 8.
    fn_2 = math.log( 1 / opponent_moves if opponent_moves != 0 else 1 , 10)
    return float(cross_product([alpha, beta], [fn_1, fn_2]))



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
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
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
            raise RuntimeError("Spent too much time thinking!")

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = (-1, -1)
        if len(game.get_legal_moves()) == 0:
            return best_move
        elif len(game.get_legal_moves()) == 1:
            return game.get_legal_moves()[0]

        utility_value = float("-inf")
        # get the maximum utility value from all the moves
        for move in game.get_legal_moves():
            try:
                val = self.min_value(game.forecast_move(move), depth-1)
                if val > utility_value:
                    best_move = move
                    utility_value = max(val, utility_value)
            except SearchTimeout:
                return best_move

        best_move = game.get_legal_moves()[0] if best_move == (-1, -1) else best_move
        return best_move

    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # terminal state
        if depth == 0:# or len(game.get_legal_moves()) == 0:
            return self.score(game, game.active_player)
        else:
            value = float("-inf")
            for move in game.get_legal_moves():
                # get the maximum utility value from all the possible moves since the current player's move
                value = max(value, self.min_value(game.forecast_move(move), depth-1))

            return value

    def min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # terminal state
        if depth == 0:# or len(game.get_legal_moves()) == 0:
            return self.score(game, game.inactive_player)
        else:
            value = float("inf")
            for move in game.get_legal_moves():
                # get the minimum utility value from all the possible moves since its opponent's move
                value= min(value, self.max_value(game.forecast_move(move), depth-1))

            return value


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
        self.time_left = time_left

        # return fast if there are no choices of legal moves
        if len(game.get_legal_moves()) == 0:
            return (-1, -1)
        elif len(game.get_legal_moves()) == 1:
            return game.get_legal_moves()[0]

        best_move = (-1, -1)
        x = game.get_legal_moves()
        try:
            # if there are not enough legal moves, start with depth 2 to prevent searching too deep at the beginning
            depth = 2 if len(game.get_legal_moves()) < 2 * self.search_depth else self.search_depth

            time_spent = prev_time_spent =  0
            time_ratio = 2
            while time_left() > 0 and time_left() > time_spent * time_ratio and depth <= len(game.get_blank_spaces()) :
                before = time_left()
                prev_best_move = best_move
                calculated_move = self.alphabeta(game, depth)
                # never discard the current best move ever!
                best_move = calculated_move if calculated_move != (-1, -1) else best_move
                prev_time_spent = time_spent
                time_spent = before - time_left()
                time_ratio = (time_spent - prev_time_spent) / prev_time_spent if prev_time_spent != 0 else time_ratio
                depth += 1

        except SearchTimeout:
            return best_move

        # Return the best move from the last completed search iteration
        best_move = game.get_legal_moves()[0] if best_move == (-1, -1) else best_move
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = (-1, -1)
        if len(game.get_legal_moves()) == 0:
            return best_move
        elif len(game.get_legal_moves()) == 1:
            return game.get_legal_moves()[0]

        utility_value = float("-inf")
        # return move after finding the move which returns the highest utility value
        for move in game.get_legal_moves():
            try:
                val, alpha, beta = self.min_value(game.forecast_move(move), depth-1, alpha, beta)
                #print("move %s with value %s utility_value %s and blank: %s" % ( move, val, utility_value, game.get_blank_spaces()) )
                if val > utility_value:
                    #print("move %s with value %s" % ( move, val) )
                    best_move = move
                    utility_value = val
            # if timer expires, return the best so far
            except SearchTimeout:
                return best_move

        best_move = game.get_legal_moves()[0] if best_move == (-1, -1) else best_move
        return best_move

    # simulate the max node in the min max search
    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # terminal state
        if depth == 0:
            return self.score(game, game.active_player), alpha, beta
        elif len(game.get_legal_moves()) == 0:
            self.score(game, game.active_player)
            return float("-inf"), alpha, beta
        else:
            value = float("-inf")
            this_alpha, this_beta = alpha, beta

            for move in game.get_legal_moves():
                res, this_alpha, this_beta = self.min_value(game.forecast_move(move), depth-1, this_alpha, this_beta)
                # if the current utility value is higher than upper bound overall, we can ignore the rest of the nodes
                if res >= beta:
                    return res, alpha, beta
                # computer max value
                value = max(value, res)

            # adjust the upper bound
            return value, alpha, min(beta, value)

    # simulate the min node in the min max search
    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # terminal state
        if depth == 0:#
            return self.score(game, game.inactive_player), alpha, beta
        elif len(game.get_legal_moves()) == 0:
            self.score(game, game.inactive_player)
            return float("inf"), alpha, beta
        else:
            value = float("inf")
            this_alpha, this_beta = alpha, beta

            for move in game.get_legal_moves():
                res, this_alpha, this_beta = self.max_value(game.forecast_move(move), depth-1, this_alpha, this_beta)
                # if the current utility value is lower than lower bound overall, we can ignore the rest of the nodes
                if res <= alpha:
                    return res, alpha, beta
                # computer min value
                value = min(value, res)

            # adjust the lower bound
            return value, max(value,alpha), beta
