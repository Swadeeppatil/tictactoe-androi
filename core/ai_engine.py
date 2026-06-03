import random
import copy

class AIEngine:
    def __init__(self, difficulty='expert'):
        self.difficulty = difficulty

    def get_best_move(self, board_state, current_player):
        size = len(board_state)
        available_moves = []
        for i in range(size):
            for j in range(size):
                if board_state[i][j] == '':
                    available_moves.append((i, j))

        if not available_moves:
            return None

        if self.difficulty == 'easy':
            return random.choice(available_moves)

        elif self.difficulty == 'medium':
            # 50% chance to play optimal, 50% random
            if random.random() < 0.5:
                return random.choice(available_moves)
            else:
                return self.get_blocking_or_winning_move(board_state, current_player, available_moves)

        elif self.difficulty == 'hard':
            # Block or Win, else random
            move = self.get_blocking_or_winning_move(board_state, current_player, available_moves)
            return move if move else random.choice(available_moves)

        elif self.difficulty in ['expert', 'impossible']:
            if size > 3:
                # Minimax is too slow for 4x4 or 5x5 full board. Use heuristcs or shallow minimax
                move = self.get_blocking_or_winning_move(board_state, current_player, available_moves)
                return move if move else random.choice(available_moves)

            # Use Minimax with Alpha-Beta Pruning for 3x3
            best_val = -float('inf')
            best_move = None
            alpha = -float('inf')
            beta = float('inf')

            for move in available_moves:
                board_copy = copy.deepcopy(board_state)
                board_copy[move[0]][move[1]] = current_player
                move_val = self.minimax(board_copy, 0, False, current_player, alpha, beta)
                
                if move_val > best_val:
                    best_move = move
                    best_val = move_val
                alpha = max(alpha, best_val)

            return best_move if best_move else random.choice(available_moves)

    def get_blocking_or_winning_move(self, board, player, available_moves):
        opponent = 'O' if player == 'X' else 'X'
        
        # 1. Check for winning move
        for move in available_moves:
            board_copy = copy.deepcopy(board)
            board_copy[move[0]][move[1]] = player
            if self.check_win(board_copy, player):
                return move

        # 2. Check for blocking move
        for move in available_moves:
            board_copy = copy.deepcopy(board)
            board_copy[move[0]][move[1]] = opponent
            if self.check_win(board_copy, opponent):
                return move
                
        return None

    def minimax(self, board, depth, is_max, player, alpha, beta):
        opponent = 'O' if player == 'X' else 'X'
        
        if self.check_win(board, player):
            return 10 - depth
        if self.check_win(board, opponent):
            return -10 + depth
        if self.is_draw(board):
            return 0

        size = len(board)
        if is_max:
            best = -float('inf')
            for i in range(size):
                for j in range(size):
                    if board[i][j] == '':
                        board[i][j] = player
                        val = self.minimax(board, depth + 1, not is_max, player, alpha, beta)
                        board[i][j] = ''
                        best = max(best, val)
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break
            return best
        else:
            best = float('inf')
            for i in range(size):
                for j in range(size):
                    if board[i][j] == '':
                        board[i][j] = opponent
                        val = self.minimax(board, depth + 1, not is_max, player, alpha, beta)
                        board[i][j] = ''
                        best = min(best, val)
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
            return best

    def check_win(self, board, player):
        size = len(board)
        # Check rows
        for i in range(size):
            if all(board[i][j] == player for j in range(size)):
                return True
        # Check cols
        for j in range(size):
            if all(board[i][j] == player for i in range(size)):
                return True
        # Diagonals
        if all(board[i][i] == player for i in range(size)):
            return True
        if all(board[i][size - 1 - i] == player for i in range(size)):
            return True
        return False

    def is_draw(self, board):
        for row in board:
            if '' in row:
                return False
        return True
