import pygame
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'Assets')
BROWN = (124, 63, 12)
YELLOW = (203, 191, 42)
WIDTH = 640
HEIGHT = 640
X_AXIS = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}


def chess_xy(string):
    return X_AXIS[string[0]], 8 - int(string[1])


class Colors(object):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class ChessFigure(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = None

    def draw(self, screen_name, xy):
        screen_name.blit(self.image, (xy[1] * 80, xy[0] * 80))


class Pawn(ChessFigure):
    def __init__(self, color):
        ChessFigure.__init__(self, color)
        if self.color == Colors.BLACK:
            self.image = pygame.image.load(os.path.join(img_folder, 'bP.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wP.png'))

    def get_moves(self, board, xy):
        return self.get_moves_black(board, xy) if self.color == Colors.BLACK else self.get_moves_white(board, xy)

    @staticmethod
    def get_moves_black(board, xy):
        moves = []
        if xy[1] < 7:
            if board[xy[1] + 1][xy[0]].color == Colors.EMPTY:
                moves.append((xy[0], xy[1] + 1))
            if xy[0] < 7 and board[xy[1] + 1][xy[0] + 1].color == Colors.WHITE:
                moves.append((xy[0] + 1, xy[1] + 1))
            if xy[0] > 0 and board[xy[1] + 1][xy[0] - 1].color == Colors.WHITE:
                moves.append((xy[0] - 1, xy[1] + 1))
        return moves

    @staticmethod
    def get_moves_white(board, xy):
        moves = []
        if xy[1] > 0:
            if board[xy[1] - 1][xy[0]].color == Colors.EMPTY:
                moves.append((xy[0], xy[1] - 1))
            if xy[0] < 7 and board[xy[1] - 1][xy[0] - 1].color == Colors.BLACK:
                moves.append((xy[0] - 1, xy[1] - 1))
            if xy[0] > 0 and board[xy[1] - 1][xy[0] + 1].color == Colors.BLACK:
                moves.append((xy[0] + 1, xy[1] - 1))
        return moves

    def clicked(self, screen_name, board, xy):
        moves = self.get_moves(board, (xy[0], xy[1]))
        for pos in moves:
            img = pygame.image.load(os.path.join(img_folder, 'border.png'))
            screen_name.blit(img, (pos[0] * 80, pos[1] * 80))


class Rook(ChessFigure):
    def __init__(self, color):
        ChessFigure.__init__(self, color)
        if self.color == Colors.BLACK:
            self.image = pygame.image.load(os.path.join(img_folder, 'bR.png'))
        else:
            self.image = pygame.image.load(os.path.join(img_folder, 'wR.png'))

    def get_moves(self, board, xy):
        return self.get_moves_black(board, xy) if self.color == Colors.BLACK else self.get_moves_white(board, xy)


    def get_moves_black(self, board, xy):
        moves = []
        # Vertical line
        i, j = xy[1], xy[0]
        while i > 0 and board[i - 1][j].color == Colors.EMPTY:
            i -= 1
            moves.append((j, i))

        if i != 0 and board[i - 1][j].color != self.color:
            moves.append((j, i - 1))

        i, j = xy[1], xy[0]
        while i < 7 and board[i + 1][j].color == Colors.EMPTY:
            i += 1
            moves.append((j, i))

        if i != 7 and board[i + 1][j].color != self.color:
            moves.append((j, i + 1))

        # Horisontal line
        i, j = xy[1], xy[0]
        while j > 0 and board[i][j - 1].color == Colors.EMPTY:
            j -= 1
            moves.append((j, i))

        if j != 0 and board[i][j - 1].color != self.color:
            moves.append((j - 1, i))

        i, j = xy[1], xy[0]
        while j < 7 and board[i][j + 1].color == Colors.EMPTY:
            j += 1
            moves.append((j, i))

        if j != 7 and board[i][j + 1].color != self.color:
            moves.append((j + 1, i))

        return moves

    def get_moves_white(self, board, xy):
        moves = []
        if xy[1] > 0:
            if board[xy[1] - 1][xy[0]].color == Colors.EMPTY:
                moves.append((xy[0], xy[1] - 1))
            if xy[0] < 7 and board[xy[1] - 1][xy[0] - 1].color == Colors.BLACK:
                moves.append((xy[0] - 1, xy[1] - 1))
            if xy[0] > 0 and board[xy[1] - 1][xy[0] + 1].color == Colors.BLACK:
                moves.append((xy[0] + 1, xy[1] - 1))
        return moves

    def clicked(self, screen_name, board, xy):
        moves = self.get_moves(board, (xy[0], xy[1]))
        for pos in moves:
            img = pygame.image.load(os.path.join(img_folder, 'border.png'))
            screen_name.blit(img, (pos[0] * 80, pos[1] * 80))


class ChessBoard(object):
    def __init__(self):
        self.board = [[ChessFigure(Colors.EMPTY)] * 8 for _ in range(8)]
        self.board[1][0] = Pawn(Colors.BLACK)
        self.board[1][1] = Pawn(Colors.BLACK)
        self.board[1][2] = Pawn(Colors.BLACK)
        self.board[1][3] = Pawn(Colors.BLACK)

        self.board[5][2] = Rook(Colors.BLACK)
        self.board[6][3] = Pawn(Colors.WHITE)
        self.board[6][4] = Pawn(Colors.WHITE)
        self.board[6][5] = Pawn(Colors.WHITE)

    def get_moves(self, xy):
        return self.board[xy[1]][xy[0]].get_moves(self.board, xy)

    def move(self, xy_before, xy_after):
        moves = self.get_moves(xy_before)
        if moves.count(xy_after) > 0:
            self.board[xy_after[1]][xy_after[0]] = self.board[xy_before[1]][xy_before[0]]
            self.board[xy_before[1]][xy_before[0]] = ChessFigure(Colors.EMPTY)
            return True
        return False

    def check_click(self, pos, figure_color):
        return self.board[pos[1]][pos[0]].color == figure_color

    def draw_borders(self, screen_name, pos):
        self.board[pos[1]][pos[0]].clicked(screen_name, self.board, pos)

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
            self.playing_board.board[item[0]][item[1]].draw(self.screen, item)

    def start(self):
        self.draw_board()
        self.draw_figures()
        pygame.display.update()

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
                        self.draw_board()
                        self.draw_figures()
                        self.playing_board.draw_borders(self.screen, (event.pos[0] // 80, event.pos[1] // 80))
                        pygame.display.update()
                        is_screen_clicked = True
                        last_click = event.pos

                    elif event.button == 1 and is_screen_clicked:
                        if self.playing_board.move((last_click[0] // 80, last_click[1] // 80),
                                                   (event.pos[0] // 80, event.pos[1] // 80)):
                            step += 1
                            color = Colors.WHITE if color == Colors.BLACK else Colors.BLACK
                        self.draw_board()
                        self.draw_figures()
                        pygame.display.update()
                        is_screen_clicked = False

                    else:
                        self.draw_board()
                        self.draw_figures()
                        pygame.display.update()
        pygame.quit()

    def move(self, string_before, string_after):
        self.playing_board.move(chess_xy(string_before), chess_xy(string_after))


Game().start()
