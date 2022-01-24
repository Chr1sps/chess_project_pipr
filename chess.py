from typing import Iterable
from chess_game_interface.chess_exceptions import InvalidMoveException
from chess_game_interface.chess_move import ChessMove
from chess_game_interface.chess_pieces import Knight, Bishop, Rook, Queen
from chess_game_interface.chess_game import ChessGame
import pygame
from io import BytesIO
from chess_io import load_svg_resize

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (96, 96, 96)
LIGHT_BROWN = (255, 206, 158)
DARK_BROWN = (209, 139, 71)
EDGE_COLOR = (128, 64, 48)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
PIECE_SIZE = 64
EDGE_SIZE = 16
BOARD_SIZE = 8 * PIECE_SIZE + 2 * EDGE_SIZE
BOARD_OFFSET = (WINDOW_HEIGHT - BOARD_SIZE) / 2
BOARD_OFFSET_CHESS_AREA = BOARD_OFFSET + EDGE_SIZE


class ChessApp:
    def __init__(self, icon_pathname: str):
        pygame.init()
        self.set_icon(icon_pathname)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.chess_game = ChessGame

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
        font = pygame.font.Font("freesansbold.ttf", 24)
        text = font.render("Reset game", True, WHITE, GREEN)
        self.reset_button = text.get_rect()
        text_offset_x = self.reset_button.width / 2
        text_offset_y = self.reset_button.height / 2
        self.screen.blit(
            text,
            (
                (WINDOW_WIDTH - BOARD_OFFSET - BOARD_SIZE) / 2
                + BOARD_OFFSET
                + BOARD_SIZE
                - text_offset_x,
                WINDOW_HEIGHT * 3 / 4 - text_offset_y,
            ),
        )

    def draw_player_message(self):
        if self.chess_game.is_finished():
            winner = self.chess_game.get_winner()
            if winner is None:
                player_text = "The game has been drawn."
            else:
                is_winner_white = winner == self.chess_game.get_white()
                player_text = f"{'White' if is_winner_white else 'Black'} has won the game."
        else:
            is_current_player_white = (
                self.chess_game.get_current_player()
                == self.chess_game.get_white()
            )
            player_text = (
                f"{'White' if is_current_player_white else 'Black'} to move."
            )
        font = pygame.font.Font("freesansbold.ttf", 24)
        text = font.render(player_text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_offset_x = text_rect.width / 2
        text_offset_y = text_rect.height / 2
        self.screen.blit(
            text,
            (
                (WINDOW_WIDTH - BOARD_OFFSET - BOARD_SIZE) / 2
                + BOARD_OFFSET
                + BOARD_SIZE
                - text_offset_x,
                WINDOW_HEIGHT / 4 - text_offset_y,
            ),
        )


def set_icon(pathname: str):
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


def draw_player_message(screen: pygame.Surface, chess_game: ChessGame):
    if chess_game.is_finished():
        winner = chess_game.get_winner()
        if winner is None:
            player_text = "The game has been drawn."
        else:
            is_winner_white = winner == chess_game.get_white()
            player_text = (
                f"{'White' if is_winner_white else 'Black'} has won the game."
            )
    else:
        is_current_player_white = (
            chess_game.get_current_player() == chess_game.get_white()
        )
        player_text = (
            f"{'White' if is_current_player_white else 'Black'} to move."
        )
    font = pygame.font.Font("freesansbold.ttf", 24)
    text = font.render(player_text, True, (0, 0, 0))
    text_rect = text.get_rect()
    text_offset_x = text_rect.width / 2
    text_offset_y = text_rect.height / 2
    screen.blit(
        text,
        (
            (WINDOW_WIDTH - BOARD_OFFSET - BOARD_SIZE) / 2
            + BOARD_OFFSET
            + BOARD_SIZE
            - text_offset_x,
            WINDOW_HEIGHT / 4 - text_offset_y,
        ),
    )


def draw_reset_button(screen: pygame.surface):
    font = pygame.font.Font("freesansbold.ttf", 24)
    text = font.render("Reset game", True, WHITE, GREEN)
    text_rect = text.get_rect()
    text_offset_x = text_rect.width / 2
    text_offset_y = text_rect.height / 2
    screen.blit(
        text,
        (
            (WINDOW_WIDTH - BOARD_OFFSET - BOARD_SIZE) / 2
            + BOARD_OFFSET
            + BOARD_SIZE
            - text_offset_x,
            WINDOW_HEIGHT * 3 / 4 - text_offset_y,
        ),
    )


def draw_move(screen: pygame.surface, chess_game: ChessGame, move: ChessMove):
    end_column, end_row = move.end_column(), move.end_row()
    center = (
        BOARD_OFFSET + EDGE_SIZE + end_column * PIECE_SIZE + PIECE_SIZE / 2,
        BOARD_OFFSET + EDGE_SIZE + (7 - end_row) * PIECE_SIZE + PIECE_SIZE / 2,
    )
    radius = PIECE_SIZE / 4
    pygame.draw.circle(screen, EDGE_COLOR, center, radius)


def draw_everything(
    screen: pygame.surface,
    chess_game: ChessGame,
    moves_list: Iterable[ChessMove],
):
    screen.fill(BACKGROUND_COLOR)

    pygame.draw.rect(
        screen,
        EDGE_COLOR,
        (BOARD_OFFSET, BOARD_OFFSET, BOARD_SIZE, BOARD_SIZE),
    )

    chess_game.draw(
        screen,
        PIECE_SIZE,
        BOARD_OFFSET_CHESS_AREA,
        BOARD_OFFSET_CHESS_AREA,
    )

    if moves_list is not None:
        for move in moves_list:
            draw_move(screen, chess_game, move)

    draw_player_message(screen, chess_game)
    draw_reset_button(screen)


def main():
    pygame.init()
    # pygame.mixer.init()
    # move_sound_path = "sounds/chess_move.wav"
    # move_sound = pygame.mixer.Sound(move_sound_path)
    pygame.display.set_caption("Chess")

    set_icon("chess_icons/white_knight.svg")

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    chess_game = ChessGame()

    move = None
    move_start_column = None
    move_start_row = None
    moves_list = None
    promotion_type = Queen

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # pygame.mixer.Sound.play(move_sound)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                board_column = int(
                    (mouse_x - BOARD_OFFSET - EDGE_SIZE) // PIECE_SIZE
                )
                board_row = int(
                    7 - ((mouse_y - BOARD_OFFSET - EDGE_SIZE) // PIECE_SIZE)
                )
                if board_column in range(8) and board_row in range(8):
                    if chess_game.is_a_current_players_piece(
                        board_column, board_row
                    ):
                        moves_list = chess_game.get_moves(
                            board_column, board_row
                        )
                        if moves_list:
                            move_start_column, move_start_row = (
                                board_column,
                                board_row,
                            )

                    elif (
                        move_start_column is not None
                        and move_start_row is not None
                        and not (
                            board_column == move_start_column
                            and board_row == move_start_row
                        )
                    ):
                        move = ChessMove(
                            move_start_column,
                            move_start_row,
                            board_column,
                            board_row,
                        )
                        move_start_column = None
                        move_start_row = None
                        moves_list = None
                        print("A move has been prepared.")
                    else:
                        move = None
                        move_start_column = None
                        move_start_row = None
                        moves_list = None
                # elif

        if move is not None:
            if chess_game.is_promotion(move):
                continue
            try:
                chess_game.make_move(move, promotion_type)
            except InvalidMoveException:
                pass
            moves_list = None
            move = None
            print(move if move is not None else "None")

        draw_everything(screen, chess_game, moves_list)

        pygame.display.update()


if __name__ == "__main__":
    main()
