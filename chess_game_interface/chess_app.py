from chess_game_interface.chess_exceptions import InvalidMoveException
from chess_game_interface.chess_move import ChessMove
from chess_game_interface.chess_pieces import Knight, Bishop, Rook, Queen
from chess_game_interface.chess_game import ChessGame
import pygame
from chess_game_interface.load_svg import load_svg_resize
from chess_game_interface.chess_utils import (
    BACKGROUND_COLOR,
    BLACK,
    BOARD_OFFSET,
    BOARD_OFFSET_CHESS_AREA,
    BOARD_SIZE,
    DARK_BROWN,
    EDGE_COLOR,
    EDGE_SIZE,
    FONT_SIZE,
    GREEN,
    LIGHT_BROWN,
    PIECE_SIZE,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class ChessApp:
    """
    A class responsible for the chess application.


    Attributes:

    screen : pygame.Surface
        a pygame.Surface object representing the window area

    running : bool
        a bool responsible for the infinite loop in the main programme

    promotion_type : type
        a ChessPiece class that determines the piece that a pawn will be
        promoted to

    chess_game : ChessGame
        a ChessGame object representing an instance of a game of chess

    move : ChessMove
        a ChessMove object representing a move that is a result of user input

    move_start_column : int
        an int representing a starting positions column in a move. By default
        set to None. Used in detecting if the first square for a chess move has
        been selected

    move_start_column : int
        an int representing a starting positions row in a move. By default set
        to None. Used in detecting if the first square for a chess move has
        been selected

    moves_list : Iterable[ChessMove]
        a list representing all the possible moves the selected piece can make

    resign : bool
        a bool indicating the side which resigned (True for white, False for
        black). Defaults to None, which signals that noone has resigned.

    reset_button : pygame.Rect
        a pygame.Rect object used for detecting if the reset button has been
        clicked

    resign_button : pygame.Rect
        a pygame.Rect object used for detecting if the resign button has been
        clicked

    promotion_rect_dict : Dict[type, pygame.rect]
        a dictionary used for detecting clicks in the pawn promotion panel
    """

    def __init__(self, icon_pathname: str):
        """
        ChessApp class constructor.


        Parameters:

        icon_pathname : str
            a string representing the path to the icon image in the svg format
        """
        pygame.init()
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound("sounds/chess_move.wav")
        pygame.display.set_caption("Chess")
        self._set_icon(icon_pathname)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = True
        self.promotion_type = None
        self.font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
        self._set_default_attributes()

    def _set_default_attributes(self):
        """
        Sets some of the attributes needed to their default values. Used when
        resetting the board.
        """
        self.chess_game = ChessGame()
        self.move = None
        self.move_start_column = None
        self.move_start_row = None
        self.moves_list = None
        self.resign = None

    def _set_icon(self, pathname: str):
        """
        Sets the icon that shows in the top-left corner of the programme.


        Parameters:

        pathname : str
            a string representing the pathname to the icon image in the svg
            format
        """
        icon = load_svg_resize(pathname, PIECE_SIZE)
        offset = int(7 * PIECE_SIZE / 64)
        cropped_icon = pygame.Surface(
            (
                PIECE_SIZE - 2 * offset,
                PIECE_SIZE - 2 * offset,
            ),
            pygame.SRCALPHA,
        )
        cropped_icon.blit(
            icon,
            (0, 0),
            (offset, offset, PIECE_SIZE - offset, PIECE_SIZE - offset),
        )
        pygame.display.set_icon(cropped_icon)

    def _draw_reset_button(self):
        """
        Draws the reset button and assigns the reset_button attribute an
        appropriate Rect object.
        """
        text = self.font.render("Reset game", True, WHITE, GREEN)
        self.reset_button = text.get_rect()
        text_x = (
            (WINDOW_WIDTH - BOARD_OFFSET - BOARD_SIZE) / 2
            + BOARD_OFFSET
            + BOARD_SIZE
            - self.reset_button.width / 2
        )
        text_y = WINDOW_HEIGHT - BOARD_OFFSET - self.reset_button.height
        self.reset_button.x = text_x
        self.reset_button.y = text_y
        self.screen.blit(
            text,
            (
                text_x,
                text_y,
            ),
        )

    def _draw_player_message(self):
        """
        Draws a message to the right of the board. The message contains info
        about whose turn is it, if a side has won, if there is a draw of if a
        side has resigned.
        """
        if self.chess_game.is_finished():
            winner = self.chess_game.get_winner()
            if winner is None:
                player_text = "The game has been drawn."
            else:
                is_winner_white = winner == self.chess_game.get_white()
                winning_side = "White" if is_winner_white else "Black"
                player_text = f"{winning_side} has won."
        elif self.resign is not None:
            resigning_side = "White" if self.resign else "Black"
            player_text = f"{resigning_side} has resigned."
        else:
            is_current_player_white = (
                self.chess_game.get_current_player()
                == self.chess_game.get_white()
            )
            player_text = (
                f"{'White' if is_current_player_white else 'Black'} to move."
            )
        text = self.font.render(player_text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_offset_x = text_rect.width / 2
        self.screen.blit(
            text,
            (
                (WINDOW_WIDTH - BOARD_OFFSET - BOARD_SIZE) / 2
                + BOARD_OFFSET
                + BOARD_SIZE
                - text_offset_x,
                BOARD_OFFSET,
            ),
        )

    def _draw_resign_button(self):
        """
        Draws the resign button and assigns the resign_button attribute an
        appropriate Rect object.
        """
        text = self.font.render("Resign", True, WHITE, BLACK)
        self.resign_button = text.get_rect()
        text_x = (
            (WINDOW_WIDTH - BOARD_OFFSET - BOARD_SIZE) / 2
            + BOARD_OFFSET
            + BOARD_SIZE
            - self.resign_button.width / 2
        )
        text_y = (
            WINDOW_HEIGHT
            - BOARD_OFFSET
            - 2 * FONT_SIZE
            - self.resign_button.height
        )
        self.resign_button.x = text_x
        self.resign_button.y = text_y
        self.screen.blit(
            text,
            (
                text_x,
                text_y,
            ),
        )

    def _draw_move(self, move: ChessMove):
        """
        Method used for drawing a move from the moves_list attribute for the
        draw_everything function.


        Parameters:

        move : ChessMove
            a ChessMove object representing a move possible to be made using a
            given piece taken from the moves_list attribute
        """
        end_column, end_row = move.end_column(), move.end_row()
        center = (
            BOARD_OFFSET
            + EDGE_SIZE
            + end_column * PIECE_SIZE
            + PIECE_SIZE / 2,
            BOARD_OFFSET
            + EDGE_SIZE
            + (7 - end_row) * PIECE_SIZE
            + PIECE_SIZE / 2,
        )
        radius = PIECE_SIZE / 4
        pygame.draw.circle(self.screen, EDGE_COLOR, center, radius)

    def _draw_promotion_selection_box(self):
        """
        Method used for drawing the promotion selection box as well as
        generating the promotion_rect_dict attribute used for checking which
        of the promotion types has been chosen.
        """
        right_side_center_x = (
            (WINDOW_WIDTH - BOARD_OFFSET - BOARD_SIZE) // 2
            + BOARD_SIZE
            + BOARD_OFFSET
        )
        right_side_center_y = WINDOW_HEIGHT // 2
        pygame.draw.rect(
            self.screen,
            EDGE_COLOR,
            (
                right_side_center_x - PIECE_SIZE // 2 - EDGE_SIZE,
                right_side_center_y - 2 * PIECE_SIZE - EDGE_SIZE,
                2 * EDGE_SIZE + PIECE_SIZE,
                2 * EDGE_SIZE + 4 * PIECE_SIZE,
            ),
        )
        pieces_list = [Queen, Rook, Bishop, Knight]
        self.promotion_rect_dict = {}
        for square in range(4):
            square_origin_x = right_side_center_x - PIECE_SIZE // 2
            square_origin_y = right_side_center_y + (square - 2) * PIECE_SIZE
            pygame.draw.rect(
                self.screen,
                LIGHT_BROWN if square % 2 else DARK_BROWN,
                (
                    square_origin_x,
                    square_origin_y,
                    PIECE_SIZE,
                    PIECE_SIZE,
                ),
            )
            pieces_list[square].draw(
                self.screen,
                self.chess_game.get_current_player()
                == self.chess_game.get_white(),
                square_origin_x,
                square_origin_y,
            )
            self.promotion_rect_dict[pieces_list[square]] = pygame.Rect(
                square_origin_x, square_origin_y, PIECE_SIZE, PIECE_SIZE
            )

    def draw_everything(
        self,
    ):
        """
        This method combines all the other draw methods in this class in order
        to draw the entire screen with all the elements that are needed.
        """
        self.screen.fill(BACKGROUND_COLOR)

        pygame.draw.rect(
            self.screen,
            EDGE_COLOR,
            (BOARD_OFFSET, BOARD_OFFSET, BOARD_SIZE, BOARD_SIZE),
        )

        self.chess_game.draw(
            self.screen,
            BOARD_OFFSET_CHESS_AREA,
            BOARD_OFFSET_CHESS_AREA,
        )

        if self.moves_list is not None:
            for move in self.moves_list:
                self._draw_move(move)

        self._draw_player_message()
        self._draw_reset_button()
        self._draw_resign_button()
        if self.move is not None and self.chess_game.is_promotion(self.move):
            self._draw_promotion_selection_box()
        pygame.display.update()

    def handle_click(self, click_pos_x: int, click_pos_y: int):
        """
        This method handles all the scenarios that can happen after a mouse
        click has been detected.


        Parameters:

        click_pos_x : int
            an int representing the x coordinate of the mouse cursor

        click_pos_y : int
            an int representing the y coordinate of the mouse cursor
        """
        board_column = int(
            (click_pos_x - BOARD_OFFSET - EDGE_SIZE) // PIECE_SIZE
        )
        board_row = int(
            7 - ((click_pos_y - BOARD_OFFSET - EDGE_SIZE) // PIECE_SIZE)
        )
        if (
            board_column in range(8)
            and board_row in range(8)
            and not (
                self.move is not None
                and self.chess_game.is_promotion(self.move)
            )
            and self.resign is None
        ):

            if self.chess_game.is_a_current_players_piece(
                board_column, board_row
            ):
                self.moves_list = self.chess_game.get_moves(
                    board_column, board_row
                )

                if self.moves_list:
                    self.move_start_column, self.move_start_row = (
                        board_column,
                        board_row,
                    )

            elif (
                self.move_start_column is not None
                and self.move_start_row is not None
                and not (
                    board_column == self.move_start_column
                    and board_row == self.move_start_row
                )
            ):

                self.move = ChessMove(
                    self.move_start_column,
                    self.move_start_row,
                    board_column,
                    board_row,
                )

                self.move_start_column = None
                self.move_start_row = None
                self.moves_list = None

            else:

                self.move = None
                self.move_start_column = None
                self.move_start_row = None
                self.moves_list = None

        elif self.move is not None and self.chess_game.is_promotion(self.move):

            promotion_types = [Queen, Rook, Bishop, Knight]
            for promotion in promotion_types:

                if self.promotion_rect_dict[promotion].collidepoint(
                    click_pos_x, click_pos_y
                ):

                    self.promotion_type = promotion
                    break

        elif self.resign_button.collidepoint(click_pos_x, click_pos_y):

            self.resign = (
                self.chess_game.get_current_player()
                == self.chess_game.get_white()
            )

        elif self.reset_button.collidepoint(click_pos_x, click_pos_y):
            self._set_default_attributes()

    def handle_move(self):
        """
        Method used for handling moves and pawn promotions.
        """
        if self.move is not None:
            if (
                self.chess_game.is_promotion(self.move)
                and self.promotion_type is None
            ):
                return
            try:
                self.chess_game.make_move(self.move, self.promotion_type)
                self.move_sound.play()
            except InvalidMoveException:
                pass
            self.moves_list = None
            self.move = None
            self.promotion_type = None
