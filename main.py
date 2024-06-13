# Import modules
from enum import Enum
import numpy as np

# Peice type enum
class PieceType(Enum):
    EMPTY = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

# Color type enum
class Color(Enum):
    VOID_CELL = 0 
    WHITE = 1
    BLACK = 2

# Peice class
class Piece:
    def __init__(self, piece_type=PieceType.EMPTY, color=Color.NONE, x=None, y=None, dead=False):
        self.piece_type = piece_type
        self.color = color
        self.x = x
        self.y = y
        self.dead = dead

    def __repr__(self):
        return f'{self.color.name[0]}{self.piece_type.name[0]}'

# Cell class
class Cell:
    def __init__(self, piece=Piece(), x=None, y=None):
        self.piece = piece
        self.x = x
        self.y = y
        if piece.piece_type != PieceType.EMPTY:
            piece.x = x
            piece.y = y

    def __repr__(self):
        return str(self.piece)

# Chessboard class
class ChessBoard:
    def __init__(self):
        self.board = np.array([[Cell(x=i, y=j) for j in range(8)] for i in range(8)])
        self.initialize_board()

    def initialize_board(self):
        # Place pieces in their initial positions
        
        # Pawns
        for i in range(8):
            self.board[1][i] = Cell(Piece(PieceType.PAWN, Color.BLACK), x=1, y=i)
            self.board[6][i] = Cell(Piece(PieceType.PAWN, Color.WHITE), x=6, y=i)

        # Rooks
        self.board[0][0] = self.board[0][7] = Cell(Piece(PieceType.ROOK, Color.BLACK), x=0, y=0)
        self.board[7][0] = self.board[7][7] = Cell(Piece(PieceType.ROOK, Color.WHITE), x=7, y=0)

        # Knights
        self.board[0][1] = self.board[0][6] = Cell(Piece(PieceType.KNIGHT, Color.BLACK), x=0, y=1)
        self.board[7][1] = self.board[7][6] = Cell(Piece(PieceType.KNIGHT, Color.WHITE), x=7, y=1)

        # Bishops
        self.board[0][2] = self.board[0][5] = Cell(Piece(PieceType.BISHOP, Color.BLACK), x=0, y=2)
        self.board[7][2] = self.board[7][5] = Cell(Piece(PieceType.BISHOP, Color.WHITE), x=7, y=2)

        # Queens
        self.board[0][3] = Cell(Piece(PieceType.QUEEN, Color.BLACK), x=0, y=3)
        self.board[7][3] = Cell(Piece(PieceType.QUEEN, Color.WHITE), x=7, y=3)

        # Kings
        self.board[0][4] = Cell(Piece(PieceType.KING, Color.BLACK), x=0, y=4)
        self.board[7][4] = Cell(Piece(PieceType.KING, Color.WHITE), x=7, y=4)

    # Print board function
    def print_board(self):
        for row in self.board:
            print(' '.join([str(cell) for cell in row]))


        if piece.piece_type == PieceType.PAWN:
            moves = self.get_pawn_moves(x, y, piece.color)
        # I need help
        return moves

    def get_pawn_moves(self, x, y, color):
        moves = []
        direction = -1 if color == Color.WHITE else 1
        if self.is_valid_move(x + direction, y):
            moves.append((x, y, x + direction, y))
        return moves

    def is_valid_move(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8 and self.board[x][y].piece.piece_type == PieceType.EMPTY
class ChessAI:
    def __init__(self, board):
        self.board = board

    def evaluate_board(self):
        # Simple evaluation function: difference in piece values
        value = 0
        for row in self.board.board:
            for cell in row:
                piece = cell.piece
                if piece.color == Color.WHITE:
                    value += self.get_piece_value(piece)
                elif piece.color == Color.BLACK:
                    value -= self.get_piece_value(piece)
        return value

    def get_piece_value(self, piece):
        if piece.piece_type == PieceType.PAWN:
            return 1
        elif piece.piece_type == PieceType.KNIGHT or piece.piece_type == PieceType.BISHOP:
            return 3
        elif piece.piece_type == PieceType.ROOK:
            return 5
        elif piece.piece_type == PieceType.QUEEN:
            return 9
        elif piece.piece_type == PieceType.KING:
            return 1000
        return 0

    def minimax(self, depth, is_maximizing):
        if depth == 0:
            return self.evaluate_board()

        possible_moves = self.board.get_possible_moves(Color.WHITE if is_maximizing else Color.BLACK)
        if is_maximizing:
            max_eval = float('-inf')
            for move in possible_moves:
                self.board.make_move(move)
                eval = self.minimax(depth - 1, False)
                self.board.undo_move(move)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                self.board.make_move(move)
                eval = self.minimax(depth - 1, True)
                self.board.undo_move(move)
                min_eval = min(min_eval, eval)
            return min_eval

    def get_best_move(self, depth):
        best_move = None
        best_value = float('-inf')
        possible_moves = self.board.get_possible_moves(Color.WHITE)
        for move in possible_moves:
            self.board.make_move(move)
            move_value = self.minimax(depth - 1, False)
            self.board.undo_move(move)
            if move_value > best_value:
                best_value = move_value
                best_move = move
        return best_move
    def make_move(self, move):
        x1, y1, x2, y2 = move
        self.board[x2][y2].piece = self.board[x1][y1].piece
        self.board[x1][y1].piece = Piece()

    def undo_move(self, move):
        x1, y1, x2, y2 = move
        self.board[x1][y1].piece = self.board[x2][y2].piece
        self.board[x2][y2].piece = Piece()

if __name__ == "__main__":
    chess_board = ChessBoard()
    chess_ai = ChessAI(chess_board)
    chess_board.print_board()

    best_move = chess_ai.get_best_move(depth=3)
    if best_move:
        chess_board.make_move(best_move)
        print("AI move:", best_move)
        chess_board.print_board()
