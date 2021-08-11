import pygame
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'Assets')
BROWN = (124, 63, 12)
YELLOW = (203, 191, 42)
WIDTH = 840
HEIGHT = 640
X_AXIS = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}


def chess_xy(string):
    return X_AXIS[string[0]], 8 - int(string[1])


class Colors(object):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class ChessFigure(pygame.sprite.Sprite):
    def __init__(self, color, xy):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = None
        self.first_move = True
        self.xy = (xy[1], xy[0])

    def draw(self, screen_name):
        screen_name.blit(self.image, (self.xy[1] * 80, self.xy[0] * 80))

    def get_vertical_move(self, board):
        moves = []
        i, j = self.xy
        while i > 0 and board[i - 1][j].color == Colors.EMPTY:
            i -= 1
            moves.append((j, i))

        if i != 0 and board[i - 1][j].color != self.color:
            moves.append((j, i - 1))

        i, j = self.xy
        while i < 7 and board[i + 1][j].color == Colors.EMPTY:
            i += 1
            moves.append((j, i))

        if i != 7 and board[i + 1][j].color != self.color:
            moves.append((j, i + 1))

        return moves

    def get_horizontal_move(self, board):
        moves = []
        i, j = self.xy
        while j > 0 and board[i][j - 1].color == Colors.EMPTY:
            j -= 1
            moves.append((j, i))

        if j != 0 and board[i][j - 1].color != self.color:
            moves.append((j - 1, i))

        i, j = self.xy
        while j < 7 and board[i][j + 1].color == Colors.EMPTY:
            j += 1
            moves.append((j, i))

        if j != 7 and board[i][j + 1].color != self.color:
            moves.append((j + 1, i))

        return moves

    def get_main_diag(self, board):
        moves = []
        i, j = self.xy
        while i > 0 and j > 0 and board[i - 1][j - 1].color == Colors.EMPTY:
            i -= 1
            j -= 1
            moves.append((j, i))

        if i != 0 and j != 0 and board[i - 1][j - 1].color != self.color:
            moves.append((j - 1, i - 1))

        i, j = self.xy
        while i < 7 and j < 7 and board[i + 1][j + 1].color == Colors.EMPTY:
            i += 1
            j += 1
            moves.append((j, i))

        if i != 7 and j != 7 and board[i + 1][j + 1].color != self.color:
            moves.append((j + 1, i + 1))

        return moves

    def get_side_diag(self, board):
        moves = []
        i, j = self.xy
        while i > 0 and j < 7 and board[i - 1][j + 1].color == Colors.EMPTY:
            i -= 1
            j += 1
            moves.append((j, i))

        if i != 0 and j != 7 and board[i - 1][j + 1].color != self.color:
            moves.append((j + 1, i - 1))

        i, j = self.xy
        while i < 7 and j > 0 and board[i + 1][j - 1].color == Colors.EMPTY:
            i += 1
            j -= 1
            moves.append((j, i))

        if i != 7 and j != 0 and board[i + 1][j - 1].color != self.color:
            moves.append((j - 1, i + 1))

        return moves



class Pawn(ChessFigure):
    def __init__(self, color, xy):
        ChessFigure.__init__(self, color, xy)
        if self.color == Colors.BLACK:
            self.image = pygame.image.load(os.path.join(img_folder, 'bP.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wP.png'))

    def get_moves(self, board):
        moves = []
        col = Colors.WHITE if self.color == Colors.BLACK else Colors.BLACK
        k = 1 if self.color == Colors.BLACK else -1
        buf_xy = (self.xy[1], self.xy[0])

        if buf_xy[1] < 7:
            if board[buf_xy[1] + k][buf_xy[0]].color == Colors.EMPTY:
                moves.append((buf_xy[0], buf_xy[1] + k))

            if self.first_move and board[buf_xy[1] + k][buf_xy[0]].color == board[buf_xy[1] + 2 * k][buf_xy[0]].color == Colors.EMPTY:
                moves.append((buf_xy[0], buf_xy[1] + 2 * k))

            if buf_xy[0] < 7 and board[buf_xy[1] + k][buf_xy[0] + 1].color == col:
                moves.append((buf_xy[0] + 1, buf_xy[1] + k))

            if buf_xy[0] > 0 and board[buf_xy[1] + k][buf_xy[0] - 1].color == col:
                moves.append((buf_xy[0] - 1, buf_xy[1] + k))

        return moves

class Rook(ChessFigure):
    def __init__(self, color, xy):
        ChessFigure.__init__(self, color, xy)
        if self.color == Colors.BLACK:
            self.image = pygame.image.load(os.path.join(img_folder, 'bR.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wR.png'))

    def get_moves(self, board):
        return self.get_vertical_move(board) + self.get_horizontal_move(board)


class Bishop(ChessFigure):
    def __init__(self, color, xy):
        ChessFigure.__init__(self, color, xy)
        if self.color == Colors.BLACK:
            self.image = pygame.image.load(os.path.join(img_folder, 'bB.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wB.png'))

    def get_moves(self, board):
        return self.get_main_diag(board) + self.get_side_diag(board)

class Queen(ChessFigure):
    def __init__(self, color, xy):
        ChessFigure.__init__(self, color, xy)
        if self.color == Colors.BLACK:
            self.image = pygame.image.load(os.path.join(img_folder, 'bQ.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wQ.png'))

    def get_moves(self, board):
        return (self.get_main_diag(board) + self.get_side_diag(board) +
                self.get_horizontal_move(board) + self.get_vertical_move(board))

class Knight(ChessFigure):
    def __init__(self, color, xy):
        ChessFigure.__init__(self, color, xy)
        if self.color == Colors.BLACK:
            self.image = pygame.image.load(os.path.join(img_folder, 'bN.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wN.png'))

    def get_one_step(self, board, direction):
        moves = []
        i, j = self.xy
        if 0 <= i + direction[0] <= 7 and 0 <= j + direction[1] <= 7 and \
                board[i + direction[0]][j + direction[1]].color != self.color:
            moves.append((j + direction[1], i + direction[0]))

        if 0 <= i + direction[0] <= 7 and 0 <= j - direction[1] <= 7 and \
                board[i + direction[0]][j - direction[1]].color != self.color:
            moves.append((j - direction[1], i + direction[0]))

        return moves

    def get_moves(self, board):
        moves = []
        moves += self.get_one_step(board, (2, 1))
        moves += self.get_one_step(board, (-2, 1))
        moves += self.get_one_step(board, (1, 2))
        moves += self.get_one_step(board, (-1, 2))

        return moves


class King(ChessFigure):
    def __init__(self, color, xy):
        ChessFigure.__init__(self, color, xy)
        if self.color == Colors.BLACK:
            self.image = pygame.image.load(os.path.join(img_folder, 'bK.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wK.png'))

    def get_moves(self, board):
        moves = []
        for i in range(self.xy[0] - 1, self.xy[0] + 2):
            for j in range(self.xy[1] - 1, self.xy[1] + 2):
                if 0 <= i <= 7 and 0 <= j <= 7 and board[i][j].color != self.color:
                    moves.append((j,i))
        return moves


class ChessBoard(object):
    def __init__(self):
        self.board = [[ChessFigure(Colors.EMPTY, (-1, -1))] * 8 for _ in range(8)]
        for i in range(8):
            self.board[1][i] = Pawn(Colors.BLACK, (i, 1))
        self.board[0][0] = Rook(Colors.BLACK, (0, 0))
        self.board[0][7] = Rook(Colors.BLACK, (7, 0))
        self.board[0][2] = Bishop(Colors.BLACK, (2, 0))
        self.board[0][5] = Bishop(Colors.BLACK, (5, 0))
        self.board[0][3] = Queen(Colors.BLACK, (3, 0))
        self.board[0][1] = Knight(Colors.BLACK, (1, 0))
        self.board[0][6] = Knight(Colors.BLACK, (6, 0))
        self.board[0][4] = King(Colors.BLACK, (4, 0))

        for i in range(8):
            self.board[6][i] = Pawn(Colors.WHITE, (i, 6))
        self.board[7][0] = Rook(Colors.WHITE, (0, 7))
        self.board[7][7] = Rook(Colors.WHITE, (7, 7))
        self.board[7][2] = Bishop(Colors.WHITE, (2, 7))
        self.board[7][5] = Bishop(Colors.WHITE, (5, 7))
        self.board[7][3] = Queen(Colors.WHITE, (3, 7))
        self.board[7][1] = Knight(Colors.WHITE, (1, 7))
        self.board[7][6] = Knight(Colors.WHITE, (6, 7))
        self.board[7][4] = King(Colors.WHITE, (4, 7))

    def get_moves(self, xy):
        #if type(self.board[xy[1]][xy[0]]) is not King:
        return self.board[xy[1]][xy[0]].get_moves(self.board)


    def move(self, xy_before, xy_after):
        moves = self.get_moves(xy_before)

        if moves.count(xy_after) > 0:

            if type(self.board[xy_before[1]][xy_before[0]]) == Pawn:
                self.board[xy_before[1]][xy_before[0]].first_move = False


            self.board[xy_after[1]][xy_after[0]] = self.board[xy_before[1]][xy_before[0]]
            self.board[xy_after[1]][xy_after[0]].xy = (xy_after[1], xy_after[0])
            self.board[xy_before[1]][xy_before[0]] = ChessFigure(Colors.EMPTY, (-1, -1))

            return True
        return False

    def check_click(self, pos, figure_color):
        return False if pos[0] >= 8 else self.board[pos[1]][pos[0]].color == figure_color

    def draw_borders(self, screen_name, pos):
        moves = self.board[pos[1]][pos[0]].get_moves(self.board)
        img = pygame.image.load(os.path.join(img_folder, 'border.png'))
        screen_name.blit(img, (pos[0] * 80, pos[1] * 80))
        for pos_moves in moves:
            screen_name.blit(img, (pos_moves[0] * 80, pos_moves[1] * 80))

    def get_color_items(self, color_name):
        result = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].color == color_name:
                    result.append((i, j))
        return result


class Game(object):
    def __init__(self, screen=None):
        pygame.init()
        pygame.mixer.init()
        self.playing_board = ChessBoard()
        self.screen = screen if screen is not None else pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    image = pygame.Surface((80, 80))
                    image.fill(YELLOW)
                    self.screen.blit(image, (i * 80, j * 80))

                else:
                    image = pygame.Surface((80, 80))
                    image.fill(BROWN)
                    self.screen.blit(image, (i * 80, j * 80))

    def draw_figures(self):
        black = self.playing_board.get_color_items(Colors.BLACK)
        white = self.playing_board.get_color_items(Colors.WHITE)
        for item in (black + white):
            self.playing_board.board[item[0]][item[1]].draw(self.screen)

    def start(self):
        self.draw()

        is_screen_clicked = False
        last_click = None

        step = 1
        color = Colors.WHITE

        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.playing_board.check_click(
                            (event.pos[0] // 80, event.pos[1] // 80), color) and not is_screen_clicked:
                        self.draw(event.pos)
                        is_screen_clicked = True
                        last_click = event.pos

                    elif event.button == 1 and is_screen_clicked:
                        if self.playing_board.check_click((event.pos[0] // 80, event.pos[1] // 80), color):
                            self.draw(event.pos)
                            last_click = event.pos

                        elif self.playing_board.move((last_click[0] // 80, last_click[1] // 80),
                                                     (event.pos[0] // 80, event.pos[1] // 80)):
                            step += 1
                            color = Colors.WHITE if color == Colors.BLACK else Colors.BLACK
                            self.draw()
                            is_screen_clicked = False

                    else:
                        self.draw()

        pygame.quit()

    def move(self, string_before, string_after):
        self.playing_board.move(chess_xy(string_before), chess_xy(string_after))

    def draw(self, event=None):
        self.draw_board()
        self.draw_figures()
        if event is not None:
            self.playing_board.draw_borders(self.screen, (event[0] // 80, event[1] // 80))
        pygame.display.update()


Game().start()