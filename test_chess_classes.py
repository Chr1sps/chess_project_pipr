from chess_classes import (
    PAWN,
    KNIGHT,
    BISHOP,
    ROOK,
    QUEEN,
    KING,
    CoordinatesOutOfBoundsException,
    IncorrectPieceTypeException,
    ChessPiece,
    ChessMove,
    ChessState,
)
from typing import Iterable
from two_player_games.player import Player
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
    chess_piece = ChessPiece(PAWN, 1, 1, player_1)
    assert chess_piece.column() == 1
    assert chess_piece.row() == 1
    assert chess_piece.player() == player_1
    assert chess_piece.type() == PAWN


def test_chess_piece_init_out_of_bounds():
    with raises(CoordinatesOutOfBoundsException):
        player_1 = Player("1")
        chess_piece = ChessPiece(PAWN, -1, 1, player_1)


def test_chess_piece_incorrect_type():
    with raises(IncorrectPieceTypeException):
        player_1 = Player("1")
        chess_piece = ChessPiece(-1, 1, 1, player_1)


def test_pawn_moves_no_edge_cases():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn = ChessPiece(PAWN, 3, 3, player_1, False)
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
    expected_moves = [ChessMove(PAWN, 3, 3, 3, 4)]
    assert chess_state._get_moves_pawn(pawn) == expected_moves


def test_pawn_moves_next_to_the_edge():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn = ChessPiece(PAWN, 0, 3, player_1, False)
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
    expected_moves = [ChessMove(PAWN, 0, 3, 0, 4)]
    assert chess_state._get_moves_pawn(pawn) == expected_moves


def test_pawn_moves_first_move():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn = ChessPiece(PAWN, 3, 1, player_1)
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
        ChessMove(PAWN, 3, 1, 3, 2),
        ChessMove(PAWN, 3, 1, 3, 3),
    ]
    assert chess_state._get_moves_pawn(pawn) == expected_moves


def test_pawn_moves_en_passant():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn_1 = ChessPiece(PAWN, 3, 4, player_1, False)
    pawn_2 = ChessPiece(PAWN, 4, 4, player_2, False, True)
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
    expected_moves = [ChessMove(PAWN, 3, 4, 3, 5), ChessMove(PAWN, 3, 4, 4, 5)]
    assert chess_state._get_moves_pawn(pawn_1) == expected_moves


def test_pawn_moves_can_take():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn_1 = ChessPiece(PAWN, 3, 4, player_1, False)
    pawn_2 = ChessPiece(PAWN, 4, 5, player_2, False)
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
    expected_moves = [ChessMove(PAWN, 3, 4, 3, 5), ChessMove(PAWN, 3, 4, 4, 5)]
    assert chess_state._get_moves_pawn(pawn_1) == expected_moves


def test_pawn_moves_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn_1 = ChessPiece(PAWN, 3, 3, player_1, False)
    pawn_2 = ChessPiece(PAWN, 3, 4, player_1, False)
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
    assert not chess_state._get_moves_pawn(pawn_1)


def test_pawn_moves_blocked_en_passant():
    player_1 = Player("1")
    player_2 = Player("2")
    pawn_1 = ChessPiece(PAWN, 3, 3, player_1, False)
    pawn_2 = ChessPiece(PAWN, 4, 4, player_1, False)
    pawn_3 = ChessPiece(PAWN, 4, 3, player_2, False)
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
    expected_moves = [ChessMove(PAWN, 3, 3, 3, 4)]
    assert chess_state._get_moves_pawn(pawn_1) == expected_moves


def test_knight_moves_no_edge_cases():
    player_1 = Player("1")
    player_2 = Player("2")
    knight = ChessPiece(KNIGHT, 3, 4, player_1)
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
        ChessMove(KNIGHT, 3, 4, 2, 2),
        ChessMove(KNIGHT, 3, 4, 1, 3),
        ChessMove(KNIGHT, 3, 4, 1, 5),
        ChessMove(KNIGHT, 3, 4, 2, 6),
        ChessMove(KNIGHT, 3, 4, 4, 6),
        ChessMove(KNIGHT, 3, 4, 5, 5),
        ChessMove(KNIGHT, 3, 4, 5, 3),
        ChessMove(KNIGHT, 3, 4, 4, 2),
    ]
    assert compare_move_tables(
        chess_state._get_moves_knight(knight), expected_moves
    )


def test_knight_moves_corner():
    player_1 = Player("1")
    player_2 = Player("2")
    knight = ChessPiece(KNIGHT, 0, 0, player_1)
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
        ChessMove(KNIGHT, 0, 0, 2, 1),
        ChessMove(KNIGHT, 0, 0, 1, 2),
    ]
    assert chess_state._get_moves_knight(knight) == expected_moves


def test_knight_moves_can_take():
    player_1 = Player("1")
    player_2 = Player("2")
    knight_1 = ChessPiece(KNIGHT, 3, 4, player_1)
    knight_2 = ChessPiece(KNIGHT, 2, 6, player_2)
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
        ChessMove(KNIGHT, 3, 4, 2, 2),
        ChessMove(KNIGHT, 3, 4, 1, 3),
        ChessMove(KNIGHT, 3, 4, 1, 5),
        ChessMove(KNIGHT, 3, 4, 2, 6),
        ChessMove(KNIGHT, 3, 4, 4, 6),
        ChessMove(KNIGHT, 3, 4, 5, 5),
        ChessMove(KNIGHT, 3, 4, 5, 3),
        ChessMove(KNIGHT, 3, 4, 4, 2),
    ]
    assert compare_move_tables(
        chess_state._get_moves_knight(knight_1), expected_moves
    )


def test_knight_moves_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    knight_1 = ChessPiece(KNIGHT, 3, 4, player_1)
    knight_2 = ChessPiece(KNIGHT, 2, 6, player_1)
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
        ChessMove(KNIGHT, 3, 4, 2, 2),
        ChessMove(KNIGHT, 3, 4, 1, 3),
        ChessMove(KNIGHT, 3, 4, 1, 5),
        ChessMove(KNIGHT, 3, 4, 4, 6),
        ChessMove(KNIGHT, 3, 4, 5, 5),
        ChessMove(KNIGHT, 3, 4, 5, 3),
        ChessMove(KNIGHT, 3, 4, 4, 2),
    ]
    assert compare_move_tables(
        chess_state._get_moves_knight(knight_1), expected_moves
    )


def test_bishop_moves_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    bishop_1 = ChessPiece(BISHOP, 3, 3, player_1)
    bishop_2 = ChessPiece(BISHOP, 1, 1, player_1)
    bishop_3 = ChessPiece(BISHOP, 5, 5, player_1)
    bishop_4 = ChessPiece(BISHOP, 1, 5, player_1)
    bishop_5 = ChessPiece(BISHOP, 5, 1, player_1)
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
        ChessMove(BISHOP, 3, 3, 2, 2),
        ChessMove(BISHOP, 3, 3, 4, 4),
        ChessMove(BISHOP, 3, 3, 2, 4),
        ChessMove(BISHOP, 3, 3, 4, 2),
    ]
    assert compare_move_tables(
        chess_state._get_moves_bishop(bishop_1), expected_moves
    )


def test_bishop_moves_can_take():
    player_1 = Player("1")
    player_2 = Player("2")
    bishop_1 = ChessPiece(BISHOP, 3, 3, player_1)
    bishop_2 = ChessPiece(BISHOP, 1, 1, player_2)
    bishop_3 = ChessPiece(BISHOP, 5, 5, player_2)
    bishop_4 = ChessPiece(BISHOP, 1, 5, player_2)
    bishop_5 = ChessPiece(BISHOP, 5, 1, player_2)
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
        ChessMove(BISHOP, 3, 3, 2, 2),
        ChessMove(BISHOP, 3, 3, 4, 4),
        ChessMove(BISHOP, 3, 3, 2, 4),
        ChessMove(BISHOP, 3, 3, 4, 2),
        ChessMove(BISHOP, 3, 3, 1, 1),
        ChessMove(BISHOP, 3, 3, 5, 5),
        ChessMove(BISHOP, 3, 3, 1, 5),
        ChessMove(BISHOP, 3, 3, 5, 1),
    ]
    assert compare_move_tables(
        chess_state._get_moves_bishop(bishop_1), expected_moves
    )


def test_bishop_moves_no_edge_cases():
    player_1 = Player("1")
    player_2 = Player("2")
    bishop = ChessPiece(BISHOP, 3, 3, player_1)
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
        ChessMove(BISHOP, 3, 3, 0, 0),
        ChessMove(BISHOP, 3, 3, 1, 1),
        ChessMove(BISHOP, 3, 3, 2, 2),
        ChessMove(BISHOP, 3, 3, 4, 4),
        ChessMove(BISHOP, 3, 3, 5, 5),
        ChessMove(BISHOP, 3, 3, 6, 6),
        ChessMove(BISHOP, 3, 3, 7, 7),
        ChessMove(BISHOP, 3, 3, 0, 6),
        ChessMove(BISHOP, 3, 3, 1, 5),
        ChessMove(BISHOP, 3, 3, 2, 4),
        ChessMove(BISHOP, 3, 3, 4, 2),
        ChessMove(BISHOP, 3, 3, 5, 1),
        ChessMove(BISHOP, 3, 3, 6, 0),
    ]
    assert compare_move_tables(
        chess_state._get_moves_bishop(bishop), expected_moves
    )


def test_rook_moves_no_edge_cases():
    player_1 = Player("1")
    player_2 = Player("2")
    rook = ChessPiece(ROOK, 3, 3, player_1)
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
        ChessMove(ROOK, 3, 3, 0, 3),
        ChessMove(ROOK, 3, 3, 1, 3),
        ChessMove(ROOK, 3, 3, 2, 3),
        ChessMove(ROOK, 3, 3, 4, 3),
        ChessMove(ROOK, 3, 3, 5, 3),
        ChessMove(ROOK, 3, 3, 6, 3),
        ChessMove(ROOK, 3, 3, 7, 3),
        ChessMove(ROOK, 3, 3, 3, 7),
        ChessMove(ROOK, 3, 3, 3, 6),
        ChessMove(ROOK, 3, 3, 3, 5),
        ChessMove(ROOK, 3, 3, 3, 4),
        ChessMove(ROOK, 3, 3, 3, 2),
        ChessMove(ROOK, 3, 3, 3, 1),
        ChessMove(ROOK, 3, 3, 3, 0),
    ]
    assert compare_move_tables(
        chess_state._get_moves_rook(rook), expected_moves
    )


def test_rook_moves_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    rook_1 = ChessPiece(ROOK, 3, 3, player_1)
    rook_2 = ChessPiece(ROOK, 3, 1, player_1)
    rook_3 = ChessPiece(ROOK, 1, 3, player_1)
    rook_4 = ChessPiece(ROOK, 5, 3, player_1)
    rook_5 = ChessPiece(ROOK, 3, 5, player_1)
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
        ChessMove(ROOK, 3, 3, 2, 3),
        ChessMove(ROOK, 3, 3, 4, 3),
        ChessMove(ROOK, 3, 3, 3, 4),
        ChessMove(ROOK, 3, 3, 3, 2),
    ]
    assert compare_move_tables(
        chess_state._get_moves_rook(rook_1), expected_moves
    )


def test_rook_moves_can_take():
    player_1 = Player("1")
    player_2 = Player("2")
    rook_1 = ChessPiece(ROOK, 3, 3, player_1)
    rook_2 = ChessPiece(ROOK, 3, 1, player_2)
    rook_3 = ChessPiece(ROOK, 1, 3, player_2)
    rook_4 = ChessPiece(ROOK, 5, 3, player_2)
    rook_5 = ChessPiece(ROOK, 3, 5, player_2)
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
        ChessMove(ROOK, 3, 3, 2, 3),
        ChessMove(ROOK, 3, 3, 4, 3),
        ChessMove(ROOK, 3, 3, 3, 4),
        ChessMove(ROOK, 3, 3, 3, 2),
        ChessMove(ROOK, 3, 3, 1, 3),
        ChessMove(ROOK, 3, 3, 5, 3),
        ChessMove(ROOK, 3, 3, 3, 5),
        ChessMove(ROOK, 3, 3, 3, 1),
    ]
    assert compare_move_tables(
        chess_state._get_moves_rook(rook_1), expected_moves
    )


def test_queen_moves_no_edge_cases():
    player_1 = Player("1")
    player_2 = Player("2")
    queen = ChessPiece(QUEEN, 3, 3, player_1)
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
        ChessMove(QUEEN, 3, 3, 0, 3),
        ChessMove(QUEEN, 3, 3, 1, 3),
        ChessMove(QUEEN, 3, 3, 2, 3),
        ChessMove(QUEEN, 3, 3, 4, 3),
        ChessMove(QUEEN, 3, 3, 5, 3),
        ChessMove(QUEEN, 3, 3, 6, 3),
        ChessMove(QUEEN, 3, 3, 7, 3),
        ChessMove(QUEEN, 3, 3, 3, 7),
        ChessMove(QUEEN, 3, 3, 3, 6),
        ChessMove(QUEEN, 3, 3, 3, 5),
        ChessMove(QUEEN, 3, 3, 3, 4),
        ChessMove(QUEEN, 3, 3, 3, 2),
        ChessMove(QUEEN, 3, 3, 3, 1),
        ChessMove(QUEEN, 3, 3, 3, 0),
        ChessMove(QUEEN, 3, 3, 0, 0),
        ChessMove(QUEEN, 3, 3, 1, 1),
        ChessMove(QUEEN, 3, 3, 2, 2),
        ChessMove(QUEEN, 3, 3, 4, 4),
        ChessMove(QUEEN, 3, 3, 5, 5),
        ChessMove(QUEEN, 3, 3, 6, 6),
        ChessMove(QUEEN, 3, 3, 7, 7),
        ChessMove(QUEEN, 3, 3, 0, 6),
        ChessMove(QUEEN, 3, 3, 1, 5),
        ChessMove(QUEEN, 3, 3, 2, 4),
        ChessMove(QUEEN, 3, 3, 4, 2),
        ChessMove(QUEEN, 3, 3, 5, 1),
        ChessMove(QUEEN, 3, 3, 6, 0),
    ]
    assert compare_move_tables(
        chess_state._get_moves_queen(queen), expected_moves
    )


def test_queen_moves_can_take():
    player_1 = Player("1")
    player_2 = Player("2")
    queen = ChessPiece(QUEEN, 3, 3, player_1, False)
    pawn_1 = ChessPiece(PAWN, 2, 2, player_2, False)
    pawn_2 = ChessPiece(PAWN, 3, 2, player_2, False)
    pawn_3 = ChessPiece(PAWN, 4, 2, player_2, False)
    pawn_4 = ChessPiece(PAWN, 2, 3, player_2, False)
    pawn_5 = ChessPiece(PAWN, 2, 4, player_2, False)
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
        ChessMove(QUEEN, 3, 3, 2, 3),
        ChessMove(QUEEN, 3, 3, 4, 3),
        ChessMove(QUEEN, 3, 3, 3, 4),
        ChessMove(QUEEN, 3, 3, 3, 2),
        ChessMove(QUEEN, 3, 3, 2, 2),
        ChessMove(QUEEN, 3, 3, 4, 4),
        ChessMove(QUEEN, 3, 3, 2, 4),
        ChessMove(QUEEN, 3, 3, 4, 2),
        ChessMove(QUEEN, 3, 3, 3, 5),
        ChessMove(QUEEN, 3, 3, 3, 6),
        ChessMove(QUEEN, 3, 3, 3, 7),
        ChessMove(QUEEN, 3, 3, 5, 5),
        ChessMove(QUEEN, 3, 3, 6, 6),
        ChessMove(QUEEN, 3, 3, 7, 7),
        ChessMove(QUEEN, 3, 3, 5, 3),
        ChessMove(QUEEN, 3, 3, 6, 3),
        ChessMove(QUEEN, 3, 3, 7, 3),
    ]
    assert compare_move_tables(
        chess_state._get_moves_queen(queen), expected_moves
    )


def test_queen_moves_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    queen = ChessPiece(QUEEN, 3, 3, player_1, False)
    pawn_1 = ChessPiece(PAWN, 2, 2, player_1, False)
    pawn_2 = ChessPiece(PAWN, 3, 2, player_1, False)
    pawn_3 = ChessPiece(PAWN, 4, 2, player_1, False)
    pawn_4 = ChessPiece(PAWN, 2, 3, player_1, False)
    pawn_5 = ChessPiece(PAWN, 2, 4, player_1, False)
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
        ChessMove(QUEEN, 3, 3, 4, 3),
        ChessMove(QUEEN, 3, 3, 3, 4),
        ChessMove(QUEEN, 3, 3, 4, 4),
        ChessMove(QUEEN, 3, 3, 3, 5),
        ChessMove(QUEEN, 3, 3, 3, 6),
        ChessMove(QUEEN, 3, 3, 3, 7),
        ChessMove(QUEEN, 3, 3, 5, 5),
        ChessMove(QUEEN, 3, 3, 6, 6),
        ChessMove(QUEEN, 3, 3, 7, 7),
        ChessMove(QUEEN, 3, 3, 5, 3),
        ChessMove(QUEEN, 3, 3, 6, 3),
        ChessMove(QUEEN, 3, 3, 7, 3),
    ]
    assert compare_move_tables(
        chess_state._get_moves_queen(queen), expected_moves
    )


def test_king_moves_no_edge_cases():
    player_1 = Player("1")
    player_2 = Player("2")
    king = ChessPiece(KING, 3, 3, player_1, False)
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
        ChessMove(KING, 3, 3, 2, 3),
        ChessMove(KING, 3, 3, 4, 3),
        ChessMove(KING, 3, 3, 3, 4),
        ChessMove(KING, 3, 3, 3, 2),
        ChessMove(KING, 3, 3, 2, 2),
        ChessMove(KING, 3, 3, 4, 4),
        ChessMove(KING, 3, 3, 2, 4),
        ChessMove(KING, 3, 3, 4, 2),
    ]
    assert compare_move_tables(
        chess_state._get_moves_king(king), expected_moves
    )


def test_king_moves_can_take():
    player_1 = Player("1")
    player_2 = Player("2")
    king = ChessPiece(KING, 3, 3, player_1, False)
    pawn_1 = ChessPiece(PAWN, 2, 2, player_2, False)
    pawn_2 = ChessPiece(PAWN, 3, 2, player_2, False)
    pawn_3 = ChessPiece(PAWN, 4, 2, player_2, False)
    pawn_4 = ChessPiece(PAWN, 2, 3, player_2, False)
    pawn_5 = ChessPiece(PAWN, 2, 4, player_2, False)
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
        ChessMove(KING, 3, 3, 2, 3),
        ChessMove(KING, 3, 3, 4, 3),
        ChessMove(KING, 3, 3, 3, 4),
        ChessMove(KING, 3, 3, 3, 2),
        ChessMove(KING, 3, 3, 2, 2),
        ChessMove(KING, 3, 3, 4, 4),
        ChessMove(KING, 3, 3, 2, 4),
        ChessMove(KING, 3, 3, 4, 2),
    ]
    assert compare_move_tables(
        chess_state._get_moves_king(king), expected_moves
    )


def test_king_moves_blocked():
    player_1 = Player("1")
    player_2 = Player("2")
    king = ChessPiece(KING, 3, 3, player_1, False)
    pawn_1 = ChessPiece(PAWN, 2, 2, player_1, False)
    pawn_2 = ChessPiece(PAWN, 3, 2, player_1, False)
    pawn_3 = ChessPiece(PAWN, 4, 2, player_1, False)
    pawn_4 = ChessPiece(PAWN, 2, 3, player_1, False)
    pawn_5 = ChessPiece(PAWN, 2, 4, player_1, False)
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
        ChessMove(KING, 3, 3, 4, 3),
        ChessMove(KING, 3, 3, 3, 4),
        ChessMove(KING, 3, 3, 4, 4),
    ]
    assert compare_move_tables(
        chess_state._get_moves_king(king), expected_moves
    )


def test_king_moves_can_castle():
    player_1 = Player("1")
    player_2 = Player("2")
    king = ChessPiece(KING, 4, 0, player_1)
    rook_1 = ChessPiece(ROOK, 0, 0, player_1)
    rook_2 = ChessPiece(ROOK, 7, 0, player_1)
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
        ChessMove(KING, 4, 0, 3, 0),
        ChessMove(KING, 4, 0, 3, 1),
        ChessMove(KING, 4, 0, 4, 1),
        ChessMove(KING, 4, 0, 5, 1),
        ChessMove(KING, 4, 0, 5, 0),
        ChessMove(KING, 4, 0, 2, 0),
        ChessMove(KING, 4, 0, 6, 0),
    ]
    assert compare_move_tables(
        chess_state._get_moves_king(king), expected_moves
    )


def test_king_moves_cant_castle_king_moved():
    player_1 = Player("1")
    player_2 = Player("2")
    king = ChessPiece(KING, 4, 0, player_1, False)
    rook_1 = ChessPiece(ROOK, 0, 0, player_1)
    rook_2 = ChessPiece(ROOK, 7, 0, player_1)
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
        ChessMove(KING, 4, 0, 3, 0),
        ChessMove(KING, 4, 0, 3, 1),
        ChessMove(KING, 4, 0, 4, 1),
        ChessMove(KING, 4, 0, 5, 1),
        ChessMove(KING, 4, 0, 5, 0),
    ]
    assert compare_move_tables(
        chess_state._get_moves_king(king), expected_moves
    )


def test_king_moves_cant_castle_rooks_moved():
    player_1 = Player("1")
    player_2 = Player("2")
    king = ChessPiece(KING, 4, 0, player_1)
    rook_1 = ChessPiece(ROOK, 0, 0, player_1, False)
    rook_2 = ChessPiece(ROOK, 7, 0, player_1, False)
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
        ChessMove(KING, 4, 0, 3, 0),
        ChessMove(KING, 4, 0, 3, 1),
        ChessMove(KING, 4, 0, 4, 1),
        ChessMove(KING, 4, 0, 5, 1),
        ChessMove(KING, 4, 0, 5, 0),
    ]
    assert compare_move_tables(
        chess_state._get_moves_king(king), expected_moves
    )


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
        ChessMove(PAWN, 0, 1, 0, 2),
        ChessMove(PAWN, 0, 1, 0, 3),
        ChessMove(PAWN, 1, 1, 1, 2),
        ChessMove(PAWN, 1, 1, 1, 3),
        ChessMove(PAWN, 2, 1, 2, 2),
        ChessMove(PAWN, 2, 1, 2, 3),
        ChessMove(PAWN, 3, 1, 3, 2),
        ChessMove(PAWN, 3, 1, 3, 3),
        ChessMove(PAWN, 4, 1, 4, 2),
        ChessMove(PAWN, 4, 1, 4, 3),
        ChessMove(PAWN, 5, 1, 5, 2),
        ChessMove(PAWN, 5, 1, 5, 3),
        ChessMove(PAWN, 6, 1, 6, 2),
        ChessMove(PAWN, 6, 1, 6, 3),
        ChessMove(PAWN, 7, 1, 7, 2),
        ChessMove(PAWN, 7, 1, 7, 3),
        ChessMove(KNIGHT, 1, 0, 0, 2),
        ChessMove(KNIGHT, 1, 0, 2, 2),
        ChessMove(KNIGHT, 6, 0, 5, 2),
        ChessMove(KNIGHT, 6, 0, 7, 2),
    ]
    assert compare_move_tables(chess_state.get_moves(), expected_moves)


def test_get_moves_init_empty_black_move():
    player_1 = Player("1")
    player_2 = Player("2")
    chess_state = ChessState(player_2, player_1, player_1)
    expected_moves = [
        ChessMove(PAWN, 0, 6, 0, 5),
        ChessMove(PAWN, 0, 6, 0, 4),
        ChessMove(PAWN, 1, 6, 1, 5),
        ChessMove(PAWN, 1, 6, 1, 4),
        ChessMove(PAWN, 2, 6, 2, 5),
        ChessMove(PAWN, 2, 6, 2, 4),
        ChessMove(PAWN, 3, 6, 3, 5),
        ChessMove(PAWN, 3, 6, 3, 4),
        ChessMove(PAWN, 4, 6, 4, 5),
        ChessMove(PAWN, 4, 6, 4, 4),
        ChessMove(PAWN, 5, 6, 5, 5),
        ChessMove(PAWN, 5, 6, 5, 4),
        ChessMove(PAWN, 6, 6, 6, 5),
        ChessMove(PAWN, 6, 6, 6, 4),
        ChessMove(PAWN, 7, 6, 7, 5),
        ChessMove(PAWN, 7, 6, 7, 4),
        ChessMove(KNIGHT, 1, 7, 0, 5),
        ChessMove(KNIGHT, 1, 7, 2, 5),
        ChessMove(KNIGHT, 6, 7, 5, 5),
        ChessMove(KNIGHT, 6, 7, 7, 5),
    ]
    assert compare_move_tables(chess_state.get_moves(), expected_moves)
