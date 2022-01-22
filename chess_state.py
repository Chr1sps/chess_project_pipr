from two_player_games.two_player_games.state import State
from two_player_games.two_player_games.player import Player
from chess_exceptions import InvalidMoveException, IncorrectPieceTypeException
from chess_pieces import ChessPiece, Pawn, Knight, Bishop, Rook, Queen, King
from chess_move import ChessMove
from typing import Iterable, List, Optional


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
    ) -> ChessPiece:
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
            piece_pawn_end_position = self._board[move.end_row()][
                move.end_column()
            ]
            if (
                piece_next_to_the_pawn is not None
                and type(piece_next_to_the_pawn) == Pawn
                and piece_next_to_the_pawn.player() != moved_piece.player()
                and piece_next_to_the_pawn.is_en_passantable()
            ):
                new_board = self._piece_shift(
                    move,
                    moved_piece,
                )
                new_board[moved_piece.row()][move.end_column()] = None
            elif (
                piece_pawn_end_position is not None
                and piece_pawn_end_position.player() == self._other_player
            ):
                new_board = self._piece_shift(
                    move,
                    moved_piece,
                )
            else:
                raise InvalidMoveException

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

    def _reset_en_passantable_pawns(self):
        row = 3 if self._current_player == self._white else 4
        for piece in self._board[row]:
            if (
                piece is not None
                and type(piece) == Pawn
                and piece.player() == self._current_player
                and piece.is_en_passantable()
            ):
                self._board[row][piece.column()] = Pawn(
                    piece.column(), row, self._current_player, False, False
                )

    def make_move(
        self, move: ChessMove, promotion_type: type = None
    ) -> "ChessState":
        self._reset_en_passantable_pawns()

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
