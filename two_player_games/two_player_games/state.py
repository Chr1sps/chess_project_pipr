from typing import Iterable, Optional

from two_player_games.two_player_games.move import Move
from two_player_games.two_player_games.player import Player


class State:
    """Immutable game state object"""

    def get_moves(self) -> Iterable[Move]:
        """
        Returns:
            Possible moves
        """
        raise NotImplementedError

    def get_current_player(self) -> Player:
        """
        Returns:
            Current player
        """
        raise NotImplementedError

    def make_move(self, move: Move) -> "State":
        """
        Creates a new state after making the move

        Parameters:
            move: the move to make

        Returns:
            The state after the move
        """
        raise NotImplementedError

    def is_finished(self) -> bool:
        """
        Returns:
            If the game is finished
        """
        raise NotImplementedError

    def get_winner(self) -> Optional[Player]:
        """
        Returns:
            The player that won or None if draw or not finished
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """
        Returns:
            The string representation of the game's state
        """
        raise NotImplementedError
