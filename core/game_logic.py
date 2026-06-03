import copy

class GameLogic:
    def __init__(self, size=3):
        self.size = size
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'
        self.history = []
        self.winner = None
        self.winning_line = None

    def reset_game(self):
        self.board = [['' for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 'X'
        self.history = []
        self.winner = None
        self.winning_line = None

    def change_size(self, size):
        self.size = size
        self.reset_game()

    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.winner:
            self.history.append(copy.deepcopy(self.board))
            self.board[row][col] = self.current_player
            self.check_winner()
            if not self.winner:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def undo_move(self):
        if self.history:
            self.board = self.history.pop()
            self.winner = None
            self.winning_line = None
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        # Check rows
        for i in range(self.size):
            if all(self.board[i][j] == self.current_player for j in range(self.size)):
                self.winner = self.current_player
                self.winning_line = [(i, j) for j in range(self.size)]
                return

        # Check columns
        for j in range(self.size):
            if all(self.board[i][j] == self.current_player for i in range(self.size)):
                self.winner = self.current_player
                self.winning_line = [(i, j) for i in range(self.size)]
                return

        # Check diagonals
        if all(self.board[i][i] == self.current_player for i in range(self.size)):
            self.winner = self.current_player
            self.winning_line = [(i, i) for i in range(self.size)]
            return

        if all(self.board[i][self.size - 1 - i] == self.current_player for i in range(self.size)):
            self.winner = self.current_player
            self.winning_line = [(i, self.size - 1 - i) for i in range(self.size)]
            return

        # Check Draw
        if self.is_draw():
            self.winner = 'Draw'

    def is_draw(self):
        for row in self.board:
            if '' in row:
                return False
        return True

    def get_available_moves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == '':
                    moves.append((i, j))
        return moves
