from chess_classes import (
    Bishop,
    CoordinatesOutOfBoundsException,
    ChessMove,
    ChessState,
    InvalidMoveException,
    King,
    Knight,
    Pawn,
    Queen,
    Rook,
)
from typing import Iterable
from two_player_games.two_player_games.player import Player
from pytest import raises


def compare_move_tables(
    table_1: Iterable[ChessMove], table_2: Iterable[ChessMove]
) -> bool:
    table_1_copy = list(table_1)
    table_2_copy = list(table_2)
    for move_1 in table_1:
        for move_2 in table_2:
            if move_1 == move_2:
                table_1_copy.remove(move_1)
                table_2_copy.remove(move_2)
                break
    if table_1_copy or table_2_copy:
        return False
    return True


def test_chess_piece_init_in_bounds():
    player_1 = Player("1")
    chess_piece = Pawn(1, 1, player_1)
    assert chess_piece.column() == 1
    assert chess_piece.row() == 1
    assert chess_piece.player() == player_1


def test_chess_piece_init_out_of_bounds():
    player_1 = Player("1")
    with raises(CoordinatesOutOfBoundsException):
        Pawn(-1, 1, player_1)


def test_pawn_moves_no_edge_cases():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn = Pawn(3, 3, player_1, False)
    board = (
        [[None for _ in range(8)] for _ in range(3)]
        + [[pawn if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(4)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
                        \n\
         P1             \n\
                        \n\
                        \n\
                        \n"
    )
    expected_moves = [ChessMove(3, 3, 3, 4)]
    assert compare_move_tables(pawn._get_moves(chess_state), expected_moves)


def test_pawn_moves_next_to_the_edge():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn = Pawn(0, 3, player_1, False)
    board = (
        [[None for _ in range(8)] for _ in range(3)]
        + [[pawn if column == 0 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(4)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
                        \n\
P1                      \n\
                        \n\
                        \n\
                        \n"
    )
    expected_moves = [ChessMove(0, 3, 0, 4)]
    assert compare_move_tables(pawn._get_moves(chess_state), expected_moves)


def test_pawn_moves_first_move():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn = Pawn(3, 1, player_1)
    board = (
        [[None for _ in range(8)]]
        + [[pawn if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(6)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
         P1             \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 1, 3, 2),
        ChessMove(3, 1, 3, 3),
    ]
    assert compare_move_tables(pawn._get_moves(chess_state), expected_moves)


def test_pawn_moves_en_passant():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn_1 = Pawn(3, 4, player_1, False)
    pawn_2 = Pawn(4, 4, player_2, False, True)
    board = (
        [[None for _ in range(8)] for _ in range(4)]
        + [[None, None, None, pawn_1, pawn_2, None, None, None]]
        + [[None for _ in range(8)] for _ in range(3)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
         P1 P2          \n\
                        \n\
                        \n\
                        \n\
                        \n"
    )
    expected_moves = [ChessMove(3, 4, 3, 5), ChessMove(3, 4, 4, 5)]
    assert compare_move_tables(pawn_1._get_moves(chess_state), expected_moves)


def test_pawn_moves_can_take():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn_1 = Pawn(3, 4, player_1, False)
    pawn_2 = Pawn(4, 5, player_2, False)
    board = (
        [[None for _ in range(8)] for _ in range(4)]
        + [[pawn_1 if column == 3 else None for column in range(8)]]
        + [[pawn_2 if column == 4 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(2)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
            P2          \n\
         P1             \n\
                        \n\
                        \n\
                        \n\
                        \n"
    )
    expected_moves = [ChessMove(3, 4, 3, 5), ChessMove(3, 4, 4, 5)]
    assert compare_move_tables(pawn_1._get_moves(chess_state), expected_moves)


def test_pawn_moves_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn_1 = Pawn(3, 3, player_1, False)
    pawn_2 = Pawn(3, 4, player_1, False)
    board = (
        [[None for _ in range(8)] for _ in range(3)]
        + [[pawn_1 if column == 3 else None for column in range(8)]]
        + [[pawn_2 if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(3)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
         P1             \n\
         P1             \n\
                        \n\
                        \n\
                        \n"
    )
    assert not pawn_1._get_moves(chess_state)


def test_pawn_moves_blocked_en_passant():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn_1 = Pawn(3, 3, player_1, False)
    pawn_2 = Pawn(4, 4, player_1, False)
    pawn_3 = Pawn(4, 3, player_2, False)
    board = (
        [[None for _ in range(8)] for _ in range(3)]
        + [[None, None, None, pawn_1, pawn_3, None, None, None]]
        + [[pawn_2 if column == 4 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(3)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
            P1          \n\
         P1 P2          \n\
                        \n\
                        \n\
                        \n"
    )
    expected_moves = [ChessMove(3, 3, 3, 4)]
    assert compare_move_tables(pawn_1._get_moves(chess_state), expected_moves)


def test_knight_moves_no_edge_cases():
    player_1 = Player("1")
    player_2 = Player("2")
    knight = Knight(3, 4, player_1)
    board = (
        [[None for _ in range(8)] for _ in range(4)]
        + [[knight if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(3)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
         N1             \n\
                        \n\
                        \n\
                        \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 4, 2, 2),
        ChessMove(3, 4, 1, 3),
        ChessMove(3, 4, 1, 5),
        ChessMove(3, 4, 2, 6),
        ChessMove(3, 4, 4, 6),
        ChessMove(3, 4, 5, 5),
        ChessMove(3, 4, 5, 3),
        ChessMove(3, 4, 4, 2),
    ]
    assert compare_move_tables(knight._get_moves(chess_state), expected_moves)


def test_knight_moves_corner():
    player_1 = Player("1")
    player_2 = Player("2")
    knight = Knight(0, 0, player_1)
    board = [[knight] + [None for _ in range(7)]] + [
        [None for _ in range(8)] for _ in range(7)
    ]
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
N1                      \n"
    )
    expected_moves = [
        ChessMove(0, 0, 2, 1),
        ChessMove(0, 0, 1, 2),
    ]
    assert compare_move_tables(knight._get_moves(chess_state), expected_moves)


def test_knight_moves_can_take():
    player_1 = Player("1")
    player_2 = Player("2")
    knight_1 = Knight(3, 4, player_1)
    knight_2 = Knight(2, 6, player_2)
    board = (
        [[None for _ in range(8)] for _ in range(4)]
        + [[knight_1 if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)]]
        + [[knight_2 if column == 2 else None for column in range(8)]]
        + [[None for _ in range(8)]]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
      N2                \n\
                        \n\
         N1             \n\
                        \n\
                        \n\
                        \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 4, 2, 2),
        ChessMove(3, 4, 1, 3),
        ChessMove(3, 4, 1, 5),
        ChessMove(3, 4, 2, 6),
        ChessMove(3, 4, 4, 6),
        ChessMove(3, 4, 5, 5),
        ChessMove(3, 4, 5, 3),
        ChessMove(3, 4, 4, 2),
    ]
    assert compare_move_tables(
        knight_1._get_moves(chess_state), expected_moves
    )


def test_knight_moves_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    knight_1 = Knight(3, 4, player_1)
    knight_2 = Knight(2, 6, player_1)
    board = (
        [[None for _ in range(8)] for _ in range(4)]
        + [[knight_1 if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)]]
        + [[knight_2 if column == 2 else None for column in range(8)]]
        + [[None for _ in range(8)]]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
      N1                \n\
                        \n\
         N1             \n\
                        \n\
                        \n\
                        \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 4, 2, 2),
        ChessMove(3, 4, 1, 3),
        ChessMove(3, 4, 1, 5),
        ChessMove(3, 4, 4, 6),
        ChessMove(3, 4, 5, 5),
        ChessMove(3, 4, 5, 3),
        ChessMove(3, 4, 4, 2),
    ]
    assert compare_move_tables(
        knight_1._get_moves(chess_state), expected_moves
    )


def test_bishop_moves_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    bishop_1 = Bishop(3, 3, player_1)
    bishop_2 = Bishop(1, 1, player_1)
    bishop_3 = Bishop(5, 5, player_1)
    bishop_4 = Bishop(1, 5, player_1)
    bishop_5 = Bishop(5, 1, player_1)
    board = (
        [[None for _ in range(8)]]
        + [[None, bishop_2, None, None, None, bishop_5, None, None]]
        + [[None for _ in range(8)]]
        + [[bishop_1 if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)]]
        + [[None, bishop_4, None, None, None, bishop_3, None, None]]
        + [[None for _ in range(8)] for _ in range(2)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
   B1          B1       \n\
                        \n\
         B1             \n\
                        \n\
   B1          B1       \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 3, 2, 2),
        ChessMove(3, 3, 4, 4),
        ChessMove(3, 3, 2, 4),
        ChessMove(3, 3, 4, 2),
    ]
    assert compare_move_tables(
        bishop_1._get_moves(chess_state), expected_moves
    )


def test_bishop_moves_can_take():
    player_1 = Player("1")
    player_2 = Player("2")
    bishop_1 = Bishop(3, 3, player_1)
    bishop_2 = Bishop(1, 1, player_2)
    bishop_3 = Bishop(5, 5, player_2)
    bishop_4 = Bishop(1, 5, player_2)
    bishop_5 = Bishop(5, 1, player_2)
    board = (
        [[None for _ in range(8)]]
        + [[None, bishop_2, None, None, None, bishop_5, None, None]]
        + [[None for _ in range(8)]]
        + [[bishop_1 if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)]]
        + [[None, bishop_4, None, None, None, bishop_3, None, None]]
        + [[None for _ in range(8)] for _ in range(2)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
   B2          B2       \n\
                        \n\
         B1             \n\
                        \n\
   B2          B2       \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 3, 2, 2),
        ChessMove(3, 3, 4, 4),
        ChessMove(3, 3, 2, 4),
        ChessMove(3, 3, 4, 2),
        ChessMove(3, 3, 1, 1),
        ChessMove(3, 3, 5, 5),
        ChessMove(3, 3, 1, 5),
        ChessMove(3, 3, 5, 1),
    ]
    assert compare_move_tables(
        bishop_1._get_moves(chess_state), expected_moves
    )


def test_bishop_moves_no_edge_cases():
    player_1 = Player("1")
    player_2 = Player("2")
    bishop = Bishop(3, 3, player_1)
    board = (
        [[None for _ in range(8)] for _ in range(3)]
        + [[bishop if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(4)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
                        \n\
         B1             \n\
                        \n\
                        \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 3, 0, 0),
        ChessMove(3, 3, 1, 1),
        ChessMove(3, 3, 2, 2),
        ChessMove(3, 3, 4, 4),
        ChessMove(3, 3, 5, 5),
        ChessMove(3, 3, 6, 6),
        ChessMove(3, 3, 7, 7),
        ChessMove(3, 3, 0, 6),
        ChessMove(3, 3, 1, 5),
        ChessMove(3, 3, 2, 4),
        ChessMove(3, 3, 4, 2),
        ChessMove(3, 3, 5, 1),
        ChessMove(3, 3, 6, 0),
    ]
    assert compare_move_tables(bishop._get_moves(chess_state), expected_moves)


def test_rook_moves_no_edge_cases():
    player_1 = Player("1")
    player_2 = Player("2")
    rook = Rook(3, 3, player_1)
    board = (
        [[None for _ in range(8)] for _ in range(3)]
        + [[rook if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(4)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
                        \n\
         R1             \n\
                        \n\
                        \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 3, 0, 3),
        ChessMove(3, 3, 1, 3),
        ChessMove(3, 3, 2, 3),
        ChessMove(3, 3, 4, 3),
        ChessMove(3, 3, 5, 3),
        ChessMove(3, 3, 6, 3),
        ChessMove(3, 3, 7, 3),
        ChessMove(3, 3, 3, 7),
        ChessMove(3, 3, 3, 6),
        ChessMove(3, 3, 3, 5),
        ChessMove(3, 3, 3, 4),
        ChessMove(3, 3, 3, 2),
        ChessMove(3, 3, 3, 1),
        ChessMove(3, 3, 3, 0),
    ]
    assert compare_move_tables(rook._get_moves(chess_state), expected_moves)


def test_rook_moves_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    rook_1 = Rook(3, 3, player_1)
    rook_2 = Rook(3, 1, player_1)
    rook_3 = Rook(1, 3, player_1)
    rook_4 = Rook(5, 3, player_1)
    rook_5 = Rook(3, 5, player_1)
    board = (
        [[None for _ in range(8)]]
        + [[rook_2 if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)]]
        + [[None, rook_3, None, rook_1, None, rook_4, None, None]]
        + [[None for _ in range(8)]]
        + [[rook_5 if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(2)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
         R1             \n\
                        \n\
   R1    R1    R1       \n\
                        \n\
         R1             \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 3, 2, 3),
        ChessMove(3, 3, 4, 3),
        ChessMove(3, 3, 3, 4),
        ChessMove(3, 3, 3, 2),
    ]
    assert compare_move_tables(rook_1._get_moves(chess_state), expected_moves)


def test_rook_moves_can_take():
    player_1 = Player("1")
    player_2 = Player("2")
    rook_1 = Rook(3, 3, player_1)
    rook_2 = Rook(3, 1, player_2)
    rook_3 = Rook(1, 3, player_2)
    rook_4 = Rook(5, 3, player_2)
    rook_5 = Rook(3, 5, player_2)
    board = (
        [[None for _ in range(8)]]
        + [[rook_2 if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)]]
        + [[None, rook_3, None, rook_1, None, rook_4, None, None]]
        + [[None for _ in range(8)]]
        + [[rook_5 if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(2)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
         R2             \n\
                        \n\
   R2    R1    R2       \n\
                        \n\
         R2             \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 3, 2, 3),
        ChessMove(3, 3, 4, 3),
        ChessMove(3, 3, 3, 4),
        ChessMove(3, 3, 3, 2),
        ChessMove(3, 3, 1, 3),
        ChessMove(3, 3, 5, 3),
        ChessMove(3, 3, 3, 5),
        ChessMove(3, 3, 3, 1),
    ]
    assert compare_move_tables(rook_1._get_moves(chess_state), expected_moves)


def test_queen_moves_no_edge_cases():
    player_1 = Player("1")
    player_2 = Player("2")
    queen = Queen(3, 3, player_1)
    board = (
        [[None for _ in range(8)] for _ in range(3)]
        + [[queen if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(4)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
                        \n\
         Q1             \n\
                        \n\
                        \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 3, 0, 3),
        ChessMove(3, 3, 1, 3),
        ChessMove(3, 3, 2, 3),
        ChessMove(3, 3, 4, 3),
        ChessMove(3, 3, 5, 3),
        ChessMove(3, 3, 6, 3),
        ChessMove(3, 3, 7, 3),
        ChessMove(3, 3, 3, 7),
        ChessMove(3, 3, 3, 6),
        ChessMove(3, 3, 3, 5),
        ChessMove(3, 3, 3, 4),
        ChessMove(3, 3, 3, 2),
        ChessMove(3, 3, 3, 1),
        ChessMove(3, 3, 3, 0),
        ChessMove(3, 3, 0, 0),
        ChessMove(3, 3, 1, 1),
        ChessMove(3, 3, 2, 2),
        ChessMove(3, 3, 4, 4),
        ChessMove(3, 3, 5, 5),
        ChessMove(3, 3, 6, 6),
        ChessMove(3, 3, 7, 7),
        ChessMove(3, 3, 0, 6),
        ChessMove(3, 3, 1, 5),
        ChessMove(3, 3, 2, 4),
        ChessMove(3, 3, 4, 2),
        ChessMove(3, 3, 5, 1),
        ChessMove(3, 3, 6, 0),
    ]
    assert compare_move_tables(queen._get_moves(chess_state), expected_moves)


def test_queen_moves_can_take():
    player_1 = Player("1")
    player_2 = Player("2")
    queen = Queen(3, 3, player_1)
    pawn_1 = Pawn(2, 2, player_2, False)
    pawn_2 = Pawn(3, 2, player_2, False)
    pawn_3 = Pawn(4, 2, player_2, False)
    pawn_4 = Pawn(2, 3, player_2, False)
    pawn_5 = Pawn(2, 4, player_2, False)
    board = (
        [[None for _ in range(8)] for _ in range(2)]
        + [[None, None, pawn_1, pawn_2, pawn_3, None, None, None]]
        + [[None, None, pawn_4, queen, None, None, None, None]]
        + [[pawn_5 if column == 2 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(3)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
      P2                \n\
      P2 Q1             \n\
      P2 P2 P2          \n\
                        \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 3, 2, 3),
        ChessMove(3, 3, 4, 3),
        ChessMove(3, 3, 3, 4),
        ChessMove(3, 3, 3, 2),
        ChessMove(3, 3, 2, 2),
        ChessMove(3, 3, 4, 4),
        ChessMove(3, 3, 2, 4),
        ChessMove(3, 3, 4, 2),
        ChessMove(3, 3, 3, 5),
        ChessMove(3, 3, 3, 6),
        ChessMove(3, 3, 3, 7),
        ChessMove(3, 3, 5, 5),
        ChessMove(3, 3, 6, 6),
        ChessMove(3, 3, 7, 7),
        ChessMove(3, 3, 5, 3),
        ChessMove(3, 3, 6, 3),
        ChessMove(3, 3, 7, 3),
    ]
    assert compare_move_tables(queen._get_moves(chess_state), expected_moves)


def test_queen_moves_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    queen = Queen(3, 3, player_1)
    pawn_1 = Pawn(2, 2, player_1, False)
    pawn_2 = Pawn(3, 2, player_1, False)
    pawn_3 = Pawn(4, 2, player_1, False)
    pawn_4 = Pawn(2, 3, player_1, False)
    pawn_5 = Pawn(2, 4, player_1, False)
    board = (
        [[None for _ in range(8)] for _ in range(2)]
        + [[None, None, pawn_1, pawn_2, pawn_3, None, None, None]]
        + [[None, None, pawn_4, queen, None, None, None, None]]
        + [[pawn_5 if column == 2 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(3)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
      P1                \n\
      P1 Q1             \n\
      P1 P1 P1          \n\
                        \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 3, 4, 3),
        ChessMove(3, 3, 3, 4),
        ChessMove(3, 3, 4, 4),
        ChessMove(3, 3, 3, 5),
        ChessMove(3, 3, 3, 6),
        ChessMove(3, 3, 3, 7),
        ChessMove(3, 3, 5, 5),
        ChessMove(3, 3, 6, 6),
        ChessMove(3, 3, 7, 7),
        ChessMove(3, 3, 5, 3),
        ChessMove(3, 3, 6, 3),
        ChessMove(3, 3, 7, 3),
    ]
    assert compare_move_tables(queen._get_moves(chess_state), expected_moves)


def test_king_moves_no_edge_cases():
    player_1 = Player("1")
    player_2 = Player("2")
    king = King(3, 3, player_1, False)
    board = (
        [[None for _ in range(8)] for _ in range(3)]
        + [[king if column == 3 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(4)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
                        \n\
         K1             \n\
                        \n\
                        \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 3, 2, 3),
        ChessMove(3, 3, 4, 3),
        ChessMove(3, 3, 3, 4),
        ChessMove(3, 3, 3, 2),
        ChessMove(3, 3, 2, 2),
        ChessMove(3, 3, 4, 4),
        ChessMove(3, 3, 2, 4),
        ChessMove(3, 3, 4, 2),
    ]
    assert compare_move_tables(king._get_moves(chess_state), expected_moves)


def test_king_moves_can_take():
    player_1 = Player("1")
    player_2 = Player("2")
    king = King(3, 3, player_1, False)
    pawn_1 = Pawn(2, 2, player_2, False)
    pawn_2 = Pawn(3, 2, player_2, False)
    pawn_3 = Pawn(4, 2, player_2, False)
    pawn_4 = Pawn(2, 3, player_2, False)
    pawn_5 = Pawn(2, 4, player_2, False)
    board = (
        [[None for _ in range(8)] for _ in range(2)]
        + [[None, None, pawn_1, pawn_2, pawn_3, None, None, None]]
        + [[None, None, pawn_4, king, None, None, None, None]]
        + [[pawn_5 if column == 2 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(3)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
      P2                \n\
      P2 K1             \n\
      P2 P2 P2          \n\
                        \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 3, 2, 3),
        ChessMove(3, 3, 4, 3),
        ChessMove(3, 3, 3, 4),
        ChessMove(3, 3, 3, 2),
        ChessMove(3, 3, 2, 2),
        ChessMove(3, 3, 4, 4),
        ChessMove(3, 3, 2, 4),
        ChessMove(3, 3, 4, 2),
    ]
    assert compare_move_tables(king._get_moves(chess_state), expected_moves)


def test_king_moves_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    king = King(3, 3, player_1, False)
    pawn_1 = Pawn(2, 2, player_1, False)
    pawn_2 = Pawn(3, 2, player_1, False)
    pawn_3 = Pawn(4, 2, player_1, False)
    pawn_4 = Pawn(2, 3, player_1, False)
    pawn_5 = Pawn(2, 4, player_1, False)
    board = (
        [[None for _ in range(8)] for _ in range(2)]
        + [[None, None, pawn_1, pawn_2, pawn_3, None, None, None]]
        + [[None, None, pawn_4, king, None, None, None, None]]
        + [[pawn_5 if column == 2 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(3)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
      P1                \n\
      P1 K1             \n\
      P1 P1 P1          \n\
                        \n\
                        \n"
    )
    expected_moves = [
        ChessMove(3, 3, 4, 3),
        ChessMove(3, 3, 3, 4),
        ChessMove(3, 3, 4, 4),
    ]
    assert compare_move_tables(king._get_moves(chess_state), expected_moves)


def test_king_moves_can_castle():
    player_1 = Player("1")
    player_2 = Player("2")
    king = King(4, 0, player_1)
    rook_1 = Rook(0, 0, player_1)
    rook_2 = Rook(7, 0, player_1)
    board = [[rook_1, None, None, None, king, None, None, rook_2]] + [
        [None for _ in range(8)] for _ in range(7)
    ]
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
R1          K1       R1 \n"
    )
    expected_moves = [
        ChessMove(4, 0, 3, 0),
        ChessMove(4, 0, 3, 1),
        ChessMove(4, 0, 4, 1),
        ChessMove(4, 0, 5, 1),
        ChessMove(4, 0, 5, 0),
        ChessMove(4, 0, 2, 0),
        ChessMove(4, 0, 6, 0),
    ]
    assert compare_move_tables(king._get_moves(chess_state), expected_moves)


def test_king_moves_cant_castle_king_moved():
    player_1 = Player("1")
    player_2 = Player("2")
    king = King(4, 0, player_1, False)
    rook_1 = Rook(0, 0, player_1)
    rook_2 = Rook(7, 0, player_1)
    board = [[rook_1, None, None, None, king, None, None, rook_2]] + [
        [None for _ in range(8)] for _ in range(7)
    ]
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
R1          K1       R1 \n"
    )
    expected_moves = [
        ChessMove(4, 0, 3, 0),
        ChessMove(4, 0, 3, 1),
        ChessMove(4, 0, 4, 1),
        ChessMove(4, 0, 5, 1),
        ChessMove(4, 0, 5, 0),
    ]
    assert compare_move_tables(king._get_moves(chess_state), expected_moves)


def test_king_moves_cant_castle_rooks_moved():
    player_1 = Player("1")
    player_2 = Player("2")
    king = King(4, 0, player_1)
    rook_1 = Rook(0, 0, player_1, False)
    rook_2 = Rook(7, 0, player_1, False)
    board = [[rook_1, None, None, None, king, None, None, rook_2]] + [
        [None for _ in range(8)] for _ in range(7)
    ]
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert (
        str(chess_state)
        == "\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
R1          K1       R1 \n"
    )
    expected_moves = [
        ChessMove(4, 0, 3, 0),
        ChessMove(4, 0, 3, 1),
        ChessMove(4, 0, 4, 1),
        ChessMove(4, 0, 5, 1),
        ChessMove(4, 0, 5, 0),
    ]
    assert compare_move_tables(king._get_moves(chess_state), expected_moves)


def test_chess_state_init_empty():
    player_1 = Player("1")
    player_2 = Player("2")
    chess_state = ChessState(player_1, player_2)
    assert (
        str(chess_state)
        == "\
R2 N2 B2 Q2 K2 B2 N2 R2 \n\
P2 P2 P2 P2 P2 P2 P2 P2 \n\
                        \n\
                        \n\
                        \n\
                        \n\
P1 P1 P1 P1 P1 P1 P1 P1 \n\
R1 N1 B1 Q1 K1 B1 N1 R1 \n"
    )


def test_get_moves_init_empty():
    player_1 = Player("1")
    player_2 = Player("2")
    chess_state = ChessState(player_1, player_2)
    expected_moves = [
        ChessMove(0, 1, 0, 2),
        ChessMove(0, 1, 0, 3),
        ChessMove(1, 1, 1, 2),
        ChessMove(1, 1, 1, 3),
        ChessMove(2, 1, 2, 2),
        ChessMove(2, 1, 2, 3),
        ChessMove(3, 1, 3, 2),
        ChessMove(3, 1, 3, 3),
        ChessMove(4, 1, 4, 2),
        ChessMove(4, 1, 4, 3),
        ChessMove(5, 1, 5, 2),
        ChessMove(5, 1, 5, 3),
        ChessMove(6, 1, 6, 2),
        ChessMove(6, 1, 6, 3),
        ChessMove(7, 1, 7, 2),
        ChessMove(7, 1, 7, 3),
        ChessMove(1, 0, 0, 2),
        ChessMove(1, 0, 2, 2),
        ChessMove(6, 0, 5, 2),
        ChessMove(6, 0, 7, 2),
    ]
    assert compare_move_tables(chess_state.get_moves(), expected_moves)


def test_get_moves_init_empty_black_move():
    player_1 = Player("1")
    player_2 = Player("2")
    chess_state = ChessState(player_2, player_1, player_1)
    expected_moves = [
        ChessMove(0, 6, 0, 5),
        ChessMove(0, 6, 0, 4),
        ChessMove(1, 6, 1, 5),
        ChessMove(1, 6, 1, 4),
        ChessMove(2, 6, 2, 5),
        ChessMove(2, 6, 2, 4),
        ChessMove(3, 6, 3, 5),
        ChessMove(3, 6, 3, 4),
        ChessMove(4, 6, 4, 5),
        ChessMove(4, 6, 4, 4),
        ChessMove(5, 6, 5, 5),
        ChessMove(5, 6, 5, 4),
        ChessMove(6, 6, 6, 5),
        ChessMove(6, 6, 6, 4),
        ChessMove(7, 6, 7, 5),
        ChessMove(7, 6, 7, 4),
        ChessMove(1, 7, 0, 5),
        ChessMove(1, 7, 2, 5),
        ChessMove(6, 7, 5, 5),
        ChessMove(6, 7, 7, 5),
    ]
    assert compare_move_tables(chess_state.get_moves(), expected_moves)


def test_make_move_init_empty():
    player_1 = Player("1")
    player_2 = Player("2")
    chess_state = ChessState(player_1, player_2)
    move = ChessMove(4, 1, 4, 3)
    new_state = chess_state.make_move(move)
    assert (
        str(new_state)
        == "\
R2 N2 B2 Q2 K2 B2 N2 R2 \n\
P2 P2 P2 P2 P2 P2 P2 P2 \n\
                        \n\
                        \n\
            P1          \n\
                        \n\
P1 P1 P1 P1    P1 P1 P1 \n\
R1 N1 B1 Q1 K1 B1 N1 R1 \n"
    )


def test_make_move_take():
    player_1 = Player("1")
    player_2 = Player("2")
    board = (
        [
            [
                King(0, 0, player_1, False),
                None,
                None,
                None,
                None,
                None,
                None,
                Rook(7, 0, player_1, False),
            ]
        ]
        + [[None for _ in range(8)] for _ in range(6)]
        + [
            [
                King(0, 7, player_2, False),
                None,
                None,
                None,
                None,
                None,
                None,
                Rook(7, 7, player_2, False),
            ]
        ]
    )
    state = ChessState(player_1, player_2, player_1, board)
    move = ChessMove(7, 0, 7, 7)
    new_state = state.make_move(move)
    assert (
        str(new_state)
        == "\
K2                   R1 \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
K1                      \n"
    )


def test_make_move_en_passant():
    player_1 = Player("1")
    player_2 = Player("2")
    board = (
        [
            [
                King(0, 0, player_1, False) if column == 0 else None
                for column in range(8)
            ]
        ]
        + [[None for _ in range(8)] for _ in range(3)]
        + [
            [
                None,
                None,
                None,
                Pawn(3, 4, player_2, False, True),
                Pawn(4, 4, player_1, False, False),
                None,
                None,
                None,
            ]
        ]
        + [[None for _ in range(8)] for _ in range(2)]
        + [
            [
                King(0, 7, player_2, False) if column == 0 else None
                for column in range(8)
            ]
        ]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    move = ChessMove(4, 4, 3, 5)
    new_state = chess_state.make_move(move)
    assert (
        str(new_state)
        == "\
K2                      \n\
                        \n\
         P1             \n\
                        \n\
                        \n\
                        \n\
                        \n\
K1                      \n"
    )


def test_make_move_pawn_promotion():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn = Pawn(3, 6, player_1, False)
    king_w = King(0, 0, player_1, False)
    king_b = King(0, 7, player_2, False)
    board = (
        [[king_w if column == 0 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(5)]
        + [[pawn if column == 3 else None for column in range(8)]]
        + [[king_b if column == 0 else None for column in range(8)]]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    move = ChessMove(3, 6, 3, 7)
    assert chess_state.is_promotion(move)
    new_state = chess_state.make_move(move, Queen)
    assert (
        str(new_state)
        == "\
K2       Q1             \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
K1                      \n"
    )


def test_make_move_pawn_promotion_cant_move_check():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn = Pawn(3, 6, player_1, False)
    king_w = King(0, 0, player_1, False)
    king_b = King(0, 7, player_2, False)
    rook_b = Rook(0, 1, player_2, False)
    board = (
        [[king_w if column == 0 else None for column in range(8)]]
        + [[rook_b if column == 0 else None for column in range(8)]]
        + [[None for _ in range(8)] for _ in range(4)]
        + [[pawn if column == 3 else None for column in range(8)]]
        + [[king_b if column == 0 else None for column in range(8)]]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    move = ChessMove(3, 6, 3, 7)
    assert chess_state.is_promotion(move)
    with raises(InvalidMoveException):
        chess_state.make_move(move, Queen)


def test_make_move_cant_castle_under_check():
    player_1 = Player("1")
    player_2 = Player("2")
    board = (
        [
            [
                None,
                None,
                None,
                None,
                King(4, 0, player_1),
                None,
                None,
                Rook(7, 0, player_1),
            ]
        ]
        + [[None for _ in range(8)] for _ in range(6)]
        + [
            [
                None,
                None,
                None,
                None,
                Rook(4, 7, player_2),
                None,
                None,
                King(7, 7, player_2),
            ]
        ]
    )
    state = ChessState(player_1, player_2, player_1, board)
    move = ChessMove(4, 0, 6, 0)
    with raises(InvalidMoveException):
        state.make_move(move)


def test_make_move_castles_queenside():
    player_1 = Player("1")
    player_2 = Player("2")
    board = (
        [
            [
                Rook(0, 0, player_1),
                None,
                None,
                None,
                King(4, 0, player_1),
                None,
                None,
                None,
            ]
        ]
        + [[None for _ in range(8)] for _ in range(6)]
        + [
            [
                Rook(0, 7, player_2),
                None,
                None,
                None,
                King(4, 7, player_2),
                None,
                None,
                None,
            ]
        ]
    )
    state = ChessState(player_1, player_2, player_1, board)
    move = ChessMove(4, 0, 2, 0)
    new_state = state.make_move(move)
    assert (
        str(new_state)
        == "\
R2          K2          \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
      K1 R1             \n"
    )


def test_make_move_castles():
    player_1 = Player("1")
    player_2 = Player("2")
    board = (
        [
            [
                None,
                None,
                None,
                None,
                King(4, 0, player_1),
                None,
                None,
                Rook(7, 0, player_1),
            ]
        ]
        + [[None for _ in range(8)] for _ in range(6)]
        + [
            [
                None,
                None,
                None,
                None,
                King(4, 7, player_2),
                None,
                None,
                Rook(7, 7, player_2),
            ]
        ]
    )
    state = ChessState(player_1, player_2, player_1, board)
    move = ChessMove(4, 0, 6, 0)
    new_state = state.make_move(move)
    assert (
        str(new_state)
        == "\
            K2       R2 \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
                        \n\
               R1 K1    \n"
    )


def test_make_move_cant_castle_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    board = (
        [
            [
                None,
                None,
                None,
                None,
                King(4, 0, player_1),
                None,
                Knight(6, 0, player_1),
                Rook(7, 0, player_1),
            ]
        ]
        + [[None for _ in range(8)] for _ in range(6)]
        + [
            [
                None,
                None,
                None,
                None,
                Rook(4, 7, player_2),
                None,
                None,
                King(7, 7, player_2),
            ]
        ]
    )
    state = ChessState(player_1, player_2, player_1, board)
    move = ChessMove(4, 0, 6, 0)
    with raises(InvalidMoveException):
        state.make_move(move)


def test_make_move_cant_castle_queenside_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    board = (
        [
            [
                Rook(0, 0, player_1),
                Knight(1, 0, player_1),
                None,
                None,
                King(4, 0, player_1),
                None,
                None,
                None,
            ]
        ]
        + [[None for _ in range(8)] for _ in range(6)]
        + [
            [
                Rook(0, 7, player_2),
                None,
                None,
                None,
                King(4, 7, player_2),
                None,
                None,
                None,
            ]
        ]
    )
    state = ChessState(player_1, player_2, player_1, board)
    move = ChessMove(4, 0, 2, 0)
    with raises(InvalidMoveException):
        state.make_move(move)


def test_make_move_cant_castle_queenside_under_check():
    player_1 = Player("1")
    player_2 = Player("2")
    board = (
        [
            [
                Rook(0, 0, player_1),
                None,
                None,
                None,
                King(4, 0, player_1),
                None,
                None,
                None,
            ]
        ]
        + [[None for _ in range(8)] for _ in range(6)]
        + [
            [
                King(0, 7, player_2),
                None,
                None,
                None,
                Rook(4, 7, player_2),
                None,
                None,
                None,
            ]
        ]
    )
    state = ChessState(player_1, player_2, player_1, board)
    move = ChessMove(4, 0, 2, 0)
    with raises(InvalidMoveException):
        state.make_move(move)


def test_is_promotion():
    player_1 = Player("1")
    player_2 = Player("2")
    board = (
        [[None for _ in range(8)] for _ in range(5)]
        + [
            [
                Pawn(column, 5, player_1, False, False)
                if not (column // 4)
                else None
                for column in range(8)
            ]
        ]
        + [
            [
                Pawn(column, 6, player_1, False, False)
                if column // 4
                else None
                for column in range(8)
            ]
        ]
        + [[None for _ in range(8)]]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert all(
        not chess_state.is_promotion(ChessMove(column, 5, column, 6))
        for column in range(4)
    )
    assert all(
        chess_state.is_promotion(ChessMove(column, 6, column, 7))
        for column in range(4, 8)
    )


def test_is_finished_init_empty():
    player_1 = Player("1")
    player_2 = Player("2")
    chess_state = ChessState(player_1, player_2)
    assert not chess_state.is_finished()


def test_is_finished_true():
    player_1 = Player("1")
    player_2 = Player("2")
    board = (
        [
            [
                None,
                None,
                None,
                None,
                King(4, 0, player_1),
                None,
                None,
                None,
            ]
        ]
        + [
            [
                None,
                None,
                None,
                None,
                Pawn(4, 1, player_2, False),
                None,
                None,
                None,
            ]
        ]
        + [
            [
                None,
                None,
                None,
                None,
                King(4, 2, player_2),
                None,
                None,
                None,
            ]
        ]
        + [[None for _ in range(8)] for _ in range(6)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert chess_state.is_finished()


def test_get_winner_init_empty():
    player_1 = Player("1")
    player_2 = Player("2")
    chess_state = ChessState(player_1, player_2)
    assert chess_state.get_winner() is None


def test_get_winner_draw():
    player_1 = Player("1")
    player_2 = Player("2")
    board = (
        [
            [
                None,
                None,
                None,
                None,
                King(4, 0, player_1),
                None,
                None,
                None,
            ]
        ]
        + [
            [
                None,
                None,
                None,
                None,
                Pawn(4, 1, player_2, False),
                None,
                None,
                None,
            ]
        ]
        + [
            [
                None,
                None,
                None,
                None,
                King(4, 2, player_2),
                None,
                None,
                None,
            ]
        ]
        + [[None for _ in range(8)] for _ in range(6)]
    )
    chess_state = ChessState(player_1, player_2, player_1, board)
    assert chess_state.get_winner() is None
