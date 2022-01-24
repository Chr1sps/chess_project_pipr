import pygame
from chess_game_interface.chess_exceptions import (
    CoordinatesOutOfBoundsException,
)
from chess_game_interface.two_player_games.two_player_games.player import (
    Player,
)
from typing import Iterable, Tuple
from itertools import product
from chess_game_interface.chess_move import ChessMove
from chess_game_interface.load_svg import load_svg_resize
from chess_game_interface.chess_utils import PIECE_SIZE


class ChessState:
    """ChessState class definition for typehints."""

    pass


class ChessPiece:
    icons = {True: None, False: None}
    """
    A class that represents a chess piece. Provides attributes and methods for
    child classes. Shouldn't be called explicitly.


    Attributes:

    _column : int
        an integer representing the column of a square that the piece
        resides on

    _row : int
        an integer representing the row of a square that the piece resides on

    _player : Player
        a Player object representing a player to which the piece belongs
    """

    def __init__(
        self,
        column: int,
        row: int,
        player: Player,
    ):
        """
        Constructor of the ChessPiece class. Function checks if the column and
        row arguments are within the range of available coordinates.


        Parameters:

        column : int
            an integer representing the column of a square that the piece
            resides on

        row : int
            an integer representing the row of a square that the piece
            resides on

        player : Player
            a Player object representing a player to which the piece belongs
        """

        if row in range(8) and column in range(8):
            self._row = row
            self._column = column
        else:
            raise CoordinatesOutOfBoundsException

        self._player = player

    def column(self) -> int:
        """Returns an integer representing the column of a square that the
        piece resides on."""
        return self._column

    def row(self) -> int:
        """Returns an integer representing the row of a square that the piece
        resides on."""
        return self._row

    def player(self) -> Player:
        """Returns a Player object representing the player that the piece
        belongs to."""
        return self._player

    def _get_moves_lines(
        self, state: ChessState, directions: Iterable[Tuple[int, int]]
    ) -> Iterable[ChessMove]:
        """
        Returns a list of all possible moves that a piece moving in a line
        would be able to make. This function ONLY takes into consideration
        how a piece moves physically (ie. if it's blocked by other pieces,
        if it can take other pieces and if it's within the board).


        Parameters:

        state : ChessState
            a ChessState object representing the current state of the game
            (the situation on the board, the current player, etc. (more
            info in the ChessState class docs in the chess_state.py file))

        directions : Iterable[Tuple[int]]
            a list containing tuples indicating directions of each of the
            lines. These tuples are of the form (int, int), where both of
            these integers belong to {-1, 0, 1} and both of the values
            aren't equal to 0 simultaneously (eg. (0, 1), (-1, 1)). These
            values correspond to the column and row direction respectively
        """
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
        """
        Returns a list of all possible moves that a piece would be able
        to make given all the possible shifts it is able to make. This
        function ONLY takes into consideration how a piece moves physically
        (ie. if it's blocked by other pieces, if it can take other pieces
        and if it's within the board).


        Parameters:

        state : ChessState
            a ChessState object representing the current state of the game
            (the situation on the board, the current player, etc. (more
            info in the ChessState class docs in the chess_state.py file))

        directions : Iterable[Tuple[int]]
            a list containing tuples indicating all the possible shifts that
            a piece can make. These tuples are of the form (int, int),
            where both of these numbers aren't equal to (eg. (0, 2),
            (-1, 3)). These values correspond to the column and row shift
            respectively
        """
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
        """_get_moves method definition for child classes."""
        pass

    @classmethod
    def draw(
        self,
        screen: pygame.Surface,
        is_white: bool,
        piece_origin_x: int,
        piece_origin_y: int,
    ):
        screen.blit(self.icons[is_white], (piece_origin_x, piece_origin_y))

    def __repr__(self) -> str:
        """Returns object info for debugging (piece type, position)."""
        return f"{type(self).__name__} at \
{chr(self._column + ord('a'))}{self._row + 1}"

    def __str__(self) -> str:
        """__str__ magic method definition for child classes."""
        pass


class Pawn(ChessPiece):
    icons = {
        True: load_svg_resize("chess_icons/white_pawn.svg", PIECE_SIZE),
        False: load_svg_resize("chess_icons/black_pawn.svg", PIECE_SIZE),
    }
    """
    A class that represents a pawn.


    Attributes:

    _column : int
        an integer representing the column of a square that the pawn
        resides on

    _row : int
        an integer representing the row of a square that the pawn
        resides on

    _player : Player
        a Player object representing a player to which the pawn belongs

    _first_move : bool
        a bool that determines if the pawn has the possibility of making
        a move by two squares forward (as its first move)

    _is_en_passantable : bool
        a bool that determines if a pawn can be taken en passant
    """

    def __init__(
        self,
        column: int,
        row: int,
        player: Player,
        first_move: bool = True,
        is_en_passantable: bool = False,
    ):
        """
        Constructor of the Pawn class. Function checks if the column and
        row arguments are within the range of available coordinates.


        Parameters:

        column : int
            an integer representing the column of a square that the pawn
            resides on

        row : int
            an integer representing the row of a square that the pawn
            resides on

        player : Player
            a Player object representing a player to which the piece belongs

        first_move : bool
            a bool that determines if the pawn has the possibility of making
            a move by two squares forward (as its first move)

        is_en_passantable : bool
            a bool that determines if a pawn can be taken en passant
        """
        super().__init__(column, row, player)
        self._first_move = first_move
        self._is_en_passantable = is_en_passantable

    def is_en_passantable(self) -> bool:
        """Returns a bool determining if a pawn can be taken en passant."""
        return self._is_en_passantable

    def first_move(self) -> bool:
        """Returns a bool determining if a pawn can make it's first move."""
        return self._first_move

    def __str__(self) -> str:
        """Returns a string representing a pawn. Used in the __str__ function
        of the ChessState class. Indicates the pawn's player."""
        return f"P{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        """
        Returns a list of all possible moves that a pawn would be able
        to make. This function ONLY takes into consideration how a
        piece moves physically ((ie. if it's blocked by other pieces,
        if it can take other pieces and if it's within the board).


        Parameters:

        state : ChessState
            a ChessState object representing the current state of the game
            (the situation on the board, the current player, etc. (more
            info in the ChessState class docs in the chess_state.py file))
        """
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
            and state._board[self._row + row_shift][self._column] is None
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
    icons = {
        True: load_svg_resize("chess_icons/white_knight.svg", PIECE_SIZE),
        False: load_svg_resize("chess_icons/black_knight.svg", PIECE_SIZE),
    }

    def __str__(self) -> str:
        """Returns a string representing a knight. Used in the __str__ function
        of the ChessState class. Indicates the knight's player."""
        return f"N{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        """
        Returns a list of all possible moves that a bishop would be
        able to make. This function ONLY takes into consideration how a
        knight moves physically ((ie. if it's blocked by other pieces,
        if it can take other pieces and if it's within the board).


        Parameters:

        state : ChessState
            a ChessState object representing the current state of the game
            (the situation on the board, the current player, etc. (more
            info in the ChessState class docs in the chess_state.py file))
        """

        possible_shifts = list(product((-2, 2), (-1, 1))) + list(
            product((-1, 1), (-2, 2))
        )
        return self._get_moves_shifts(state, possible_shifts)


class Bishop(ChessPiece):
    icons = {
        True: load_svg_resize("chess_icons/white_bishop.svg", PIECE_SIZE),
        False: load_svg_resize("chess_icons/black_bishop.svg", PIECE_SIZE),
    }

    def __str__(self) -> str:
        """Returns a string representing a bishop. Used in the __str__ function
        of the ChessState class. Indicates the bishop's player."""
        return f"B{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        """
        Returns a list of all possible moves that a bishop would be
        able to make. This function ONLY takes into consideration how a
        bishop moves physically ((ie. if it's blocked by other pieces,
        if it can take other pieces and if it's within the board).


        Parameters:

        state : ChessState
            a ChessState object representing the current state of the game
            (the situation on the board, the current player, etc. (more
            info in the ChessState class docs in the chess_state.py file))
        """
        return self._get_moves_lines(state, product((-1, 1), (-1, 1)))


class Rook(ChessPiece):
    icons = {
        True: load_svg_resize("chess_icons/white_rook.svg", PIECE_SIZE),
        False: load_svg_resize("chess_icons/black_rook.svg", PIECE_SIZE),
    }
    """
    A class that represents a rook.


    Atributes:

    _column : int
        an integer representing the column of a square that the rook
        resides on

    _row : int
        an integer representing the row of a square that the rook
        resides on

    _player : Player
        a Player object representing a player to which the rook belongs

    _can_castle : bool
        a bool that determines if the rook has the possibility of castling
    """

    def __init__(
        self,
        column: int,
        row: int,
        player: Player,
        can_castle: bool = True,
    ):
        """
        Constructor of the Rook class. Function checks if the column and
        row arguments are within the range of available coordinates.


        Parameters:

        column : int
            an integer representing the column of a square that the rook
            resides on

        row : int
            an integer representing the row of a square that the rook
            resides on

        player : Player
            a Player object representing a player to which the rook belongs

        can_castle : bool
            a bool that determines if the rook has the possibility of castling
        """
        super().__init__(column, row, player)
        self._can_castle = can_castle

    def can_castle(self):
        """Returns a bool determining if the rook can castle."""
        return self._can_castle

    def __str__(self) -> str:
        """Returns a string representing a rook. Used in the __str__ function
        of the ChessState class. Indicates the rook's player."""
        return f"R{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        """
        Returns a list of all possible moves that a rook would be
        able to make. This function ONLY takes into consideration how a
        rook moves physically ((ie. if it's blocked by other pieces,
        if it can take other pieces and if it's within the board).


        Parameters:

        state : ChessState
            a ChessState object representing the current state of the game
            (the situation on the board, the current player, etc. (more
            info in the ChessState class docs in the chess_state.py file))
        """

        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        return self._get_moves_lines(state, directions)


class Queen(ChessPiece):
    icons = {
        True: load_svg_resize("chess_icons/white_queen.svg", PIECE_SIZE),
        False: load_svg_resize("chess_icons/black_queen.svg", PIECE_SIZE),
    }

    def __str__(self) -> str:
        """Returns a string representing a queen. Used in the __str__ function
        of the ChessState class. Indicates the queen's player."""
        return f"Q{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        """
        Returns a list of all possible moves that a queen would be
        able to make. This function ONLY takes into consideration how a
        queen moves physically ((ie. if it's blocked by other pieces,
        if it can take other pieces and if it's within the board).


        Parameters:

        state : ChessState
            a ChessState object representing the current state of the game
            (the situation on the board, the current player, etc. (more
            info in the ChessState class docs in the chess_state.py file))
        """

        directions = list(product((1, 0, -1), (1, 0, -1)))
        directions.remove((0, 0))
        return self._get_moves_lines(state, directions)


class King(ChessPiece):
    icons = {
        True: load_svg_resize("chess_icons/white_king.svg", PIECE_SIZE),
        False: load_svg_resize("chess_icons/black_king.svg", PIECE_SIZE),
    }
    """
    A class that represents a king.


    Atributes:

    _column : int
        an integer representing the column of a square that the king
        resides on

    _row : int
        an integer representing the row of a square that the king
        resides on

    _player : Player
        a Player object representing a player to which the king belongs

    _can_castle : bool
        a bool that determines if the king has the possibility of castling
    """

    def __init__(
        self,
        column: int,
        row: int,
        player: Player,
        can_castle: bool = True,
    ):
        """
        Constructor of the King class. Function checks if the column and
        row arguments are within the range of available coordinates.


        Parameters:

        column : int
            an integer representing the column of a square that the king
            resides on

        row : int
            an integer representing the row of a square that the king
            resides on

        player : Player
            a Player object representing a player to which the king belongs

        can_castle : bool
            a bool that determines if the king has the possibility of castling
        """
        super().__init__(column, row, player)
        self._can_castle = can_castle

    def can_castle(self):
        """Returns a bool determining if the king can castle."""
        return self._can_castle

    def __str__(self) -> str:
        """Returns a string representing a king. Used in the __str__ function
        of the ChessState class. Indicates the king's player."""
        return f"K{self._player.char}"

    def _get_moves(self, state: ChessState) -> Iterable[ChessMove]:
        """
        Returns a list of all possible moves that a king would be
        able to make. This function ONLY takes into consideration how a
        king moves physically ((ie. if it's blocked by other pieces,
        if it can take other pieces and if it's within the board) and if
        it can castle.


        Parameters:

        state : ChessState
            a ChessState object representing the current state of the game
            (the situation on the board, the current player, etc. (more
            info in the ChessState class docs in the chess_state.py file))
        """

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
