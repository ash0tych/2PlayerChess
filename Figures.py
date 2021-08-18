import pygame
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'Assets')

class ChessFigure(pygame.sprite.Sprite):
    def __init__(self, color, xy):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = None
        self.first_move = False
        self.xy = (xy[1], xy[0])

    def get_image(self):
        return self.image

    def get_vertical_move(self, board, color):
        moves = set()
        i, j = self.xy
        while i > 0 and board[i - 1][j].color == 'none':
            i -= 1
            moves.add((j, i))

        if i != 0 and board[i - 1][j].color != color:
            moves.add((j, i - 1))

        i, j = self.xy
        while i < 7 and board[i + 1][j].color == 'none':
            i += 1
            moves.add((j, i))

        if i != 7 and board[i + 1][j].color != color:
            moves.add((j, i + 1))

        return moves

    def get_horizontal_move(self, board, color):
        moves = set()
        i, j = self.xy
        while j > 0 and board[i][j - 1].color == 'none':
            j -= 1
            moves.add((j, i))

        if j != 0 and board[i][j - 1].color != color:
            moves.add((j - 1, i))

        i, j = self.xy
        while j < 7 and board[i][j + 1].color == 'none':
            j += 1
            moves.add((j, i))

        if j != 7 and board[i][j + 1].color != color:
            moves.add((j + 1, i))

        return moves

    def get_main_diag(self, board, color):
        moves = set()
        i, j = self.xy
        while i > 0 and j > 0 and board[i - 1][j - 1].color == 'none':
            i -= 1
            j -= 1
            moves.add((j, i))

        if i != 0 and j != 0 and board[i - 1][j - 1].color != color:
            moves.add((j - 1, i - 1))

        i, j = self.xy
        while i < 7 and j < 7 and board[i + 1][j + 1].color == 'none':
            i += 1
            j += 1
            moves.add((j, i))

        if i != 7 and j != 7 and board[i + 1][j + 1].color != color:
            moves.add((j + 1, i + 1))

        return moves

    def get_side_diag(self, board, color):
        moves = set()
        i, j = self.xy
        while i > 0 and j < 7 and board[i - 1][j + 1].color == 'none':
            i -= 1
            j += 1
            moves.add((j, i))

        if i != 0 and j != 7 and board[i - 1][j + 1].color != color:
            moves.add((j + 1, i - 1))

        i, j = self.xy
        while i < 7 and j > 0 and board[i + 1][j - 1].color == 'none':
            i += 1
            j -= 1
            moves.add((j, i))

        if i != 7 and j != 0 and board[i + 1][j - 1].color != color:
            moves.add((j - 1, i + 1))

        return moves


class Pawn(ChessFigure):
    def __init__(self, color, xy):
        ChessFigure.__init__(self, color, xy)
        self.first_move = True
        if self.color == 'b':
            self.image = pygame.image.load(os.path.join(img_folder, 'bP.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wP.png'))

    def get_moves(self, board, color):
        return set.union(self.get_pawn_straight_moves(board, color), self.get_pawn_diag_moves(board, color))

    def get_pawn_straight_moves(self, board, color):
        moves = set()
        k = 1 if color == 'b' else -1
        buf_xy = (self.xy[1], self.xy[0])

        if buf_xy[1] < 7:
            if board[buf_xy[1] + k][buf_xy[0]].color == 'none':
                moves.add((buf_xy[0], buf_xy[1] + k))

            if self.first_move and board[buf_xy[1] + k][buf_xy[0]].color == \
                    board[buf_xy[1] + 2 * k][buf_xy[0]].color == 'none':
                moves.add((buf_xy[0], buf_xy[1] + 2 * k))
        return moves

    def get_pawn_diag_moves(self, board, color):
        moves = set()
        col = 'w' if color == 'b' else 'b'
        k = 1 if self.color == 'b' else -1
        buf_xy = (self.xy[1], self.xy[0])

        if buf_xy[1] < 7:
            if buf_xy[0] < 7 and board[buf_xy[1] + k][buf_xy[0] + 1].color == col:
                moves.add((buf_xy[0] + 1, buf_xy[1] + k))

            if buf_xy[0] > 0 and board[buf_xy[1] + k][buf_xy[0] - 1].color == col:
                moves.add((buf_xy[0] - 1, buf_xy[1] + k))

        return moves

    def get_possible_pawn_diag_moves(self):
        moves = set()
        k = 1 if self.color == 'b' else -1
        buf_xy = (self.xy[1], self.xy[0])
        if buf_xy[1] < 7:
            if buf_xy[0] < 7:
                moves.add((buf_xy[0] + 1, buf_xy[1] + k))
            if buf_xy[0] > 0:
                moves.add((buf_xy[0] - 1, buf_xy[1] + k))

        return moves


class Rook(ChessFigure):
    def __init__(self, color, xy):
        ChessFigure.__init__(self, color, xy)
        self.first_move = True
        if self.color == 'b':
            self.image = pygame.image.load(os.path.join(img_folder, 'bR.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wR.png'))

    def get_moves(self, board, color):
        return set.union(self.get_vertical_move(board, color), self.get_horizontal_move(board, color))


class Bishop(ChessFigure):
    def __init__(self, color, xy):
        ChessFigure.__init__(self, color, xy)
        if self.color == 'b':
            self.image = pygame.image.load(os.path.join(img_folder, 'bB.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wB.png'))

    def get_moves(self, board, color):
        return set.union(self.get_main_diag(board, color), self.get_side_diag(board, color))


class Queen(ChessFigure):
    def __init__(self, color, xy):
        ChessFigure.__init__(self, color, xy)
        if self.color == 'b':
            self.image = pygame.image.load(os.path.join(img_folder, 'bQ.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wQ.png'))

    def get_moves(self, board, color):
        return set.union(self.get_main_diag(board, color), self.get_side_diag(board, color),
                         self.get_horizontal_move(board, color), self.get_vertical_move(board, color))


class Knight(ChessFigure):
    def __init__(self, color, xy):
        ChessFigure.__init__(self, color, xy)
        if self.color == 'b':
            self.image = pygame.image.load(os.path.join(img_folder, 'bN.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wN.png'))

    def get_one_step(self, board, direction, color):
        moves = set()
        i, j = self.xy
        if 0 <= i + direction[0] <= 7 and 0 <= j + direction[1] <= 7 and \
                board[i + direction[0]][j + direction[1]].color != color:
            moves.add((j + direction[1], i + direction[0]))

        if 0 <= i + direction[0] <= 7 and 0 <= j - direction[1] <= 7 and \
                board[i + direction[0]][j - direction[1]].color != color:
            moves.add((j - direction[1], i + direction[0]))

        return moves

    def get_moves(self, board, color):
        moves = set()
        moves = set.union(self.get_one_step(board, (2, 1), color), moves)
        moves = set.union(self.get_one_step(board, (-2, 1), color), moves)
        moves = set.union(self.get_one_step(board, (1, 2), color), moves)
        moves = set.union(self.get_one_step(board, (-1, 2), color), moves)
        return moves


class King(ChessFigure):
    def __init__(self, color, xy):
        ChessFigure.__init__(self, color, xy)
        self.first_move = True
        self.was_checked = False
        if self.color == 'b':
            self.image = pygame.image.load(os.path.join(img_folder, 'bK.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wK.png'))

    def get_moves(self, board, color):
        moves = set()
        for i in range(self.xy[0] - 1, self.xy[0] + 2):
            for j in range(self.xy[1] - 1, self.xy[1] + 2):
                if 0 <= i <= 7 and 0 <= j <= 7 and board[i][j].color != color:
                    moves.add((j, i))
        return moves

    def can_be_castled(self, board):
        right_rook = left_rook = False
        if self.first_move and not self.was_checked:
            y = 0 if self.color == 'b' else 7
            left_rook = board[y][0].first_move
            right_rook = board[y][7].first_move

        return left_rook, right_rook
