from chess_game_interface.chess_exceptions import (
    CoordinatesOutOfBoundsException,
)
from chess_game_interface.two_player_games.two_player_games.move import Move


class ChessMove(Move):
    """
    A class representing moves in chess.


    Attributes:

    _start_column : int
        an integer representing the column of a square
        from which the move originates

    _start_row : int
        an integer representing the row of a square
        from which the move originates

    _end_column : int
        an integer representing the column of a square
        that is the destination of the move

    _end_row : int
        an integer representing the row of a square
        that is the destination of the move
    """

    def __init__(
        self,
        start_column: int,
        start_row: int,
        end_column: int,
        end_row: int,
    ):

        """
        Constructor of the ChessMove class. Function checks if the given
        arguments are within the range of available coordinates.


        Parameters:

        start_column : int
            an integer representing the column of a square
            from which the move originates

        start_row : int
            an integer representing the row of a square
            from which the move originates

        end_column : int
            an integer representing the column of a square
            that is the destination of the move

        end_row : int
            an integer representing the row of a square
            that is the destination of the move
        """

        if all(
            coordinate in range(8)
            for coordinate in (start_column, start_row, end_column, end_row)
        ):
            self._start_column = start_column
            self._start_row = start_row
            self._end_column = end_column
            self._end_row = end_row
        else:
            raise CoordinatesOutOfBoundsException

    def start_column(self) -> int:
        """Returns the column of an originating square."""
        return self._start_column

    def start_row(self) -> int:
        """Returns the row of an originating square."""
        return self._start_row

    def end_column(self) -> int:
        """Returns the column of a destination square."""
        return self._end_column

    def end_row(self) -> int:
        """Returns the row of a destination square."""
        return self._end_row

    def __eq__(self, other: object) -> bool:
        """Checks if two moves are equal."""
        if not isinstance(other, ChessMove):
            return False
        return (
            self._start_column == other._start_column
            and self._start_row == other._start_row
            and self._end_column == other._end_column
            and self._end_row == other._end_row
        )

    def __repr__(self) -> str:
        """
        Return object info for debugging (originating and destination square).
        """
        return f"{chr(self._start_column + ord('a'))}{self._start_row + 1} move to \
{chr(self._end_column + ord('a'))}{self._end_row + 1}"
