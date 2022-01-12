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


class InvalidMoveException(Exception):
    def __init__(self):
        super().__init__("Invalid move given to the function.")


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
        return f"{self._start_column} {self._start_row} move to {self._end_column} {self._end_row}"


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
                ChessMove(
                    pawn.column(),
                    pawn.row(),
                    pawn.column(),
                    pawn.row() + row_shift,
                )
            )
        if (
            pawn.first_move
            and self._board[pawn.row() + 2 * row_shift][pawn.column()] is None
        ):
            result.append(
                ChessMove(
                    pawn.column(),
                    pawn.row(),
                    pawn.column(),
                    pawn.row() + 2 * row_shift,
                )
            )
        if right_column in range(8):
            right_diagonal = self._board[pawn.row() + row_shift][right_column]
            if (
                right_diagonal is not None
                and right_diagonal.player() != pawn.player()
            ):
                result.append(
                    ChessMove(
                        pawn.column(),
                        pawn.row(),
                        right_column,
                        pawn.row() + row_shift,
                    )
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
                    ChessMove(
                        pawn.column(),
                        pawn.row(),
                        right_column,
                        pawn.row() + row_shift,
                    )
                )

        if left_column in range(8):
            left_diagonal = self._board[pawn.row() + row_shift][left_column]
            if (
                left_diagonal is not None
                and left_diagonal.player() != pawn.player()
            ):
                result.append(
                    ChessMove(
                        pawn.column(),
                        pawn.row(),
                        left_column,
                        pawn.row() + row_shift,
                    )
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
                    ChessMove(
                        pawn.column(),
                        pawn.row(),
                        left_column,
                        pawn.row() + row_shift,
                    )
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
                result.append(
                    ChessMove(
                        knight.column(),
                        knight.row(),
                        new_column,
                        new_row,
                    )
                )
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
                    result.append(
                        ChessMove(
                            bishop.column(),
                            bishop.row(),
                            new_column,
                            new_row,
                        )
                    )
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
                    result.append(
                        ChessMove(
                            rook.column(),
                            rook.row(),
                            new_column,
                            new_row,
                        )
                    )
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
                result.append(
                    ChessMove(king.column(), king.row(), new_column, new_row)
                )

        if king.column() == 4 and king.can_castle:

            left_corner = self._board[king.row()][0]
            if (
                left_corner
                and left_corner.type() == ROOK
                and left_corner.player() == king.player()
                and left_corner.can_castle
                and all(
                    self._board[king.row()][column] is None
                    for column in range(1, 4)
                )
            ):
                result.append(
                    ChessMove(king.column(), king.row(), 2, king.row())
                )

            right_corner = self._board[king.row()][7]
            if (
                right_corner
                and right_corner.type() == ROOK
                and right_corner.player() == king.player()
                and right_corner.can_castle
                and all(
                    self._board[king.row()][column] is None
                    for column in range(5, 7)
                )
            ):
                result.append(
                    ChessMove(king.column(), king.row(), 6, king.row())
                )

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

    def _get_current_players_king(self) -> ChessPiece:
        for row in self._board:
            for square in row:
                if (
                    square is not None
                    and square.type() == KING
                    and square.player() == self._current_player
                ):
                    return square

    def make_move(self, move: ChessMove) -> "ChessState":
        new_board = [[square for square in row] for row in self._board]
        valid_moves = self.get_moves()
        if move not in valid_moves:
            raise InvalidMoveException
        moved_piece = new_board[move.start_row()][move.start_column()]
        new_board[move.start_row()][move.start_column()] = None
        # ^ might accidentally delete the moved_piece object !

        if moved_piece.type() == PAWN:
            row_shift = move.end_row() - move.start_row()
            column_shift = move.end_column() - move.start_column()

            if row_shift in (-2, 2):  # first move
                new_board[move.end_row()][move.end_column()] = ChessPiece(
                    PAWN,
                    move.end_column(),
                    move.end_row(),
                    moved_piece.player(),
                    False,
                    True,
                )

            elif column_shift in (
                -1,
                1,
            ):  # en passant and taking
                piece_next_to_the_pawn = self._board[moved_piece.row()][
                    move.end_column()
                ]
                if (
                    piece_next_to_the_pawn.type() == PAWN
                    and piece_next_to_the_pawn.player() != moved_piece.player()
                    and piece_next_to_the_pawn.is_en_passantable()
                ):
                    new_board[moved_piece.row()][move.end_column()] = None
                new_board[move.end_row()][move.end_column()] = ChessPiece(
                    PAWN,
                    move.end_column(),
                    move.end_row(),
                    moved_piece.player(),
                    False,
                    False,
                )

            else:
                new_board[move.end_row()][move.end_column()] = ChessPiece(
                    PAWN,
                    move.end_column(),
                    move.end_row(),
                    moved_piece.player(),
                    False,
                    False,
                )

        elif moved_piece.type() in (ROOK, KING):
            new_board[move.end_row()][move.end_column()] = ChessPiece(
                moved_piece.type(),
                move.end_column(),
                move.end_row(),
                moved_piece.player(),
                False,
            )

        else:
            new_board[move.end_row()][move.end_column()] = ChessPiece(
                moved_piece.type(),
                move.end_column(),
                move.end_row(),
                moved_piece.player(),
            )

        if moved_piece.type() == KING:
            possible_end_positions_other_player = [
                (enemy_move.end_column(), enemy_move.end_row())
                for enemy_move in ChessState(
                    self._other_player,
                    self._current_player,
                    self._white,
                    self._board,
                ).get_moves()
            ]
            if move == ChessMove(4, 0, 6, 0):
                squares_to_check = ((4, 0), (5, 0), (6, 0))
                if any(
                    square in possible_end_positions_other_player
                    for square in squares_to_check
                ):
                    raise InvalidMoveException
                else:
                    new_board[0][5] = ChessPiece(
                        ROOK, 5, 0, self._current_player, False
                    )
                    new_board[0][7] = None
            elif move == ChessMove(4, 0, 2, 0):
                squares_to_check = ((4, 0), (3, 0), (2, 0))
                if any(
                    square in possible_end_positions_other_player
                    for square in squares_to_check
                ):
                    raise InvalidMoveException
                else:
                    new_board[0][3] = ChessPiece(
                        ROOK, 3, 0, self._current_player, False
                    )
                    new_board[0][0] = None

        new_state = ChessState(
            self._other_player, self._current_player, self._white, new_board
        )
        new_state_current_player = ChessState(
            self._current_player, self._other_player, self._white, new_board
        )
        new_state_current_player_king = (
            new_state_current_player._get_current_players_king()
        )
        new_state_current_player_king_pos = (
            new_state_current_player_king.column(),
            new_state_current_player_king.row(),
        )
        new_state_moves_end_positions = [
            (new_move.end_column(), new_move.end_row())
            for new_move in new_state.get_moves()
        ]
        if new_state_current_player_king_pos in new_state_moves_end_positions:
            raise InvalidMoveException
        return new_state

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
