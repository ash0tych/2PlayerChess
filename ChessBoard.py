from Figures import *
import copy


# Our class that controls everything
class ChessBoard(object):
    def __init__(self):
        self.board = [[ChessFigure('none', (-1, -1))] * 8 for _ in range(8)]
        self.black_king = (-1, -1)
        self.white_king = (-1, -1)
        self.step = 0
        self.current_color = 'w'

    # Figure initialising
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

    # Resets ALL
    def new_game(self):
        self.figure_init()
        self.step = 1
        self.current_color = 'w'

    # Moves methods

    # Main method to get moves for 1 figure (returns only REAL moves)
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

    # Doing one pseudo move to check for move possibility (u can't move to create check/checkmate for yourself)
    def delete_unreal_moves(self, moves, xy):
        moves_after_deleting = set()
        for move in moves:
            deleted_figure = self.pseudo_move(xy, move)
            if not self.is_king_check(self.current_color):
                moves_after_deleting.add(move)

            self.pseudo_move_back(xy, move, deleted_figure)

        return moves_after_deleting

    # Pseudo move forward. Pseudo moves do not changing situation (zero flags changed)
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

    # Pseudo move back. Used to undo pseudo move. Needed cuz pointers still need to be placed right
    def pseudo_move_back(self, xy_before, xy_after, deleted_figure):
        self.board[xy_before[1]][xy_before[0]] = self.board[xy_after[1]][xy_after[0]]
        self.board[xy_before[1]][xy_before[0]].xy = (xy_before[1], xy_before[0])

        if type(self.board[xy_before[1]][xy_before[0]]) == King:
            if self.board[xy_before[1]][xy_before[0]].color == 'b':
                self.black_king = xy_before
            else:
                self.white_king = xy_before

        self.board[xy_after[1]][xy_after[0]] = deleted_figure

    # Method of moving. It's changing flags, doing castle moves and etc
    def move(self, xy_before, xy_after):
        if type(self.board[xy_before[1]][xy_before[0]]) == King:
            left = self.board[xy_before[1]][xy_before[0]].can_be_castled(self.board)[0]
            right = self.board[xy_before[1]][xy_before[0]].can_be_castled(self.board)[1]
            if self.is_castle_move(xy_after) and left and right:
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

    # Simple pointer swap. Nothing interesting
    def do_normal_move(self, xy_before, xy_after):
        self.board[xy_before[1]][xy_before[0]].first_move = False
        self.board[xy_after[1]][xy_after[0]] = self.board[xy_before[1]][xy_before[0]]

        self.board[xy_after[1]][xy_after[0]].xy = (xy_after[1], xy_after[0])
        self.board[xy_before[1]][xy_before[0]] = ChessFigure('none', (-1, -1))

    # Castle moves
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

    # Creating queen when pawn on the last position
    def pawn_on_last(self, xy):
        self.board[xy[1]][xy[0]] = Queen(self.get_current_color(), xy)

    # Moves gets

    # Full steps for one color. Covering paramether is used to add covering (when u protect self color)
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

    # Get full real steps for color
    def get_full_real_steps(self, color):
        moves = set()
        for item in self.get_color_items(color):
            moves.update(self.get_moves((item[1], item[0])))

        return moves

    # Get possible castle moves
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

    # Info gets

    # Returns king pos (by color)
    def get_king_pos(self, color):
        if color == 'w':
            return self.white_king
        return self.black_king

    # Returns figures xy by color
    def get_color_items(self, color_name):
        result = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].color == color_name:
                    result.append((i, j))
        return result

    # I don't even need to comment this
    def get_current_color(self):
        return self.current_color

    def get_enemy_color(self):
        return 'b' if self.current_color == 'w' else 'w'

    # Other checks (i dont wanna explain obvious things)
    def check_move(self, xy_before, xy_after):
        return xy_after in self.get_moves(xy_before)

    @staticmethod
    def is_castle_move(xy):
        return xy in {(2, 0), (6, 0), (2, 7), (6, 7)}

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

        return set() == self.get_full_real_steps(self.get_current_color()) and self.is_king_check(color)

    def is_king_stalemate(self, color):
        return self.get_full_real_steps(self.get_current_color()) == set() and not self.is_king_check(color)

    def check_for_current_check(self):
        if self.is_king_checkmate(self.get_current_color()):
            king = 2
        elif self.is_king_check(self.get_current_color()):
            king = 1
        elif self.is_king_stalemate(self.get_current_color()):
            king = 3
        else:
            king = 0
        return king

    @staticmethod
    def is_pawn_on_last(xy):
        return xy[1] == 0 or xy[1] == 7

    # Game step
    def do_the_game_step(self, xy_before, xy_after):
        tuple_1 = self.return_figure_info(xy_before)
        tuple_2 = self.return_figure_info(xy_after)

        self.move(xy_before, xy_after)

        self.step += 1
        self.current_color = self.get_enemy_color()

        new_king_pos = self.get_king_pos(self.current_color)
        if self.is_king_check(self.current_color):
            self.board[new_king_pos[1]][new_king_pos[0]].was_checked = True

        king = self.check_for_current_check()

        return tuple_1, tuple_2, king

    # Used for info logging
    def return_figure_info(self, xy):
        color = self.board[xy[1]][xy[0]].color
        name = type(self.board[xy[1]][xy[0]])
        image = copy.copy(self.board[xy[1]][xy[0]].image)
        return xy, color, name, image
