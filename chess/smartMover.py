import random
import chess


class Player:
    def __init__(self, board, color, time):
        self.color = color
        self.depth = 2
        print(color)
        self.pieceValues = {'p': 100, 'n': 320, "b": 330, "r": 500, "q": 900, "k": 0}
        pass

    # def move(self, board, time):
    #     legalMoves = list(board.legal_moves)
    #     bestActionList = []
    #     bestSum = -float('inf')
    #     # print(board)
    #     for i in legalMoves:
    #         board.push(i)
    #         sum = self.eval(board,time)
    #         if sum>bestSum:
    #             bestSum = sum
    #             bestActionList = [i]
    #         elif sum == bestSum:
    #             bestActionList.append(i)
    #         board.pop()
    #     return random.choice(bestActionList)
    # 
    # def moveLearner(self, board, time):

    def move(self, board, time):
        action = self.moveHelper(board, time, True, 1, -float('inf'), float('inf'))
        return action

    def moveHelper(self, board, time, agentIndex, curDepth, alpha, beta):
        legalMoves = list(board.legal_moves)
        if (curDepth > self.depth) or (len(legalMoves) == 0):
            return self.eval(board, time)
        actionList = dict()
        oldCurDepth = curDepth
        if agentIndex:
            curDepth += 1
        for i in board.legal_moves:
            board.push(i)
            actionList[i] = self.moveHelper(board, time, not agentIndex,
                                                 curDepth, alpha, beta)
            board.pop()
            if agentIndex == 0:
                if max(actionList.values()) > beta:
                    if oldCurDepth == 1:
                        bestSum = max(actionList.values())
                        bestActionList = []
                        for i in actionList.keys():
                            if actionList[i] == bestSum:
                                bestActionList.append(i)
                        return random.choice(bestActionList)
                    return max(actionList.values())
                alpha = max(alpha, max(actionList.values()))

            else:
                if min(actionList.values()) < alpha:
                    return min(actionList.values())
                beta = min(beta, max(actionList.values()))
        if not (agentIndex) == 0:
            if oldCurDepth == 1:
                bestSum = max(actionList.values())
                bestActionList = []
                for i in actionList.keys():
                    if actionList[i] == bestSum:
                        bestActionList.append(i)
                return random.choice(bestActionList)
            return max(actionList.values())
        return min(actionList.values())

    def eval(self, board, time):
        if board.is_checkmate() and board.turn == self.color:
            return float('inf')
        if board.is_checkmate() and board.turn != self.color:
            return - float('inf')
        # print(board.piece_map())
        pieceList = []
        for i in board.piece_map().keys():
            pieceList.append(board.piece_map()[i])
        # print(pieceList)
        sum = 0
        for piece in pieceList:
            if piece.color == self.color:
                sum += (self.pieceValues[str(piece).lower()])
            else:
                sum -= self.pieceValues[str(piece).lower()]
        return sum

