class CoordinatesOutOfBoundsException(Exception):
    def __init__(self):
        super().__init__("Coordinate(s) out of bounds in the called function.")


class IncorrectPieceTypeException(Exception):
    def __init__(self):
        super().__init__("Wrong chess piece type in the called function.")


class InvalidMoveException(Exception):
    def __init__(self):
        super().__init__("Invalid move given to the function.")


class WhitePlayerNotInTheGameException(Exception):
    def __init__(self):
        super().__init__(
            "White player isn't either the current player or the other player."
        )
