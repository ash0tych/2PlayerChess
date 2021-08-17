import pygame
import os
import copy
import sys


game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'Assets')
BROWN = (124, 63, 12)
YELLOW = (203, 191, 42)
WIDTH = 840
HEIGHT = 640


class Log_info(object):
    def __init__(self, step, tuple_1, tuple_2, check):
        self.step = step
        self.first_figure_tuple = tuple_1
        self.second_figure_tuple = tuple_2
        self.check = check


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
        self.can_take_on_asile = False
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


class ChessBoard(object):
    def __init__(self):
        self.board = [[ChessFigure('none', (-1, -1))] * 8 for _ in range(8)]
        self.black_king = (-1, -1)
        self.white_king = (-1, -1)
        self.step = 0
        self.current_color = 'w'

    def figure_init(self):
        for i in range(8):
            self.board[1][i] = Pawn('b', (i, 1))
        self.board[0][0] = Rook('b', (0, 0))
        self.board[0][7] = Rook('b', (7, 0))
        self.board[0][2] = Bishop('b', (2, 0))
        self.board[0][5] = Bishop('b', (5, 0))
        self.board[0][3] = Queen('b', (3, 0))
        self.board[0][1] = Knight('b', (1, 0))
        self.board[0][6] = Knight('b', (6, 0))
        self.board[0][4] = King('b', (4, 0))
        self.black_king = (4, 0)

        for i in range(8):
            self.board[6][i] = Pawn('w', (i, 6))
        self.board[7][0] = Rook('w', (0, 7))
        self.board[7][7] = Rook('w', (7, 7))
        self.board[7][2] = Bishop('w', (2, 7))
        self.board[7][5] = Bishop('w', (5, 7))
        self.board[7][3] = Queen('w', (3, 7))
        self.board[7][1] = Knight('w', (1, 7))
        self.board[7][6] = Knight('w', (6, 7))
        self.board[7][4] = King('w', (4, 7))
        self.white_king = (4, 7)

    def new_game(self):
        self.step = 1
        self.current_color = 'w'

    def get_moves(self, xy):
        if type(self.board[xy[1]][xy[0]]) is not King:
            moves_before_deleting = self.board[xy[1]][xy[0]].get_moves(self.board, self.board[xy[1]][xy[0]].color)

        else:
            king_moves = self.board[xy[1]][xy[0]].get_moves(self.board, self.board[xy[1]][xy[0]].color)
            covering_enemy_moves = self.get_color_steps(self.get_enemy_color(), covering=True)
            moves_before_deleting = king_moves.difference(covering_enemy_moves)

            castle_moves = self.get_castle_moves(xy)
            moves_before_deleting.update(castle_moves)

        moves = self.delete_unreal_moves(moves_before_deleting, xy)
        return moves

    def check_move(self, xy_before, xy_after):
        return xy_after in self.get_moves(xy_before)

    def delete_unreal_moves(self, moves, xy):
        moves_after_deleting = set()
        for move in moves:
            deleted_figure = self.pseudo_move(xy, move)
            if not self.is_king_check(self.current_color):
                moves_after_deleting.add(move)

            self.pseudo_move_back(xy, move, deleted_figure)

        return moves_after_deleting

    def move(self, xy_before, xy_after):
        if type(self.board[xy_before[1]][xy_before[0]]) == King:
            if self.is_castle_move(xy_after) and self.board[xy_before[1]][xy_before[0]].can_be_castled(self.board):
                self.do_castle_move(xy_after)

            else:
                self.do_normal_move(xy_before, xy_after)

            if self.current_color == 'b':
                self.black_king = xy_after
            else:
                self.white_king = xy_after

        elif type(self.board[xy_before[1]][xy_before[0]]) == Pawn and self.is_pawn_on_last(xy_after):
            self.do_normal_move(xy_before, xy_after)
            self.pawn_on_last(xy_after)

        else:
            self.do_normal_move(xy_before, xy_after)

    @staticmethod
    def is_castle_move(xy):
        return xy in {(2, 0), (6, 0), (2, 7), (6, 7)}

    def do_castle_move(self, xy):
        if xy[0] < 4:
            rook_before = 0
            rook_after = 3
            king_after = 2
        else:
            rook_before = 7
            rook_after = 5
            king_after = 6

        self.do_normal_move((rook_before, xy[1]), (rook_after, xy[1]))
        self.do_normal_move((4, xy[1]), (king_after, xy[1]))

    def do_normal_move(self, xy_before, xy_after):
        self.board[xy_before[1]][xy_before[0]].first_move = False
        self.board[xy_after[1]][xy_after[0]] = self.board[xy_before[1]][xy_before[0]]

        self.board[xy_after[1]][xy_after[0]].xy = (xy_after[1], xy_after[0])
        self.board[xy_before[1]][xy_before[0]] = ChessFigure('none', (-1, -1))

    def pseudo_move(self, xy_before, xy_after):
        deleted_figure = copy.copy(self.board[xy_after[1]][xy_after[0]])
        self.board[xy_after[1]][xy_after[0]] = self.board[xy_before[1]][xy_before[0]]

        if type(self.board[xy_after[1]][xy_after[0]]) == King:
            if self.board[xy_after[1]][xy_after[0]].color == 'b':
                self.black_king = xy_after
            else:
                self.white_king = xy_after

        self.board[xy_after[1]][xy_after[0]].xy = (xy_after[1], xy_after[0])
        self.board[xy_before[1]][xy_before[0]] = ChessFigure('none', (-1, -1))
        return deleted_figure

    def pseudo_move_back(self, xy_before, xy_after, deleted_figure):
        self.board[xy_before[1]][xy_before[0]] = self.board[xy_after[1]][xy_after[0]]
        self.board[xy_before[1]][xy_before[0]].xy = (xy_before[1], xy_before[0])

        if type(self.board[xy_before[1]][xy_before[0]]) == King:
            if self.board[xy_before[1]][xy_before[0]].color == 'b':
                self.black_king = xy_before
            else:
                self.white_king = xy_before

        self.board[xy_after[1]][xy_after[0]] = deleted_figure

    def check_click(self, pos, color):
        return False if pos[0] >= 8 else self.board[pos[1]][pos[0]].color == color

    def is_king_check(self, color):
        enemy_color = self.get_enemy_color()
        pos = self.get_king_pos(color)
        enemy_steps = self.get_color_steps(enemy_color)
        if pos in enemy_steps:
            return True

        return False

    def is_king_checkmate(self, color):

        return set() == self.get_full_real_steps() and self.is_king_check(color)

    def is_king_stalemate(self, color):
        return self.get_color_steps(color) == set() and not self.is_king_check(color)


    def get_king_pos(self, color):
        if color == 'w':
            return self.white_king
        return self.black_king

    def get_color_items(self, color_name):
        result = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].color == color_name:
                    result.append((i, j))
        return result

    def get_color_steps(self, color_name, covering=False):
        moves = set()
        colored_items = self.get_color_items(color_name)
        if covering:
            reverse_color = self.get_enemy_color()
        else:
            reverse_color = color_name

        for item in colored_items:
            if type(self.board[item[0]][item[1]]) == Pawn:
                buf_set = set(self.board[item[0]][item[1]].get_possible_pawn_diag_moves())
            else:
                buf_set = set(self.board[item[0]][item[1]].get_moves(self.board, reverse_color))

            moves.update(buf_set)

        return moves

    def get_full_real_steps(self):
        moves = set()
        for item in self.get_color_items(self.get_current_color()):
            moves.update(self.get_moves((item[1], item[0])))

        return moves

    def get_castle_moves(self, xy):
        castle_moves = set()
        left, right = self.board[xy[1]][xy[0]].can_be_castled(self.board)
        full_enemy_steps = self.get_color_steps(self.get_enemy_color())
        if left and len(self.board[xy[1]][0].get_horizontal_move(self.board, self.get_enemy_color())) == 4:
            if (2, xy[1]) not in full_enemy_steps and (3, xy[1]) not in full_enemy_steps:
                castle_moves.add((2, xy[1]))

        if right and len(self.board[xy[1]][7].get_horizontal_move(self.board, self.get_enemy_color())) == 3:
            if (6, xy[1]) not in full_enemy_steps and (5, xy[1]) not in full_enemy_steps:
                castle_moves.add((6, xy[1]))

        return castle_moves

    def get_current_color(self):
        return self.current_color

    def get_enemy_color(self):
        return 'b' if self.current_color == 'w' else 'w'

    def do_the_game_step(self, xy_before, xy_after):
        tuple_1 = self.return_figure_info(xy_before)
        tuple_2 = self.return_figure_info(xy_after)

        self.move(xy_before, xy_after)

        self.step += 1
        self.current_color = self.get_enemy_color()

        new_king_pos = self.get_king_pos(self.current_color)
        if self.is_king_check(self.current_color):
            self.board[new_king_pos[1]][new_king_pos[0]].was_checked = True

        if self.is_king_checkmate(self.get_current_color()):
            king = 2
        elif self.is_king_check(self.get_current_color()):
            king = 1
        elif self.is_king_stalemate(self.get_current_color()):
            king = 3
        else:
            king = 0

        return tuple_1, tuple_2, king



    def is_pawn_on_last(self, xy):
        return xy[1] == 0 or xy[1] == 7

    def pawn_on_last(self, xy):
        self.board[xy[1]][xy[0]] = Queen(self.get_current_color(), xy)

    def return_figure_info(self, xy):
        pos = xy
        color = self.board[xy[1]][xy[0]].color
        name = type(self.board[xy[1]][xy[0]])
        image = copy.copy(self.board[xy[1]][xy[0]].image)
        return (pos, color, name, image)


class Game(object):
    def __init__(self, screen=None):
        pygame.init()
        pygame.mixer.init()
        self.playing_board = ChessBoard()
        self.playing_board.figure_init()
        self.screen = screen if screen is not None else pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('segoe', 40)
        self.menu_img = pygame.image.load(os.path.join(img_folder, 'menu.png'))
        self.board_img = pygame.image.load(os.path.join(img_folder, 'chess_board.png'))
        self.upper_border_img = pygame.image.load(os.path.join(img_folder, 'upper_border.png'))
        self.lower_border_img = pygame.image.load(os.path.join(img_folder, 'lower_border.png'))
        self.log = []


    def draw_board(self):
        self.screen.blit(self.board_img, (0, 0))

    def draw_figures(self):
        black = self.playing_board.get_color_items('b')
        white = self.playing_board.get_color_items('w')
        for item in (black + white):
            image = self.playing_board.board[item[0]][item[1]].get_image()
            self.screen.blit(image, (item[1] * 80, item[0] * 80))

    def start(self):
        self.draw()

        is_screen_clicked = False
        last_click = None

        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_color = self.playing_board.get_current_color()
                    converted_event_pos = (event.pos[0] // 80, event.pos[1] // 80)
                    converted_last_pos = (last_click[0] // 80, last_click[1] // 80) if last_click is not None else None

                    if event.button == 1 and self.playing_board.check_click(converted_event_pos, current_color) and\
                            not is_screen_clicked:
                        self.draw(event.pos)
                        is_screen_clicked = True
                        last_click = event.pos

                    elif event.button == 1 and is_screen_clicked:
                        if self.playing_board.check_click(converted_event_pos, current_color):
                            self.draw(event.pos)
                            last_click = event.pos

                        elif self.playing_board.check_move(converted_last_pos, converted_event_pos):
                            tuple_1, tuple_2, king = self.playing_board.do_the_game_step(converted_last_pos, converted_event_pos)
                            self.save_log_info(tuple_1, tuple_2, king)
                            self.draw()
                            is_screen_clicked = False

                        else:
                            self.draw()

                    else:
                        self.draw()

        pygame.quit()

    def move(self, string_before, string_after):
        self.playing_board.move(chess_xy(string_before), chess_xy(string_after))

    def draw(self, event=None):
        self.draw_board()
        self.draw_figures()
        self.draw_menu()
        self.show_current_color()
        self.draw_log()

        if event is not None:
            self.draw_borders((event[0] // 80, event[1] // 80))

        if self.playing_board.is_king_checkmate(self.playing_board.get_current_color()):
            pos = self.playing_board.get_king_pos(self.playing_board.get_current_color())
            img = pygame.image.load(os.path.join(img_folder, 'checkmate_border.png'))
            self.screen.blit(img, (pos[0] * 80, pos[1] * 80))

        elif self.playing_board.is_king_check(self.playing_board.get_current_color()):
            pos = self.playing_board.get_king_pos(self.playing_board.get_current_color())
            img = pygame.image.load(os.path.join(img_folder, 'check_border.png'))
            self.screen.blit(img, (pos[0] * 80, pos[1] * 80))

        elif self.playing_board.is_king_stalemate(self.playing_board.get_current_color()):
            pos = self.playing_board.get_king_pos(self.playing_board.get_current_color())
            img = pygame.image.load(os.path.join(img_folder, 'stalemate_border.png'))
            self.screen.blit(img, (pos[0] * 80, pos[1] * 80))

        pygame.display.update()

    def draw_borders(self, pos):
        moves = self.playing_board.get_moves(pos)
        img = pygame.image.load(os.path.join(img_folder, 'border.png'))
        self.screen.blit(img, (pos[0] * 80, pos[1] * 80))
        for pos_moves in moves:
            self.screen.blit(img, (pos_moves[0] * 80, pos_moves[1] * 80))

    def draw_menu(self):
        self.screen.blit(self.menu_img, (640, 0))
        
    def show_current_color(self):
        if self.playing_board.get_current_color() == 'b':
            self.screen.blit(self.upper_border_img, (640, 0))
        else:
            self.screen.blit(self.lower_border_img, (640, 0))

    def draw_log(self):
        size = len(self.log)
        if size <= 15:
            for i in range(size):
                self.draw_step(self.log[i].first_figure_tuple, self.log[i].second_figure_tuple, self.log[i].check, i)
        else:
            bias = size - 15
            for i in range(bias, size):
                self.draw_step(self.log[i].first_figure_tuple, self.log[i].second_figure_tuple, self.log[i].check, i - bias)


    def draw_step(self, tuple_1, tuple_2, check, y):
        pos1, _, _, image1 = tuple_1
        pos2, _, _, image2 = tuple_2

        self.screen.blit(pygame.transform.scale(image1, (30, 30)), (695, 90 + y * 30))
        if image2 is not None:
            self.screen.blit(pygame.transform.scale(image2, (30, 30)), (785, 90 + y * 30))

        self.screen.blit(self.font.render(self.chess_xy(pos1), True, (0, 0, 0)), (665, 95 + y * 30))
        self.screen.blit(self.font.render(self.chess_xy(pos2), True, (0, 0, 0)), (755, 95 + y * 30))

        if check == 1:
            img = pygame.image.load(os.path.join(img_folder, 'check_log.png'))
            self.screen.blit(img, (660, 90 + y * 30))
        elif check == 2:
            img = pygame.image.load(os.path.join(img_folder, 'checkmate_log.png'))
            self.screen.blit(img, (660, 90 + y * 30))
        elif check == 3:
            img = pygame.image.load(os.path.join(img_folder, 'stalemate_log.png'))
            self.screen.blit(img, (660, 90 + y * 30))

    def chess_xy(self, xy):
        x_axis = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return x_axis[xy[0]] + str(8 - xy[1])

    def save_log_info(self, tuple_1, tuple_2, king):
        log_component = Log_info(self.playing_board.step, tuple_1, tuple_2, king)
        self.log.append(log_component)


Game().start()
