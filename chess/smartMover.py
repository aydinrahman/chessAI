import random
import chess


class Player:
    def __init__(self, board, color, time):
        self.color = color
        print(color)
        pass

    def move(self, board, time):
        legalMoves = list(board.legal_moves)
        bestActionList = []
        bestSum = -float('inf')
        # print(board)
        for i in legalMoves:
            board.push(i)
            sum = self.eval(board,time)
            if sum>bestSum:
                bestSum = sum
                bestActionList = [i]
            elif sum == bestSum:
                bestActionList.append(i)
            board.pop()
        return random.choice(bestActionList)
        #     #return self.eval(newBoard,time)
        # return random.choice(list(board.legal_moves))


    def eval(self, board, time):
        if board.is_checkmate():
            return float('inf')
        pieceValues = {'p': 100 ,'n': 320 ,"b": 330, "r": 500, "q": 900, "k":0}
        # print(board.piece_map())
        pieceList = []
        for i in board.piece_map().keys():
            pieceList.append(board.piece_map()[i])
        # print(pieceList)
        sum = 0
        for piece in pieceList:
            if piece.color == self.color:
                sum += pieceValues[str(piece).lower()]
            else:
                sum -= pieceValues[str(piece).lower()]
        # print(sum)

        return sum

