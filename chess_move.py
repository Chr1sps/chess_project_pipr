from chess_exceptions import CoordinatesOutOfBoundsException
from two_player_games.two_player_games.move import Move


class ChessMove(Move):
    def __init__(
        self,
        start_column: int,
        start_row: int,
        end_column: int,
        end_row: int,
    ):
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
        return self._start_column

    def start_row(self) -> int:
        return self._start_row

    def end_column(self) -> int:
        return self._end_column

    def end_row(self) -> int:
        return self._end_row

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChessMove):
            return False
        return (
            self._start_column == other._start_column
            and self._start_row == other._start_row
            and self._end_column == other._end_column
            and self._end_row == other._end_row
        )

    def __repr__(self) -> str:
        return f"{chr(self._start_column + ord('a'))}{self._start_row + 1} move to \
{chr(self._end_column + ord('a'))}{self._end_row + 1}"
