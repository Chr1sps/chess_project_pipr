from pydoc import cli
from chess_game_interface.chess_exceptions import InvalidMoveException
from chess_game_interface.chess_move import ChessMove
from chess_game_interface.chess_pieces import Knight, Bishop, Rook, Queen
from chess_game_interface.chess_game import ChessGame
import pygame
from chess_io import load_svg_resize

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (96, 96, 96)
LIGHT_BROWN = (255, 206, 158)
DARK_BROWN = (209, 139, 71)
EDGE_COLOR = (128, 64, 48)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
PIECE_SIZE = 64
EDGE_SIZE = 16
BOARD_SIZE = 8 * PIECE_SIZE + 2 * EDGE_SIZE
BOARD_OFFSET = (WINDOW_HEIGHT - BOARD_SIZE) / 2
BOARD_OFFSET_CHESS_AREA = BOARD_OFFSET + EDGE_SIZE
FONT_SIZE = 24


class ChessApp:
    def __init__(self, icon_pathname: str):
        pygame.init()
        pygame.display.set_caption("Chess")
        self.set_icon(icon_pathname)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = True
        self.promotion_type = Queen
        self._set_default_attributes()

    def _set_default_attributes(self):
        self.chess_game = ChessGame()
        self.move = None
        self.move_start_column = None
        self.move_start_row = None
        self.moves_list = None
        self.resign = None

    def set_icon(self, pathname: str):
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

    def draw_reset_button(self):
        font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
        text = font.render("Reset game", True, WHITE, GREEN)
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

    def draw_player_message(self):
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
        font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
        text = font.render(player_text, True, (0, 0, 0))
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

    def draw_resign_button(self):
        font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
        text = font.render("Resign", True, WHITE, BLACK)
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

    def draw_move(self, move: ChessMove):
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

    def draw_everything(
        self,
    ):
        self.screen.fill(BACKGROUND_COLOR)

        pygame.draw.rect(
            self.screen,
            EDGE_COLOR,
            (BOARD_OFFSET, BOARD_OFFSET, BOARD_SIZE, BOARD_SIZE),
        )

        self.chess_game.draw(
            self.screen,
            PIECE_SIZE,
            BOARD_OFFSET_CHESS_AREA,
            BOARD_OFFSET_CHESS_AREA,
        )

        if self.moves_list is not None:
            for move in self.moves_list:
                self.draw_move(move)

        self.draw_player_message()
        self.draw_reset_button()
        self.draw_resign_button()
        pygame.display.update()

    def handle_click(self, click_pos_x: int, click_pos_y: int):
        print(
            self.resign_button.x,
            self.resign_button.y,
            self.resign_button.size,
        )
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
                print("A move has been prepared.")
            else:
                self.move = None
                self.move_start_column = None
                self.move_start_row = None
                self.moves_list = None

        elif self.resign_button.collidepoint(click_pos_x, click_pos_y):
            self.resign = (
                self.chess_game.get_current_player()
                == self.chess_game.get_white()
            )

        elif self.reset_button.collidepoint(click_pos_x, click_pos_y):
            self._set_default_attributes()

    def handle_move(self):
        if self.move is not None:
            if self.chess_game.is_promotion(self.move):
                return
            try:
                self.chess_game.make_move(self.move, self.promotion_type)
            except InvalidMoveException:
                pass
            self.moves_list = None
            self.move = None
            print(self.move if self.move is not None else "None")


def main():
    icon = "chess_icons/white_knight.svg"
    app = ChessApp(icon)

    while app.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                app.handle_click(mouse_x, mouse_y)

        app.handle_move()

        app.draw_everything()


if __name__ == "__main__":
    main()
