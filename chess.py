import pygame
from chess_game_interface.chess_app import ChessApp


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
