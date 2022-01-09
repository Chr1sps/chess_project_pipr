from typing import Iterable, List, Optional
from two_player_games.game import Game
from two_player_games.state import State
from two_player_games.player import Player
from two_player_games.move import Move
from itertools import product


PAWN = 0
KNIGHT = 1
BISHOP = 2
ROOK = 3
QUEEN = 4
KING = 5


class CoordinatesOutOfBoundsException(Exception):
    def __init__(self):
        super().__init__("Coordinate(s) out of bounds in the called function.")


class IncorrectPieceTypeException(Exception):
    def __init__(self):
        super().__init__("Wrong chess piece type in the called function.")


class ChessPiece:
    def __init__(
        self,
        type: int,
        column: int,
        row: int,
        player: Player,
        first_move_or_can_castle: bool = True,
        is_en_passantable: bool = False,
    ):
        if row in range(8) and column in range(8):
            self._row = row
            self._column = column
        else:
            raise CoordinatesOutOfBoundsException

        if type in range(6):
            self._type = type
        else:
            raise IncorrectPieceTypeException

        self._player = player

        if type == PAWN:
            self.first_move = first_move_or_can_castle
            self.is_en_passantable = is_en_passantable

        if type in (ROOK, KING):
            self.can_castle = first_move_or_can_castle

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

    def type(self) -> int:
        return self._type

    def column(self) -> int:
        return self._column

    def row(self) -> int:
        return self._row

    def player(self) -> Player:
        return self._player

    def __str__(self) -> str:
        piece_acronyms = {
            PAWN: "P",
            KNIGHT: "N",
            BISHOP: "B",
            ROOK: "R",
            QUEEN: "Q",
            KING: "K",
        }
        return f"{piece_acronyms[self._type]}{self._player.char}"

    def __eq__(self, other: "ChessPiece") -> bool:
        return self._type == other._type

    def __repr__(self) -> str:
        piece_names = {
            PAWN: "Pawn",
            KNIGHT: "Knight",
            BISHOP: "Bishop",
            ROOK: "Rook",
            QUEEN: "Queen",
            KING: "King",
        }
        return f"{piece_names[self._type]} at {self._column} {self._row}"


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
        piece_names = {
            PAWN: "Pawn",
            KNIGHT: "Knight",
            BISHOP: "Bishop",
            ROOK: "Rook",
            QUEEN: "Queen",
            KING: "King",
        }
        return f"{piece_names[self.piece.type()]} move to {self.new_column} {self.new_row}"


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
            white = white or current_player
            black = other_player if current_player == white else current_player
            self._board = [
                [
                    ChessPiece(ROOK, 0, 0, white),
                    ChessPiece(KNIGHT, 1, 0, white),
                    ChessPiece(BISHOP, 2, 0, white),
                    ChessPiece(QUEEN, 3, 0, white),
                    ChessPiece(KING, 4, 0, white),
                    ChessPiece(BISHOP, 5, 0, white),
                    ChessPiece(KNIGHT, 6, 0, white),
                    ChessPiece(ROOK, 7, 0, white),
                ],
                [
                    ChessPiece(PAWN, column_index, 1, white)
                    for column_index in range(8)
                ],
                [None for column in range(8)],
                [None for column in range(8)],
                [None for column in range(8)],
                [None for column in range(8)],
                [
                    ChessPiece(PAWN, column_index, 6, black)
                    for column_index in range(8)
                ],
                [
                    ChessPiece(ROOK, 0, 7, black),
                    ChessPiece(KNIGHT, 1, 7, black),
                    ChessPiece(BISHOP, 2, 7, black),
                    ChessPiece(QUEEN, 3, 7, black),
                    ChessPiece(KING, 4, 7, black),
                    ChessPiece(BISHOP, 5, 7, black),
                    ChessPiece(KNIGHT, 6, 7, black),
                    ChessPiece(ROOK, 7, 7, black),
                ],
            ]

        self._current_player = current_player
        self._other_player = other_player

        self._white = white or current_player

    def _get_moves_pawn(self, pawn: ChessPiece) -> Iterable[ChessMove]:
        result = []
        row_shift = 1 if pawn.player() == self._white else -1
        right_column = pawn.column() + 1
        left_column = pawn.column() - 1

        if self._board[pawn.row() + row_shift][pawn.column()] is None:
            result.append(
                ChessMove(pawn, pawn.row() + row_shift, pawn.column())
            )
        if (
            pawn.first_move
            and self._board[pawn.row() + 2 * row_shift][pawn.column()] is None
        ):
            result.append(
                ChessMove(pawn, pawn.row() + 2 * row_shift, pawn.column())
            )
        if right_column in range(8):
            right_diagonal = self._board[pawn.row() + row_shift][right_column]
            if (
                right_diagonal is not None
                and right_diagonal.player() != pawn.player()
            ):
                result.append(
                    ChessMove(pawn, pawn.row() + row_shift, right_column)
                )

            right_square = self._board[pawn.row()][right_column]
            if (
                right_square is not None
                and right_square.type() == PAWN
                and right_square.player() != pawn.player()
                and right_square.is_en_passantable
                and right_diagonal is None
            ):
                result.append(
                    ChessMove(pawn, pawn.row() + row_shift, right_column)
                )

        if left_column in range(8):
            left_diagonal = self._board[pawn.row() + row_shift][left_column]
            if (
                left_diagonal is not None
                and left_diagonal.player() != pawn.player()
            ):
                result.append(
                    ChessMove(pawn, pawn.row() + row_shift, left_column)
                )

            left_square = self._board[pawn.row()][left_column]
            if (
                left_square is not None
                and left_square.type() == PAWN
                and left_square.player() != pawn.player()
                and left_square.is_en_passantable
                and left_diagonal is None
            ):
                result.append(
                    ChessMove(pawn, pawn.row() + row_shift, left_column)
                )

        return result

    def _get_moves_knight(self, knight: ChessPiece) -> Iterable[ChessMove]:
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

    def _get_moves_bishop(self, bishop: ChessPiece) -> Iterable[ChessMove]:
        result = []
        for direction in product((-1, 1), (-1, 1)):
            dir_column, dir_row = direction
            for distance in range(1, 8):
                new_column = bishop.column() + distance * dir_column
                new_row = bishop.row() + distance * dir_row
                if new_column not in range(8) or new_row not in range(8):
                    break
                possible_square = self._board[new_row][new_column]
                if not (
                    possible_square is not None
                    and possible_square.player() == bishop.player()
                ):
                    result.append(ChessMove(bishop, new_column, new_row))
                if possible_square is not None:
                    break
        return result

    def _get_moves_rook(self, rook: ChessPiece) -> Iterable[ChessMove]:
        result = []
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for direction in directions:
            dir_column, dir_row = direction
            for distance in range(1, 8):
                new_column = rook.column() + distance * dir_column
                new_row = rook.row() + distance * dir_row
                if new_column not in range(8) or new_row not in range(8):
                    continue
                possible_square = self._board[new_row][new_column]
                if not (
                    possible_square is not None
                    and possible_square.player() == rook.player()
                ):
                    result.append(ChessMove(rook, new_column, new_row))
                if possible_square is not None:
                    break
        return result

    def _get_moves_king(self, king: ChessPiece) -> Iterable[ChessMove]:
        result = []
        possible_shifts = list(product((1, 0, -1), (1, 0, -1)))
        possible_shifts.remove((0, 0))
        for shift in possible_shifts:
            new_column, new_row = shift
            new_column += king.column()
            new_row += king.row()
            if new_column not in range(8) or new_row not in range(8):
                continue
            possible_square = self._board[new_row][new_column]
            if not (
                possible_square is not None
                and possible_square.player() == king.player()
            ):
                result.append(ChessMove(king, new_column, new_row))
        return result

    def _get_moves_queen(self, queen: ChessPiece) -> Iterable[ChessMove]:
        return self._get_moves_bishop(queen) + self._get_moves_rook(queen)

    def _get_moves_piece(self, piece: ChessPiece) -> Iterable[ChessMove]:
        if piece is None:
            return None
        return {
            PAWN: self._get_moves_pawn,
            KNIGHT: self._get_moves_knight,
            BISHOP: self._get_moves_bishop,
            ROOK: self._get_moves_rook,
            QUEEN: self._get_moves_queen,
            KING: self._get_moves_king,
        }[piece.type()](piece)

    def get_moves(self) -> Iterable[ChessMove]:
        result = []
        for row in self._board:
            for piece in row:
                piece_moves = []
                if (
                    piece is not None
                    and piece.player() == self._current_player
                ):
                    piece_moves = self._get_moves_piece(piece)
                result += piece_moves
        return result

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
