from chess_exceptions import CoordinatesOutOfBoundsException
from two_player_games.two_player_games.player import Player
from typing import Iterable, Tuple
from itertools import product
from chess_move import ChessMove


class ChessState:
    pass


class ChessPiece:
    def __init__(
        self,
        column: int,
        row: int,
        player: Player,
    ):

        if row in range(8) and column in range(8):
            self._row = row
            self._column = column
        else:
            raise CoordinatesOutOfBoundsException

        self._player = player

    def set_row(self, row: int):
        if row in list(range(8)):
            self._row = row
        else:
            raise CoordinatesOutOfBoundsException

    def set_column(self, column: int):
        if column in list(range(8)):
            self._column = column
        else:
            raise CoordinatesOutOfBoundsException

    def column(self) -> int:
        return self._column

    def row(self) -> int:
        return self._row

    def player(self) -> Player:
        return self._player

    def _get_moves_lines(
        self, state: ChessState, directions: Iterable[Tuple[int, int]]
    ) -> Iterable[ChessMove]:
        result = []
        for direction in directions:
            dir_column, dir_row = direction
            for distance in range(1, 8):
                new_column = self._column + distance * dir_column
                new_row = self._row + distance * dir_row
                if new_column not in range(8) or new_row not in range(8):
                    continue
                possible_square = state._board[new_row][new_column]
                if not (
                    possible_square is not None
                    and possible_square.player() == self._player
                ):
                    result.append(
                        ChessMove(
                            self._column,
                            self._row,
                            new_column,
                            new_row,
                        )
                    )
                if possible_square is not None:
                    break
        return result

    def _get_moves_shifts(
        self, state: ChessState, shifts: Iterable[Tuple[int, int]]
    ) -> Iterable[ChessMove]:
        result = []
        for position in shifts:
            new_column, new_row = position
            new_column += self._column
            new_row += self._row
            if new_column not in range(8) or new_row not in range(8):
                continue
            possible_square = state._board[new_row][new_column]
            if not (
                possible_square is not None
                and possible_square.player() == self._player
            ):
                result.append(
                    ChessMove(
                        self._column,
                        self._row,
                        new_column,
                        new_row,
                    )
                )
        return result

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__} at \
{chr(self._column + ord('a'))}{self._row + 1}"

    def __str__(self) -> str:
        pass


class Pawn(ChessPiece):
    def __init__(
        self,
        column: int,
        row: int,
        player: Player,
        first_move: bool = True,
        is_en_passantable: bool = False,
    ):

        super().__init__(column, row, player)
        self._first_move = first_move
        self._is_en_passantable = is_en_passantable

    def is_en_passantable(self) -> bool:
        return self._is_en_passantable

    def first_move(self) -> bool:
        return self._first_move

    def __str__(self) -> str:
        return f"P{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        result = []
        row_shift = 1 if self._player == state._white else -1
        right_column = self._column + 1
        left_column = self._column - 1

        if state._board[self._row + row_shift][self._column] is None:
            result.append(
                ChessMove(
                    self._column,
                    self._row,
                    self._column,
                    self._row + row_shift,
                )
            )
        if (
            self._first_move
            and state._board[self._row + 2 * row_shift][self._column] is None
        ):
            result.append(
                ChessMove(
                    self._column,
                    self._row,
                    self._column,
                    self._row + 2 * row_shift,
                )
            )
        if right_column in range(8):
            right_diagonal = state._board[self._row + row_shift][right_column]
            if (
                right_diagonal is not None
                and right_diagonal.player() != self._player
            ):
                result.append(
                    ChessMove(
                        self._column,
                        self._row,
                        right_column,
                        self._row + row_shift,
                    )
                )

            right_square = state._board[self._row][right_column]
            if (
                right_square is not None
                and type(right_square) == Pawn
                and right_square.player() != self._player
                and right_square.is_en_passantable
                and right_diagonal is None
            ):
                result.append(
                    ChessMove(
                        self._column,
                        self._row,
                        right_column,
                        self._row + row_shift,
                    )
                )

        if left_column in range(8):
            left_diagonal = state._board[self._row + row_shift][left_column]
            if (
                left_diagonal is not None
                and left_diagonal.player() != self._player
            ):
                result.append(
                    ChessMove(
                        self._column,
                        self._row,
                        left_column,
                        self._row + row_shift,
                    )
                )

            left_square = state._board[self._row][left_column]
            if (
                left_square is not None
                and type(left_square) == Pawn
                and left_square.player() != self._player
                and left_square.is_en_passantable
                and left_diagonal is None
            ):
                result.append(
                    ChessMove(
                        self._column,
                        self._row,
                        left_column,
                        self._row + row_shift,
                    )
                )

        return result


class Knight(ChessPiece):
    def __str__(self) -> str:
        return f"N{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        possible_shifts = list(product((-2, 2), (-1, 1))) + list(
            product((-1, 1), (-2, 2))
        )
        return self._get_moves_shifts(state, possible_shifts)


class Bishop(ChessPiece):
    def __str__(self) -> str:
        return f"B{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        return self._get_moves_lines(state, product((-1, 1), (-1, 1)))


class Rook(ChessPiece):
    def __init__(
        self,
        column: int,
        row: int,
        player: Player,
        can_castle: bool = True,
    ):

        super().__init__(column, row, player)
        self._can_castle = can_castle

    def can_castle(self):
        return self._can_castle

    def __str__(self) -> str:
        return f"R{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        return self._get_moves_lines(state, directions)


class Queen(ChessPiece):
    def __str__(self) -> str:
        return f"Q{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        directions = list(product((1, 0, -1), (1, 0, -1)))
        directions.remove((0, 0))
        return self._get_moves_lines(state, directions)


class King(ChessPiece):
    def __init__(
        self,
        column: int,
        row: int,
        player: Player,
        can_castle: bool = True,
    ):

        super().__init__(column, row, player)
        self._can_castle = can_castle

    def can_castle(self):
        return self._can_castle

    def __str__(self) -> str:
        return f"K{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:

        possible_shifts = list(product((1, 0, -1), (1, 0, -1)))
        possible_shifts.remove((0, 0))
        result = self._get_moves_shifts(state, possible_shifts)

        if self._column == 4 and self._can_castle:

            left_corner = state._board[self._row][0]
            if (
                left_corner
                and type(left_corner) == Rook
                and left_corner.player() == self._player
                and left_corner.can_castle()
                and all(
                    state._board[self._row][column] is None
                    for column in range(1, 4)
                )
            ):
                result.append(ChessMove(self._column, self._row, 2, self._row))

            right_corner = state._board[self._row][7]
            if (
                right_corner
                and type(right_corner) == Rook
                and right_corner.player() == self._player
                and right_corner.can_castle()
                and all(
                    state._board[self._row][column] is None
                    for column in range(5, 7)
                )
            ):
                result.append(ChessMove(self._column, self._row, 6, self._row))

        return result
