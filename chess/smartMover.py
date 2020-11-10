import random
import chess


class Player:
    def __init__(self, board, color, time):
        pass

    def move(self, board, time):
        return self.eval(board,time)
        return random.choice(list(board.legal_moves))


    def eval(self, board, time):
        print(list(board.legal_moves)[0])
        return random.choice(list(board.legal_moves))