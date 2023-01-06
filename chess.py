"""
Pseudocode:

class Board:
    reset_board():
        init board, which is a dictionary[col][row], which contains None or Piece
        init taken, which is an empty list
        fill in the board with pieces:
            board["A"][1] = Rook("W")
            board["H"][1] = Rook("W')
            ...

    __init__():
        reset_board()

    is_check():
        loop thru all pieces see if their "valid moving location" includes the king
        return White, Black, or None

    is_checkmate():
        loop thru all pieces and check_movable_place()
        if all are empty, return colour

    check_movable_place(location_of_piece):
        if location doesn't have piece return None or empty list
        moveable = type(board[location_of_piece]).can_move_to(board, location_of_piece)
        if in check, remove all locations that doesn't stop a check

    move_piece(from, to)

class Piece:
    moved = False
    move_number = 0
    (pawn only) first_move_length = 1 or 2
    colour = W/B
    can_move_to(board, from_location):
        follow piece rule to find all place movable
        remove places blocked by own / enemy piece
        remove places of own piece
        special pieces have special rules (en passant OR castle)
            pawn:
                check moved: -> if not add 2 blocks in the front
                out of 2 blocks, check if first one is blocked, if so remove both
                check 2nd block, if blocked remove
                check surrounding (diagonal) -> if they are enemy piece, add them
                check left and right side -> if they are pawn, AND is their first move, AND they moved 2 blocks
                -> add diagonal right to moveable
            king:
                check moved: if not check if have unobstructed path to rook -> if so check the rook's "moved" status
                -> also check all other pieces (of enemy) if they can move to either location the king will pass


"""


class Piece:
    def __init__(self, colour, moved=False, move_number=0):
        self.colour = colour
        self.moved = moved
        self.move_number = move_number

    def can_move_to(self, board, from_location):
        """
        return a list of all possible locations the piece can move to, ignoring check restriction
        :param board: Board object that the piece is on (to check if the move is valid)
        :param from_location: Tuple of (col, row) of the piece's current location
        :return: a list of all possible locations (in tuple) the piece can move to, ignoring check restriction
        """
        pass

    def moved(self):
        self.moved = True
        self.move_number += 1

    def __str__(self):
        return self.colour + self.__class__.__name__

    def __repr__(self):
        return self.__str__()


class Pawn(Piece):
    def __init__(self, colour, moved=False, move_number=0):
        super().__init__(colour, moved, move_number)
        self.first_move_length = 0  # change to 1 or 2 when the pawn is first moved

    def can_move_to(self, board, from_location):
        # TODO: check if destination is out of board, which may cause index out of range
        possible_destinations = []
        col, row = from_location
        if self.colour == "W" and board[col][row + 1] is None:
            possible_destinations.append((col, row + 1))
            if not self.moved and board[col][row + 2] is None:
                possible_destinations.append((col, row + 2))
        if self.colour == "W":
            if board[col + 1][row + 1] is not None and board[col + 1][row + 1].colour == "B":
                possible_destinations.append((col + 1, row + 1))
            if board[col - 1][row + 1] is not None and board[col - 1][row + 1].colour == "B":
                possible_destinations.append((col - 1, row + 1))

        if self.colour == "B" and board[col][row - 1] is None:
            possible_destinations.append((col, row - 1))
            if not self.moved and board[col][row - 2] is None:
                possible_destinations.append((col, row - 2))
        if self.colour == "B":
            if board[col + 1][row - 1] is not None and board[col + 1][row - 1].colour == "W":
                possible_destinations.append((col + 1, row - 1))
            if board[col - 1][row - 1] is not None and board[col - 1][row - 1].colour == "W":
                possible_destinations.append((col - 1, row - 1))

        if board[col + 1][row] is not None and board[col + 1][row].colour != self.colour and type(board[col + 1][row]) is Pawn and board[col + 1][row].first_move_length == 2:
            possible_destinations.append((col + 1, row + 1))
        if board[col - 1][row] is not None and board[col - 1][row].colour != self.colour and type(board[col - 1][row]) is Pawn and board[col - 1][row].first_move_length == 2:
            possible_destinations.append((col - 1, row + 1))

        for col, row in possible_destinations:
            if 0 > col or col > 7 or 0 > row or row > 7:
                possible_destinations.remove((col, row))
        return possible_destinations


class Rook(Piece):
    def can_move_to(self, board, from_location):
        possible_destinations = []
        col, row = from_location
        for i in range(1, 8):
            if 0 <= col + i <= 7:
                if board[col + i][row] is None or board[col + i][row].colour != self.colour:
                    possible_destinations.append((col + i, row))
                elif board[col + i][row].colour != self.colour:
                    possible_destinations.append((col + i, row))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= col - i <= 7:
                if board[col - i][row] is None:
                    possible_destinations.append((col - i, row))
                elif board[col - i][row].colour != self.colour:
                    possible_destinations.append((col - i, row))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= row + i <= 7:
                if board[col][row + i] is None:
                    possible_destinations.append((col, row + i))
                elif board[col][row + i].colour != self.colour:
                    possible_destinations.append((col, row + i))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= row - i <= 7:
                if board[col][row - i] is None:
                    possible_destinations.append((col, row - i))
                elif board[col][row - i].colour != self.colour:
                    possible_destinations.append((col, row - i))
                    break
                else:
                    break
            else:
                break

        return possible_destinations


class Knight(Piece):
    def can_move_to(self, board, from_location):
        possible_destinations = []
        col, row = from_location
        if 0 <= col + 2 <= 7 and 0 <= row + 1 <= 7:
            if board[col + 2][row + 1] is None or board[col + 2][row + 1].colour != self.colour:
                possible_destinations.append((col + 2, row + 1))
        if 0 <= col + 2 <= 7 and 0 <= row - 1 <= 7:
            if board[col + 2][row - 1] is None or board[col + 2][row - 1].colour != self.colour:
                possible_destinations.append((col + 2, row - 1))
        if 0 <= col - 2 <= 7 and 0 <= row + 1 <= 7:
            if board[col - 2][row + 1] is None or board[col - 2][row + 1].colour != self.colour:
                possible_destinations.append((col - 2, row + 1))
        if 0 <= col - 2 <= 7 and 0 <= row - 1 <= 7:
            if board[col - 2][row - 1] is None or board[col - 2][row - 1].colour != self.colour:
                possible_destinations.append((col - 2, row - 1))
        if 0 <= col + 1 <= 7 and 0 <= row + 2 <= 7:
            if board[col + 1][row + 2] is None or board[col + 1][row + 2].colour != self.colour:
                possible_destinations.append((col + 1, row + 2))
        if 0 <= col + 1 <= 7 and 0 <= row - 2 <= 7:
            if board[col + 1][row - 2] is None or board[col + 1][row - 2].colour != self.colour:
                possible_destinations.append((col + 1, row - 2))
        if 0 <= col - 1 <= 7 and 0 <= row + 2 <= 7:
            if board[col - 1][row + 2] is None or board[col - 1][row + 2].colour != self.colour:
                possible_destinations.append((col - 1, row + 2))
        if 0 <= col - 1 <= 7 and 0 <= row - 2 <= 7:
            if board[col - 1][row - 2] is None or board[col - 1][row - 2].colour != self.colour:
                possible_destinations.append((col - 1, row - 2))
        return possible_destinations


class Bishop(Piece):
    def can_move_to(self, board, from_location):
        possible_destinations = []
        col, row = from_location
        for i in range(1, 8):
            if 0 <= col + i <= 7 and 0 <= row + i <= 7:
                if board[col + i][row + i] is None:
                    possible_destinations.append((col + i, row + i))
                elif board[col + i][row + i].colour != self.colour:
                    possible_destinations.append((col + i, row + i))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= col - i <= 7 and 0 <= row - i <= 7:
                if board[col - i][row - i] is None:
                    possible_destinations.append((col - i, row - i))
                elif board[col - i][row - i].colour != self.colour:
                    possible_destinations.append((col - i, row - i))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= col + i <= 7 and 0 <= row - i <= 7:
                if board[col + i][row - i] is None:
                    possible_destinations.append((col + i, row - i))
                elif board[col + i][row - i].colour != self.colour:
                    possible_destinations.append((col + i, row - i))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= col - i <= 7 and 0 <= row + i <= 7:
                if board[col - i][row + i] is None:
                    possible_destinations.append((col - i, row + i))
                elif board[col - i][row + i].colour != self.colour:
                    possible_destinations.append((col - i, row + i))
                    break
                else:
                    break
            else:
                break

        return possible_destinations


class Queen(Piece):
    def can_move_to(self, board, from_location):
        possible_destinations = []
        col, row = from_location
        for i in range(1, 8):
            if 0 <= col + i <= 7 and 0 <= row + i <= 7:
                if board[col + i][row + i] is None:
                    possible_destinations.append((col + i, row + i))
                elif board[col + i][row + i].colour != self.colour:
                    possible_destinations.append((col + i, row + i))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= col - i <= 7 and 0 <= row - i <= 7:
                if board[col - i][row - i] is None:
                    possible_destinations.append((col - i, row - i))
                elif board[col - i][row - i].colour != self.colour:
                    possible_destinations.append((col - i, row - i))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= col + i <= 7 and 0 <= row - i <= 7:
                if board[col + i][row - i] is None:
                    possible_destinations.append((col + i, row - i))
                elif board[col + i][row - i].colour != self.colour:
                    possible_destinations.append((col + i, row - i))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= col - i <= 7 and 0 <= row + i <= 7:
                if board[col - i][row + i] is None:
                    possible_destinations.append((col - i, row + i))
                elif board[col - i][row + i].colour != self.colour:
                    possible_destinations.append((col - i, row + i))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= col + i <= 7:
                if board[col + i][row] is None:
                    possible_destinations.append((col + i, row))
                elif board[col + i][row].colour != self.colour:
                    possible_destinations.append((col + i, row))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= col - i <= 7:
                if board[col - i][row] is None:
                    possible_destinations.append((col - i, row))
                elif board[col - i][row].colour != self.colour:
                    possible_destinations.append((col - i, row))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= row + i <= 7:
                if board[col][row + i] is None:
                    possible_destinations.append((col, row + i))
                elif board[col][row + i].colour != self.colour:
                    possible_destinations.append((col, row + i))
                    break
                else:
                    break
            else:
                break

        for i in range(1, 8):
            if 0 <= row - i <= 7:
                if board[col][row - i] is None:
                    possible_destinations.append((col, row - i))
                elif board[col][row - i].colour != self.colour:
                    possible_destinations.append((col, row - i))
                    break
                else:
                    break
            else:
                break

        return possible_destinations


class King(Piece):
    def can_move_to(self, board, from_location):
        possible_destinations = []
        col, row = from_location
        if 0 <= col + 1 <= 7 and 0 <= row + 1 <= 7:
            if board[col + 1][row + 1] is None or board[col + 1][row + 1].colour != self.colour:
                possible_destinations.append((col + 1, row + 1))
        if 0 <= col + 1 <= 7 and 0 <= row - 1 <= 7:
            if board[col + 1][row - 1] is None or board[col + 1][row - 1].colour != self.colour:
                possible_destinations.append((col + 1, row - 1))
        if 0 <= col - 1 <= 7 and 0 <= row + 1 <= 7:
            if board[col - 1][row + 1] is None or board[col - 1][row + 1].colour != self.colour:
                possible_destinations.append((col - 1, row + 1))
        if 0 <= col - 1 <= 7 and 0 <= row - 1 <= 7:
            if board[col - 1][row - 1] is None or board[col - 1][row - 1].colour != self.colour:
                possible_destinations.append((col - 1, row - 1))
        if 0 <= col + 1 <= 7:
            if board[col + 1][row] is None or board[col + 1][row].colour != self.colour:
                possible_destinations.append((col + 1, row))
        if 0 <= col - 1 <= 7:
            if board[col - 1][row] is None or board[col - 1][row].colour != self.colour:
                possible_destinations.append((col - 1, row))
        if 0 <= row + 1 <= 7:
            if board[col][row + 1] is None or board[col][row + 1].colour != self.colour:
                possible_destinations.append((col, row + 1))
        if 0 <= row - 1 <= 7:
            if board[col][row - 1] is None or board[col][row - 1].colour != self.colour:
                possible_destinations.append((col, row - 1))

        if not self.moved:
            if board[0][row] is not None and not board[0][row].moved:
                if board[1][row] is None and board[2][row] is None and board[3][row] is None:
                    possible_destinations.append((2, row))
            if board[7][row] is not None and not board[7][row].moved:
                if board[5][row] is None and board[6][row] is None:
                    possible_destinations.append((6, row))
        return possible_destinations

class Board:
    def reset_board(self):
        # TODO: store the king's position
        self.board = {}
        for i in range(8):
            self.board[i] = {}
            for j in range(8):
                self.board[i][j] = None
        self.taken = []

        self.board[0][0] = Rook("W")
        self.board[7][0] = Rook("W")
        self.board[1][0] = Knight("W")
        self.board[6][0] = Knight("W")
        self.board[2][0] = Bishop("W")
        self.board[5][0] = Bishop("W")
        self.board[3][0] = Queen("W")
        self.board[4][0] = King("W")
        for i in range(8):
            self.board[i][1] = Pawn("W")
        self.board[0][7] = Rook("B")
        self.board[7][7] = Rook("B")
        self.board[1][7] = Knight("B")
        self.board[6][7] = Knight("B")
        self.board[2][7] = Bishop("B")
        self.board[5][7] = Bishop("B")
        self.board[3][7] = Queen("B")
        self.board[4][7] = King("B")
        for i in range(8):
            self.board[i][6] = Pawn("B")

    def __init__(self):
        self.reset_board()

    def under_check(self, colour):
        # TODO: for every enemy piece, find movable squares and see if they include the king square
        # TODO: check for castling (you can't castle if will be under check even if result of castle is checkmate on opponent)
        pass

    def under_checkmate(self, colour):
        pass

    def check_movable_place(self, from_location):
        pass

    def make_move(self, from_location, to_location):
        # TODO: remember to check for en passant takes
        # TODO: remember to check for castling
        # TODO: remember to call moved() on the piece
        pass


