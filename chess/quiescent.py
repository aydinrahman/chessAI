import random
import chess
import numpy as np


class Player:
    def __init__(self, board, color, time):
        random.seed(28)
        self.moveCalls = 0
        self.color = color
        self.depth = 1
        self.bool = False
        # pawn = 0; knight = 1; bishop = 2; rook = 3; queen = 4; king = 5
        self.piece_values = {'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 900,
                        'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -900}
        # values gotten from https://www.chessprogramming.org/Simplified_Evaluation_Function
        self.positionValues = {
            'P': np.array([[0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
                           [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
                           [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
                           [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
                           [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
                           [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
                           [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
                           [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]),

            'N': np.array([[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
                           [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
                           [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
                           [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
                           [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
                           [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
                           [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
                           [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]),

            'B': np.array([[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
                           [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                           [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
                           [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
                           [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
                           [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
                           [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
                           [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]),

            'R': np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  0.0],
                           [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,  0.5],
                           [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                           [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                           [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                           [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                           [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                           [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0,  0.0]]),

            'Q': np.array([[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
                           [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
                           [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                           [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                           [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
                           [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
                           [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
                           [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]),

            'K': np.array([[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                           [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                           [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                           [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                           [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                           [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
                           [2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
                           [2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]])}

    def move(self, board, time):
        self.moveCalls = 0
        action = self.moveHelper(board, time, True, 1, -float('inf'), float('inf'))
        return action

    def moveHelper(self, board, time, agentIndex, curDepth, alpha, beta):
        self.moveCalls += 1
        if (curDepth > self.depth) or board.is_checkmate():
            return self.positionEvaluation(board)
        actionList = dict()
        oldCurDepth = curDepth
        if not agentIndex:
            curDepth += 1
        legMoves = list(board.legal_moves)

        for i in legMoves:
            origPieces = len(board.piece_map().keys())
            board.push(i)
            finPieces = len(board.piece_map().keys())
            if origPieces != finPieces and board.turn == self.color:
                eval = self.positionEvaluation(board)
                actionList[i] = self.Quiesce(board, time, eval, eval+900)
            else:
                actionList[i] = self.moveHelper(board, time, not agentIndex,
                                            curDepth, alpha, beta)
            board.pop()
            if agentIndex:
                if actionList[i] > beta:
                    return actionList[i]
                alpha = max(alpha, actionList[i])
            else:
                if actionList[i] < alpha:
                    return actionList[i]
                beta = min(beta, actionList[i])

        if agentIndex:
            if oldCurDepth == 1:
                bestSum = max(actionList.values())
                bestActionList = []
                for i in actionList.keys():
                    if actionList[i] == bestSum:
                        bestActionList.append(i)
                return random.choice(bestActionList)
            return max(actionList.values())
        if len(actionList.values()) == 0:
            return float('inf')
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

    def positionEvaluation(self, position):
        # Position of pieces is not taken into account for their strength
        position_values = self.positionValues
        piece_values = self.piece_values
        if position_values == 'None':
            total_eval = 0
            pieces = list(position.piece_map().values())

            for piece in pieces:
                total_eval += piece_values[str(piece)]

            return total_eval

        else:
            positionTotalEval = 0
            pieces = position.piece_map()

            for j in pieces:
                file = chess.square_file(j)
                rank = chess.square_rank(j)

                piece_type = str(pieces[j])
                positionArray = position_values[piece_type.upper()]

                if piece_type.isupper():
                    flippedPositionArray = np.flip(positionArray, axis=0)
                    positionTotalEval += piece_values[piece_type] + \
                                         flippedPositionArray[rank, file]

                else:
                    positionTotalEval += piece_values[piece_type] - \
                                         positionArray[rank, file]

            if self.color == False:
                positionTotalEval *=-1
            return positionTotalEval

    def Quiesce(self, board, time, alpha, beta):
        stand_pat = self.positionEvaluation(board)
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