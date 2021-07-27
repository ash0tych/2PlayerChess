import pygame
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'Assets')
BROWN = (124, 63, 12)
YELLOW = (203, 191, 42)
WIDTH = 640
HEIGHT = 640


class Colors(object):
    EMPTY = 0
    BLACK = 1
    WHITE = 2


class ChessFigure(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = None
        self.rect = None


class Pawn(ChessFigure):
    def get_moves(self, board, xy):
        moves = []
        if self.color == Colors.BLACK and xy[1] < 7:
            if board[xy[1] + 1][xy[0]].color == Colors.EMPTY:
                moves.append((xy[0], xy[1] + 1))
            if xy[0] < 7 and board[xy[1] + 1][xy[0] + 1].color == Colors.WHITE:
                moves.append((xy[0] + 1, xy[1] + 1))
            if xy[0] > 0 and board[xy[1] + 1][xy[0] - 1].color == Colors.WHITE:
                moves.append((xy[0] - 1, xy[1] + 1))

        if self.color == Colors.WHITE and xy[1] > 0:
            if board[xy[1] - 1][xy[0]].color == Colors.EMPTY:
                moves.append((xy[0], xy[1] - 1))
            if xy[0] < 7 and board[xy[1] - 1][xy[0] - 1].color == Colors.BLACK:
                moves.append((xy[0] - 1, xy[1] - 1))
            if xy[0] > 0 and board[xy[1] - 1][xy[0] + 1].color == Colors.BLACK:
                moves.append((xy[0] + 1, xy[1] - 1))
        return moves

    def draw(self, screen_name, xy):
        if self.image is None:
            if self.color == Colors.BLACK:
                self.image = pygame.image.load(os.path.join(img_folder, 'bP.png'))
            else:
                self.image = pygame.image.load(os.path.join(img_folder, 'wP.png'))

        self.rect = self.image.get_rect()
        self.rect.topleft = (xy[1] * 80, xy[0] * 80)
        screen_name.blit(self.image, self.rect)

    def clicked(self, screen_name, board, xy):
        moves = self.get_moves(board, (xy[0], xy[1]))
        for pos in moves:
            img = pygame.image.load(os.path.join(img_folder, 'border.png'))
            rect = img.get_rect()
            rect.topleft = (pos[0] * 80, pos[1] * 80)
            screen_name.blit(img, rect)


class ChessBoard(object):
    def __init__(self):
        self.board = [[ChessFigure(Colors.EMPTY)] * 8 for _ in range(8)]
        self.board[1][0] = Pawn(Colors.BLACK)
        self.board[7][1] = Pawn(Colors.WHITE)

    def __str__(self):
        result = '  a b c d e f g h\n'

        for i in range(8):
            result += '{} '.format(8 - i) + ''.join(map(str, self.board[i])) + '\n'
        return result

    def get_moves(self, xy):
        return self.board[xy[1]][xy[0]].get_moves(self.board, xy)

    def move(self, xy_before, xy_after):
        moves = self.get_moves(xy_before)
        if moves.count(xy_after) > 0:
            self.board[xy_after[1]][xy_after[0]] = self.board[xy_before[1]][xy_before[0]]
            self.board[xy_before[1]][xy_before[0]] = ChessFigure(Colors.EMPTY)

    def check_click(self, pos):
        return self.board[pos[1]][pos[0]].color != Colors.EMPTY

    def draw_borders(self, screen_name, pos):
        self.board[pos[1]][pos[0]].clicked(screen_name, self.board, pos)


class Game(object):
    def __init__(self, screen = None):
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
                    rect = image.get_rect()
                    rect.topleft = (i * 80, j * 80)
                    self.screen.blit(image, rect)

                else:
                    image = pygame.Surface((80, 80))
                    image.fill(BROWN)
                    rect = image.get_rect()
                    rect.topleft = (i * 80, j * 80)
                    self.screen.blit(image, rect)

                if self.playing_board.board[i][j].color != Colors.EMPTY:
                    self.playing_board.board[i][j].draw(self.screen, (i, j))

    def start(self):
        self.draw_board()
        pygame.display.update()
        is_screen_clicked = False
        last_click = None
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.playing_board.check_click(
                            (event.pos[0] // 80, event.pos[1] // 80)) and is_screen_clicked == False:
                        self.draw_board()
                        self.playing_board.draw_borders(self.screen, (event.pos[0] // 80, event.pos[1] // 80))
                        pygame.display.update()
                        is_screen_clicked = True
                        last_click = event.pos

                    elif event.button == 1 and is_screen_clicked:
                        self.playing_board.move((last_click[0] // 80, last_click[1] // 80),
                                     (event.pos[0] // 80, event.pos[1] // 80))
                        self.draw_board()
                        pygame.display.update()
                        is_screen_clicked = False

                    else:
                        self.draw_board()
                        pygame.display.update()
        pygame.quit()

Game().start()