import pygame
import os

from ChessBoard import ChessBoard
from LogInfo import LogInfo

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'Assets')
WIDTH = 840
HEIGHT = 640


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

                    if event.button == 1 and self.playing_board.check_click(converted_event_pos, current_color) and \
                            not is_screen_clicked:
                        self.draw(event.pos)
                        is_screen_clicked = True
                        last_click = event.pos

                    elif event.button == 1 and is_screen_clicked:
                        if self.playing_board.check_click(converted_event_pos, current_color):
                            self.draw(event.pos)
                            last_click = event.pos

                        elif self.playing_board.check_move(converted_last_pos, converted_event_pos):
                            tuple_1, tuple_2, king = self.playing_board.do_the_game_step(converted_last_pos,
                                                                                         converted_event_pos)
                            self.save_log_info(tuple_1, tuple_2, king)
                            self.draw()
                            is_screen_clicked = False

                        else:
                            self.draw()

                    else:
                        self.draw()

                if self.playing_board.check_for_current_check() >= 2:
                    running = False

        last_view = True
        while last_view:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    last_view = False

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
                self.draw_step(self.log[i].first_figure_tuple, self.log[i].second_figure_tuple, self.log[i].check,
                               i - bias)

    def draw_step(self, tuple_1, tuple_2, check, y):
        pos1, _, _, image1 = tuple_1
        pos2, _, _, image2 = tuple_2
        arrow = pygame.image.load(os.path.join(img_folder, 'arrow.png'))
        self.screen.blit(pygame.transform.scale(image1, (30, 30)), (695, 90 + y * 30))
        if image2 is not None:
            self.screen.blit(pygame.transform.scale(image2, (30, 30)), (785, 90 + y * 30))

        self.screen.blit(arrow, (725, 97 + y * 30))

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

    @staticmethod
    def chess_xy(xy):
        x_axis = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return x_axis[xy[0]] + str(8 - xy[1])

    def save_log_info(self, tuple_1, tuple_2, king):
        log_component = LogInfo(self.playing_board.step, tuple_1, tuple_2, king)
        self.log.append(log_component)


Game().start()
