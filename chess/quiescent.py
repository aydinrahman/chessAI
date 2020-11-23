import random
import chess


class Player:
    def __init__(self, board, color, time):
        random.seed(2)
        self.moveCalls = 0
        self.color = color
        self.depth = 1
        # pawn = 0; knight = 1; bishop = 2; rook = 3; queen = 4; king = 5
        self.pieceValues = [100, 320, 330, 500, 900, 0]
        self.positionValues = {
            "P": [0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, -20, -20, 10, 10, 5, 5, -5, 10, 0, 0, -10, -5, 5, 0, 0, 0, 20, 20,
                  0, 0, 0, 5, 5, 10, 25, 25, 10, 5, 5, 10, 10, 20, 30, 30, 20, 10, 10, 50, 50, 50, 50, 50, 50, 50, 50,
                  0, 0, 0, 0, 0, 0, 0, 0],
            "N": [-50, -40, -30, -30, -30, -30, -40, -50, -40, -20, 0, 5, 5, 0, -20, -40, -30, 5, 10, 15, 15, 10, 5,
                  -30, -30, 0, 15, 20, 20, 15, 0, -30, -30, 5, 15, 20, 20, 15, 5, -30, -30, 0, 10, 15, 15, 10, 0, -30,
                  -40, -20, 0, 0, 0, 0, -20, -40, -50, -40, -30, -30, -30, -30, -40, -50],
            "B": [-20, -10, -10, -10, -10, -10, -10, -20, -10, 5, 0, 0, 0, 0, 5, -10, -10, 10, 10, 10, 10, 10, 10, -10,
                  -10, 0, 10, 10, 10, 10, 0, -10, -10, 5, 5, 10, 10, 5, 5, -10, -10, 0, 5, 10, 10, 5, 0, -10, -10, 0, 0,
                  0, 0, 0, 0, -10, -20, -10, -10, -10, -10, -10, -10, -20],
            "R": [0, 0, 0, 5, 5, 0, 0, 0, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5,
                  -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 5, 10, 10, 10, 10, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0,
                  0],
            "Q": [-20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 5, 0, 0, 0, 0, -10, -10, 5, 5, 5, 5, 5, 0, -10, 0, 0, 5,
                  5, 5, 5, 0, -5, -5, 0, 5, 5, 5, 5, 0, -5, -10, 0, 5, 5, 5, 5, 0, -10, -10, 0, 0, 0, 0, 0, 0, -10, -20,
                  -10, -10, -5, -5, -10, -10, -20],
            "K": [20, 30, 10, 0, 0, 10, 30, 20, 20, 20, 0, 0, 0, 0, 20, 20, -10, -20, -20, -20, -20, -20, -20, -10, -20,
                  -30, -30, -40, -40, -30, -30, -20, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50,
                  -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30]}

    def move(self, board, time):
        self.moveCalls = 0
        action = self.moveHelper(board, time, True, 1, -float('inf'), float('inf'))
        # print("move = " + str(action))
        # print("num of moveCalls:")
        # print(self.moveCalls)
        return action

    def moveHelper(self, board, time, agentIndex, curDepth, alpha, beta):
        self.moveCalls += 1
        if (curDepth > self.depth) or board.is_checkmate():
            return self.eval(board, time)
        actionList = dict()
        oldCurDepth = curDepth
        if not agentIndex:
            curDepth += 1
        for i in board.legal_moves:
            origPieces = len(board.piece_map().keys())
            board.push(i)
            finPieces = len(board.piece_map().keys())
            if origPieces != finPieces and board.turn == self.color:
                actionList[i] = self.Quiesce(board, time, -20000, 20000)
            else:
                actionList[i] = self.moveHelper(board, time, not agentIndex,
                                            curDepth, alpha, beta)
            board.pop()
            if agentIndex:
                if max(actionList.values()) >= beta:
                    if oldCurDepth == 1:
                        bestSum = max(actionList.values())
                        bestActionList = []
                        for i in actionList.keys():
                            if actionList[i] == bestSum:
                                bestActionList.append(i)
                        return random.choice(bestActionList)
                    return max(actionList.values())
                # print(actionList)
                alpha = max(alpha, max(actionList.values()))

            else:
                if len(actionList.values()) == 0:
                    # print("hi?")
                    return float('inf')
                # print(actionList)
                if min(actionList.values()) <= alpha:
                    return min(actionList.values())
                beta = min(beta, max(actionList.values()))
        if agentIndex:
            if oldCurDepth == 1:
                bestSum = max(actionList.values())
                bestActionList = []
                for i in actionList.keys():
                    if actionList[i] == bestSum:
                        bestActionList.append(i)
                # print(actionList)
                # print("bestActionList")
                # print(bestActionList)
                return random.choice(bestActionList)
            # print(actionList)
            return max(actionList.values())
        if len(actionList.values()) == 0:
            # print("hi-er?")
            return float('inf')
        # print(actionList)
        return min(actionList.values())

    def eval(self, board, time):
        if board.is_checkmate() and board.turn == self.color:
            return - float('inf')
        if board.is_checkmate() and board.turn != self.color:
            return float('inf')

        sum = 0

        for i in board.piece_map().keys():
            piece = board.piece_map()[i]
            p = piece.symbol()
            if piece.color == self.color:
                if self.color:
                    sum += self.pieceValues[piece.piece_type - 1] + self.positionValues[p.upper()][i]
                else:
                    sum += self.pieceValues[piece.piece_type - 1] + self.positionValues[p.upper()][(7 - i // 8) * 8 + i]
            else:
                if self.color:
                    sum -= self.pieceValues[piece.piece_type - 1] + self.positionValues[p.upper()][i]
                else:
                    sum -= self.pieceValues[piece.piece_type - 1] + self.positionValues[p.upper()][(7 - i // 8) * 8 + i]

        if board.is_check() and board.turn == self.color:
            sum -= 50
        elif board.is_check() and board.turn != self.color:
            sum += 50

        return sum

    def Quiesce(self, board, time, alpha, beta):
        # if alpha == -20001:
        #     stand_pat = self.eval(board, time)
        #     print("stand_pat = " +str(stand_pat))
        #     if board.turn != self.color:
        #         stand_pat *= -1
        #     if (stand_pat >= beta):
        #         return beta
        #
        #     if (alpha < stand_pat):
        #         alpha = stand_pat
        #
        #     for i in board.legal_moves:
        #         print("i = " + str(i))
        #         origPieces = len(board.piece_map().keys())
        #         board.push(i)
        #         finPieces = len(board.piece_map().keys())
        #         if origPieces != finPieces:
        #             score = -self.Quiesce(board, time, -beta, -alpha)
        #
        #             if (score >= beta):
        #                 board.pop()
        #                 return beta
        #             if (score > alpha):
        #                 alpha = score
        #         board.pop()
        #
        #     return alpha
        # else:
        stand_pat = self.eval(board, time)
        if board.turn != self.color:
            stand_pat*=-1
        if (stand_pat >= beta):
            return beta

        if (alpha < stand_pat):
            alpha = stand_pat


        for i in board.legal_moves:
            origPieces = len(board.piece_map().keys())
            board.push(i)
            finPieces = len(board.piece_map().keys())
            if origPieces != finPieces:
                score = -self.Quiesce(board, time, -beta, -alpha)

                if (score >= beta):
                    board.pop()
                    return beta
                if (score > alpha):
                    alpha = score
            board.pop()


        return alpha