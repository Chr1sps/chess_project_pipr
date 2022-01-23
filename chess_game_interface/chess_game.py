from chess_game_interface.two_player_games.two_player_games.game import Game
from chess_game_interface.two_player_games.two_player_games.player import (
    Player,
)
from chess_game_interface.chess_move import ChessMove
from chess_game_interface.chess_state import ChessState


class ChessGame(Game):
    """
    A class that represents a chess game.


    Attributes:

    state : ChessState
        a ChessState object that represents the current state of the board
        (which player is playing the move, which player is waiting for their
        move, which player is playing white, what pieces are on the board,
        etc.)
    """

    FIRST_PLAYER_DEFAULT_CHAR = "W"
    SECOND_PLAYER_DEFAULT_CHAR = "B"

    def __init__(
        self, first_player: Player = None, second_player: Player = None
    ):
        """
        ChessGame class constructor.


        Parameters:

        first_player : Player
            a Player object that represents the player moving first in the game
            (and, therefore, playing white)

        second_player : Player
            a Player object representing the player moving second in the game
            (and, therefore, playing black)
        """
        _first_player = first_player or Player(self.FIRST_PLAYER_DEFAULT_CHAR)
        _second_player = second_player or Player(
            self.SECOND_PLAYER_DEFAULT_CHAR
        )

        state = ChessState(_first_player, _second_player)

        super().__init__(state)

    def is_promotion(self, move: ChessMove) -> bool:
        """
        Returns True if a move will result in a promotion.


        Parameters:

        move : ChessMove
            a ChessMove object representing a move
        """
        return self.state.is_promotion(move)

    def make_move(self, move: ChessMove, promotion_type: type = None):
        """
        Makes a move and updates the state attribute accordingly.


        Parameters:

        move : ChessMove
            a ChessMove object representing the move being made

        promotion_type : type
            a type that represents the class of a piece to which the pawn will
            promote
        """
        self.state = self.state.make_move(move, promotion_type)
