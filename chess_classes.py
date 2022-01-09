from typing import Iterable, List, Optional
from two_player_games.game import Game
from two_player_games.state import State
from two_player_games.player import Player
from two_player_games.move import Move
from itertools import product

"""
This file will likely be broken down into several
subfiles corresponding to each class.
"""


class CoordinatesOutOfBoundsException(Exception):
    def __init__(self):
        super().__init__("Coordinate(s) out of bounds in the called function")


class ChessPiece:
    def __init__(self, column: int, row: int, player: Player):
        """
        Chess piece class.

        Variables:
            row:
        """
        if row in list(range(8)) and column in list(range(8)):
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

    def __str__(self) -> str:
        pass

    def __eq__(self, other: "ChessPiece") -> bool:
        return type(self) == type(other)


class Pawn(ChessPiece):
    def __init__(
        self,
        column: int,
        row: int,
        player: Player,
        first_move=True,
        is_en_passantable=False,
    ):
        super().__init__(column, row, player)
        self.first_move = first_move
        self.is_en_passantable = is_en_passantable

    def __str__(self) -> str:
        return f"P{self._player.char}"


class Knight(ChessPiece):
    def __str__(self) -> str:
        return f"N{self._player.char}"


class Bishop(ChessPiece):
    def __str__(self) -> str:
        return f"B{self._player.char}"


class Rook(ChessPiece):
    def __init__(self, column: int, row: int, player: Player, can_castle=True):
        super().__init__(row, column, player)
        self.can_castle = can_castle

    def __str__(self) -> str:
        return f"R{self._player.char}"


class Queen(ChessPiece):
    def __str__(self) -> str:
        return f"Q{self._player.char}"


class King(ChessPiece):
    def __init__(self, column: int, row: int, player: Player, can_castle=True):
        super().__init__(row, column, player)
        self.can_castle = can_castle

    def __str__(self) -> str:
        return f"K{self._player.char}"


class ChessMove(Move):
    def __init__(self, piece: ChessPiece, new_column: int, new_row: int):
        self.piece = piece
        self.new_column = new_column
        self.new_row = new_row

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChessMove):
            return False
        return (
            self.piece == other.piece,
            self.new_column == other.new_column,
            self.new_row == other.new_row,
        )

    def __repr__(self) -> str:
        return f"{type(self.piece).__name__} move to {self.new_column} {self.new_row}"


class ChessState(State):
    def __init__(
        self,
        current_player: Player,
        other_player: Player,
        white: Player = None,
        board: List[List[ChessPiece]] = None,
    ):

        if board:
            self._board = board
        else:
            self._board = [
                [
                    Rook(0, 0, current_player),
                    Knight(1, 0, current_player),
                    Bishop(2, 0, current_player),
                    Queen(3, 0, current_player),
                    King(4, 0, current_player),
                    Bishop(5, 0, current_player),
                    Knight(6, 0, current_player),
                    Rook(7, 0, current_player),
                ],
                [
                    Pawn(column_index, 1, current_player)
                    for column_index in range(8)
                ],
                [None for column in range(8)],
                [None for column in range(8)],
                [None for column in range(8)],
                [None for column in range(8)],
                [
                    Pawn(column_index, 6, other_player)
                    for column_index in range(8)
                ],
                [
                    Rook(0, 7, other_player),
                    Knight(1, 7, other_player),
                    Bishop(2, 7, other_player),
                    Queen(3, 7, other_player),
                    King(4, 7, other_player),
                    Bishop(5, 7, other_player),
                    Knight(6, 7, other_player),
                    Rook(7, 7, other_player),
                ],
            ]

        self._current_player = current_player
        self._other_player = other_player

        self._white = white or current_player

    def _get_moves_pawn(self, pawn: Pawn) -> Iterable[ChessMove]:
        result = []
        row_shift = 1 if pawn.player() == self._white else -1
        if pawn.player() == self._white:  # potentially dangerous if
            if self._board[pawn.row() + row_shift][pawn.column()] is None:
                result.append(
                    ChessMove(pawn, pawn.row() + row_shift, pawn.column())
                )
                if (
                    pawn.first_move
                    and self._board[pawn.row() + 2 * row_shift][pawn.column()]
                    is None
                ):
                    result.append(
                        ChessMove(
                            pawn, pawn.row() + 2 * row_shift, pawn.column()
                        )
                    )
            left_diagonal = self._board[pawn.row() + row_shift][
                pawn.column() - 1
            ]
            right_diagonal = self._board[pawn.row() + row_shift][
                pawn.column() + 1
            ]
            if (
                left_diagonal is not None
                and left_diagonal.player() != pawn.player()
            ):
                result.append(
                    ChessMove(pawn, pawn.row() + row_shift, pawn.column() - 1)
                )
            if (
                right_diagonal is not None
                and right_diagonal.player() != pawn.player()
            ):
                result.append(
                    ChessMove(pawn, pawn.row() + row_shift, pawn.column() + 1)
                )
            left_square = self._board[pawn.row()][pawn.column() - 1]
            right_square = self._board[pawn.row()][pawn.column() + 1]
            if (
                isinstance(left_square, Pawn)
                and left_square.player() != pawn.player()
                and left_square.is_en_passantable
                and left_diagonal is None
            ):
                result.append(
                    ChessMove(pawn, pawn.row() + row_shift, pawn.column() - 1)
                )
            if (
                isinstance(right_square, Pawn)
                and right_square.player() != pawn.player()
                and right_square.is_en_passantable
                and right_diagonal is None
            ):
                result.append(
                    ChessMove(pawn, pawn.row() + row_shift, pawn.column() + 1)
                )
        return result

    def _get_moves_knight(self, knight: Knight) -> Iterable[ChessMove]:
        result = []
        possible_shifts = list(product((-2, 2), (-1, 1))) + list(
            product((-1, 1), (-2, 2))
        )
        for position in possible_shifts:
            new_column, new_row = position
            new_column += knight.column()
            new_row += knight.row()
            if new_column not in range(8) or new_row not in range(8):
                continue
            if not (
                self._board[new_row][new_column] is not None
                and self._board[new_row][new_column].player()
                == knight.player()
            ):
                result.append(ChessMove(knight, new_column, new_row))
        return result

    def _get_moves_bishop(self, bishop: Bishop) -> Iterable[ChessMove]:
        result = []
        for direction in product((-1, 1), (-1, 1)):
            dir_column, dir_row = direction
            for distance in range(1, 8):
                new_column = bishop.column() + distance * dir_column
                new_row = bishop.row() + distance * dir_row
                if new_column not in range(8) or new_row not in range(8):
                    continue
                possible_square = self._board[new_column][new_row]
                if not (
                    possible_square is not None
                    and possible_square.player() == bishop.player()
                ):
                    result.append(ChessMove(bishop, new_column, new_row))
                if possible_square is not None:
                    break
        return result

    def _get_moves_rook(self, rook: Rook) -> Iterable[ChessMove]:
        result = []
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for direction in directions:
            dir_column, dir_row = direction
            for distance in range(1, 8):
                new_column = rook.column() + distance * dir_column
                new_row = rook.row() + distance * dir_row
                if new_column not in range(8) or new_row not in range(8):
                    continue
                possible_square = self._board[new_column][new_row]
                if not (
                    possible_square is not None
                    and possible_square.player() == rook.player()
                ):
                    result.append(ChessMove(rook, new_column, new_row))
                if possible_square is not None:
                    break
        return result

    def _get_moves_queen(self, queen: Queen) -> Iterable[ChessMove]:
        return self._get_moves_bishop(
            Bishop(queen.column(), queen.row(), queen.player())
        ) + self._get_moves_rook(
            Rook(queen.column(), queen.row(), queen.player())
        )

    def _get_moves_king(self, king: King) -> Iterable[ChessMove]:
        result = []
        possible_shifts = list(product((1, 0, -1), (1, 0, -1)))
        possible_shifts.remove((0, 0))
        for shift in possible_shifts:
            new_column, new_row = shift
            new_column += king.column()
            new_row += king.row()
            if new_column not in range(8) or new_row not in range(8):
                continue
            possible_square = self._board[new_column][new_row]
            if not (
                possible_square is not None
                and possible_square.player() == king.player()
            ):
                result.append(ChessMove(king, new_column, new_row))
        return result

    def _get_moves_piece(self, piece: ChessPiece) -> Iterable[ChessMove]:
        pass

    def get_moves(self) -> Iterable[ChessMove]:
        pass

    def get_current_player(self) -> Player:
        return self._current_player

    def make_move(self, move: ChessMove) -> "ChessState":
        pass

    def is_finished(self) -> bool:
        pass

    def get_winner(self) -> Optional[Player]:
        pass

    def __str__(self) -> str:
        return "".join(
            [
                ("".join([f"{piece} " if piece else "   " for piece in row]))
                + "\n"
                for row in reversed(self._board)
            ]
        )


class ChessGame(Game):
    """Class that represents a chess game"""

    FIRST_PLAYER_DEFAULT_CHAR = "1"
    SECOND_PLAYER_DEFAULT_CHAR = "2"

    def __init__(
        self, first_player: Player = None, second_player: Player = None
    ):

        self._first_player = first_player or Player(
            self.FIRST_PLAYER_DEFAULT_CHAR
        )
        self._second_player = second_player or Player(
            self.SECOND_PLAYER_DEFAULT_CHAR
        )

        state = ChessState(self._first_player, self._second_player)

        super().__init__(state)
