from two_player_games.two_player_games.game import Game
from two_player_games.two_player_games.player import Player
from chess_move import ChessMove
from chess_state import ChessState


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
