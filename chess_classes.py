from typing import Iterable, List, Optional
from two_player_games.two_player_games.game import Game
from two_player_games.two_player_games.state import State
from two_player_games.two_player_games.player import Player
from two_player_games.two_player_games.move import Move
from itertools import product


class CoordinatesOutOfBoundsException(Exception):
    def __init__(self):
        super().__init__("Coordinate(s) out of bounds in the called function.")


class IncorrectPieceTypeException(Exception):
    def __init__(self):
        super().__init__("Wrong chess piece type in the called function.")


class InvalidMoveException(Exception):
    def __init__(self):
        super().__init__("Invalid move given to the function.")


class ChessState:
    pass


class ChessMove:
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
        row_shift = 1 if self.player() == state._white else -1
        right_column = self.column() + 1
        left_column = self.column() - 1

        if state._board[self.row() + row_shift][self.column()] is None:
            result.append(
                ChessMove(
                    self.column(),
                    self.row(),
                    self.column(),
                    self.row() + row_shift,
                )
            )
        if (
            self._first_move
            and state._board[self.row() + 2 * row_shift][self.column()] is None
        ):
            result.append(
                ChessMove(
                    self.column(),
                    self.row(),
                    self.column(),
                    self.row() + 2 * row_shift,
                )
            )
        if right_column in range(8):
            right_diagonal = state._board[self.row() + row_shift][right_column]
            if (
                right_diagonal is not None
                and right_diagonal.player() != self.player()
            ):
                result.append(
                    ChessMove(
                        self.column(),
                        self.row(),
                        right_column,
                        self.row() + row_shift,
                    )
                )

            right_square = state._board[self.row()][right_column]
            if (
                right_square is not None
                and type(right_square) == Pawn
                and right_square.player() != self.player()
                and right_square.is_en_passantable
                and right_diagonal is None
            ):
                result.append(
                    ChessMove(
                        self.column(),
                        self.row(),
                        right_column,
                        self.row() + row_shift,
                    )
                )

        if left_column in range(8):
            left_diagonal = state._board[self.row() + row_shift][left_column]
            if (
                left_diagonal is not None
                and left_diagonal.player() != self.player()
            ):
                result.append(
                    ChessMove(
                        self.column(),
                        self.row(),
                        left_column,
                        self.row() + row_shift,
                    )
                )

            left_square = state._board[self.row()][left_column]
            if (
                left_square is not None
                and type(left_square) == Pawn
                and left_square.player() != self.player()
                and left_square.is_en_passantable
                and left_diagonal is None
            ):
                result.append(
                    ChessMove(
                        self.column(),
                        self.row(),
                        left_column,
                        self.row() + row_shift,
                    )
                )

        return result


class Knight(ChessPiece):
    def __str__(self) -> str:
        return f"N{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        result = []
        possible_shifts = list(product((-2, 2), (-1, 1))) + list(
            product((-1, 1), (-2, 2))
        )
        for position in possible_shifts:
            new_column, new_row = position
            new_column += self.column()
            new_row += self.row()
            if new_column not in range(8) or new_row not in range(8):
                continue
            possible_square = state._board[new_row][new_column]
            if not (
                possible_square is not None
                and possible_square.player() == self.player()
            ):
                result.append(
                    ChessMove(
                        self.column(),
                        self.row(),
                        new_column,
                        new_row,
                    )
                )
        return result


class Bishop(ChessPiece):
    def __str__(self) -> str:
        return f"B{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        result = []
        for direction in product((-1, 1), (-1, 1)):
            dir_column, dir_row = direction
            for distance in range(1, 8):
                new_column = self.column() + distance * dir_column
                new_row = self.row() + distance * dir_row
                if new_column not in range(8) or new_row not in range(8):
                    break
                possible_square = state._board[new_row][new_column]
                if not (
                    possible_square is not None
                    and possible_square.player() == self.player()
                ):
                    result.append(
                        ChessMove(
                            self.column(),
                            self.row(),
                            new_column,
                            new_row,
                        )
                    )
                if possible_square is not None:
                    break
        return result


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
        result = []
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        for direction in directions:
            dir_column, dir_row = direction
            for distance in range(1, 8):
                new_column = self.column() + distance * dir_column
                new_row = self.row() + distance * dir_row
                if new_column not in range(8) or new_row not in range(8):
                    continue
                possible_square = state._board[new_row][new_column]
                if not (
                    possible_square is not None
                    and possible_square.player() == self.player()
                ):
                    result.append(
                        ChessMove(
                            self.column(),
                            self.row(),
                            new_column,
                            new_row,
                        )
                    )
                if possible_square is not None:
                    break
        return result


class Queen(ChessPiece):
    def __str__(self) -> str:
        return f"Q{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        result = []
        directions = list(product((1, 0, -1), (1, 0, -1)))
        directions.remove((0, 0))
        for direction in directions:
            dir_column, dir_row = direction
            for distance in range(1, 8):
                new_column = self.column() + distance * dir_column
                new_row = self.row() + distance * dir_row
                if new_column not in range(8) or new_row not in range(8):
                    continue
                possible_square = state._board[new_row][new_column]
                if not (
                    possible_square is not None
                    and possible_square.player() == self.player()
                ):
                    result.append(
                        ChessMove(
                            self.column(),
                            self.row(),
                            new_column,
                            new_row,
                        )
                    )
                if possible_square is not None:
                    break
        return result


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

        result = []
        possible_shifts = list(product((1, 0, -1), (1, 0, -1)))
        possible_shifts.remove((0, 0))

        for shift in possible_shifts:

            new_column, new_row = shift
            new_column += self.column()
            new_row += self.row()

            if new_column not in range(8) or new_row not in range(8):
                continue

            possible_square = state._board[new_row][new_column]
            if not (
                possible_square is not None
                and possible_square.player() == self.player()
            ):
                result.append(
                    ChessMove(self.column(), self.row(), new_column, new_row)
                )

        if self.column() == 4 and self.can_castle():

            left_corner = state._board[self.row()][0]
            if (
                left_corner
                and type(left_corner) == Rook
                and left_corner.player() == self.player()
                and left_corner.can_castle()
                and all(
                    state._board[self.row()][column] is None
                    for column in range(1, 4)
                )
            ):
                result.append(
                    ChessMove(self.column(), self.row(), 2, self.row())
                )

            right_corner = state._board[self.row()][7]
            if (
                right_corner
                and type(right_corner) == Rook
                and right_corner.player() == self.player()
                and right_corner.can_castle()
                and all(
                    state._board[self.row()][column] is None
                    for column in range(5, 7)
                )
            ):
                result.append(
                    ChessMove(self.column(), self.row(), 6, self.row())
                )

        return result


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
                    Rook(0, 0, white),
                    Knight(1, 0, white),
                    Bishop(2, 0, white),
                    Queen(3, 0, white),
                    King(4, 0, white),
                    Bishop(5, 0, white),
                    Knight(6, 0, white),
                    Rook(7, 0, white),
                ],
                [Pawn(column_index, 1, white) for column_index in range(8)],
                [None for column in range(8)],
                [None for column in range(8)],
                [None for column in range(8)],
                [None for column in range(8)],
                [Pawn(column_index, 6, black) for column_index in range(8)],
                [
                    Rook(0, 7, black),
                    Knight(1, 7, black),
                    Bishop(2, 7, black),
                    Queen(3, 7, black),
                    King(4, 7, black),
                    Bishop(5, 7, black),
                    Knight(6, 7, black),
                    Rook(7, 7, black),
                ],
            ]

        self._current_player = current_player
        self._other_player = other_player

        self._white = white or current_player

    def get_moves(self) -> Iterable[ChessMove]:

        result = []

        for row in self._board:
            for piece in row:
                piece_moves = []
                if (
                    piece is not None
                    and piece.player() == self._current_player
                ):
                    piece_moves = piece._get_moves(self)
                result += piece_moves
        return result

    def get_current_player(self) -> Player:
        return self._current_player

    def _get_current_players_king(self) -> ChessPiece:
        for row in self._board:
            for square in row:
                if (
                    square is not None
                    and type(square) == King
                    and square.player() == self._current_player
                ):
                    return square

    def _make_piece(
        self,
        piece_type: type,
        column: int,
        row: int,
        player: Player,
        first_move_or_can_castle=False,
        is_en_passantable=False,
    ):
        if piece_type == Pawn:
            return Pawn(
                column,
                row,
                player,
                first_move_or_can_castle,
                is_en_passantable,
            )
        elif piece_type in (Rook, King):
            return piece_type(
                column,
                row,
                player,
                first_move_or_can_castle,
            )
        else:
            return piece_type(
                column,
                row,
                player,
            )

    def _piece_shift(
        self,
        move: ChessMove,
        moved_piece: ChessPiece,
        first_move_or_can_castle=False,
        is_en_passantable=False,
    ) -> List[List[ChessPiece]]:

        new_board = [[square for square in row] for row in self._board]
        new_board[move.start_row()][move.start_column()] = None
        new_board[move.end_row()][move.end_column()] = self._make_piece(
            type(moved_piece),
            move.end_column(),
            move.end_row(),
            moved_piece.player(),
            first_move_or_can_castle,
            is_en_passantable,
        )
        return new_board

    def _evaluate_pawn_scenarios(
        self,
        move: ChessMove,
        moved_piece: ChessPiece,
        promotion_type: type = None,
    ) -> List[List[ChessPiece]]:
        row_shift = move.end_row() - move.start_row()
        column_shift = move.end_column() - move.start_column()

        if self.is_promotion(move):
            if promotion_type in (Knight, Bishop, Rook, Queen):
                moved_piece = self._make_piece(
                    promotion_type,
                    moved_piece.column(),
                    moved_piece.row(),
                    moved_piece.player(),
                    False,
                )
            else:
                raise IncorrectPieceTypeException

        # first move
        if row_shift in (-2, 2):
            new_board = self._piece_shift(
                move,
                moved_piece,
                False,
                True,
            )

        # en passant and taking
        elif column_shift in (-1, 1):
            piece_next_to_the_pawn = self._board[moved_piece.row()][
                move.end_column()
            ]
            new_board = self._piece_shift(
                move,
                moved_piece,
            )
            if (
                piece_next_to_the_pawn is not None
                and type(piece_next_to_the_pawn) == Pawn
                and piece_next_to_the_pawn.player() != moved_piece.player()
                and piece_next_to_the_pawn.is_en_passantable()
            ):
                new_board[moved_piece.row()][move.end_column()] = None

        else:  # move forward by one square
            new_board = self._piece_shift(
                move,
                moved_piece,
            )

        return new_board

    def _is_in_check(self, state: "ChessState" = None) -> bool:
        if state is None:
            state = self
        state_switched_sides = ChessState(
            state._other_player,
            state._current_player,
            state._white,
            state._board,
        )
        current_king = state._get_current_players_king()
        current_king_pos = (current_king.column(), current_king.row())
        state_switched_sides_end_positions = [
            (move.end_column(), move.end_row())
            for move in state_switched_sides.get_moves()
        ]
        if current_king_pos in state_switched_sides_end_positions:
            return True
        return False

    def _evaluate_castling_scenarios(
        self,
        move: ChessMove,
        moved_piece: ChessPiece,
        board: List[List[ChessPiece]],
    ) -> List[List[ChessPiece]]:

        new_board = [[square for square in row] for row in board]

        squares_enemy_can_attack = [
            (enemy_move.end_column(), enemy_move.end_row())
            for enemy_move in ChessState(
                self._other_player,
                self._current_player,
                self._white,
                self._board,
            ).get_moves()
        ]

        king_shift_dir = move.end_column() - move.start_column()
        king_shift_dir = king_shift_dir // abs(king_shift_dir)

        squares_to_check = (
            (column, 0)
            for column in range(
                4, move.end_column() + king_shift_dir, king_shift_dir
            )
        )

        if any(
            square in squares_enemy_can_attack for square in squares_to_check
        ):

            raise InvalidMoveException

        else:

            new_board[0][4 + king_shift_dir] = self._make_piece(
                Rook, 4 + king_shift_dir, 0, self._current_player, False
            )

            new_board[0][int(3.5 + 3.5 * king_shift_dir)] = None

        return new_board

    def make_move(
        self, move: ChessMove, promotion_type: type = None
    ) -> "ChessState":
        moved_piece = self._board[move.start_row()][move.start_column()]
        valid_moves = self.get_moves()
        if move not in valid_moves:
            raise InvalidMoveException

        if type(moved_piece) == Pawn:
            new_board = self._evaluate_pawn_scenarios(
                move, moved_piece, promotion_type
            )

        else:
            new_board = self._piece_shift(
                move,
                moved_piece,
            )

        if type(moved_piece) == King and move in (
            ChessMove(4, 0, 2, 0),
            ChessMove(4, 0, 6, 0),
        ):
            new_board = self._evaluate_castling_scenarios(
                move, moved_piece, new_board
            )

        new_state = ChessState(
            self._other_player, self._current_player, self._white, new_board
        )

        new_state_current_player = ChessState(
            self._current_player, self._other_player, self._white, new_board
        )

        if self._is_in_check(new_state_current_player):
            raise InvalidMoveException

        return new_state

    def is_promotion(self, move: ChessMove) -> bool:
        moved_piece = self._board[move.start_row()][move.start_column()]
        if (
            moved_piece is not None
            and type(moved_piece) == Pawn
            and move.end_row()
            == (7 if moved_piece.player() == self._white else 0)
        ):
            return True
        return False

    def is_finished(self) -> bool:
        get_moves_list = self.get_moves()
        for move in get_moves_list:
            try:
                self.make_move(move)
                return False
            except InvalidMoveException:
                continue
        return True

    def get_winner(self) -> Optional[Player]:
        if self.is_finished() and self._is_in_check():
            return self._other_player
        return None

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

    FIRST_PLAYER_DEFAULT_CHAR = "W"
    SECOND_PLAYER_DEFAULT_CHAR = "B"

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

    def is_promotion(self, move: ChessMove) -> bool:
        return self.state.is_promotion(move)

    def make_move(self, move: ChessMove, promotion_type: int = None):
        self.state = self.state.make_move(move, promotion_type)
