import random
import chess
import numpy


class Player:
    def __init__(self, board, color, time):
        random.seed(3)
        self.color = color
        self.depth = 1
        self.pieceValues = {'p': 100, 'n': 320, "b": 330, "r": 500, "q": 900, "k": 0}
        self.PAWN_TABLE = numpy.array([
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5,  10, 10,-20,-20, 10, 10, 5],
            [5, -5, -10, 0,  0, -10, -5, 5],
            [0,  0,  0,  20, 25, 0,  0,  0],
            [5,  5,  10, 20, 20, 10, 5,  5],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ])

        pass

    def move(self, board, time):
        print("move g")
        action = self.moveHelper(board, time, True, 1, -float('inf'), float('inf'))
        return action

    def moveHelper(self, board, time, agentIndex, curDepth, alpha, beta):
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
                curDepth -= 1
                print("it's working?")
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
                        if len(bestActionList) > 1:
                            print("multiple options")
                            print(bestActionList)
                        return random.choice(bestActionList)
                    return max(actionList.values())
                alpha = max(alpha, max(actionList.values()))

            else:
                if len(actionList.values()) == 0:
                    return float('inf')
                print("actionList = " + str(actionList))
                print("min of actionList = " + str(min(actionList.values())))
                if min(actionList.values()) <= alpha:
                    print("step 2")
                    return min(actionList.values())
                beta = min(beta, max(actionList.values()))
        if agentIndex:
            if oldCurDepth == 1:
                bestSum = max(actionList.values())
                bestActionList = []
                for i in actionList.keys():
                    if actionList[i] == bestSum:
                        bestActionList.append(i)
                if len(bestActionList) > 1:
                    print("multiple options")
                    print(bestActionList)
                    print(actionList)
                return random.choice(bestActionList)
            return max(actionList.values())
        if len(actionList.values()) == 0:
            return float('inf')
        return min(actionList.values())

    def eval(self, board, time):
        print("doing an eval")
        if board.is_checkmate() and board.turn == self.color:
            return - float('inf')
        if board.is_checkmate() and board.turn != self.color:
            return float('inf')
        sum = 0
        for i in board.piece_map().keys():
            piece = board.piece_map()[i]
            if piece.color == self.color:
                sum += (self.pieceValues[str(piece).lower()])
            else:
                sum -= self.pieceValues[str(piece).lower()]

            if piece.piece_type == 1:
                if piece.color == self.color:
                    if self.color:
                        sum += self.PAWN_TABLE[i//8][i%8]
                    else:
                        sum += self.PAWN_TABLE[7- (i//8)][(i % 8)]
                else:
                    if self.color:
                        sum -= self.PAWN_TABLE[i//8][i%8]
                    else:
                        sum -= self.PAWN_TABLE[7- (i//8)][(i % 8)]

        if board.is_check():
            sum -= 50
        if (4 in board.piece_map() and board.piece_map()[4] == 6):
            if self.color == board.piece_map[4].color:
                sum += 50
            else:
                sum -= 50
        if (60 in board.piece_map() and board.piece_map()[60] == 6):
            if self.color == board.piece_map[60].color:
                sum += 50
            else:
                sum -= 50





        if sum == -425:
            print("THIS IS THE SUPER IMPORTANT THING TO LOOK AT ")
            if board.is_checkmate() and board.turn == self.color:
                print("checkmate = possible")
                return - float('inf')
            if board.is_checkmate() and board.turn != self.color:
                print("checkmate = possible 2")
                return float('inf')
            sum = 0
            print(board)
            for i in board.piece_map().keys():
                piece = board.piece_map()[i]
                if piece.color == self.color:
                    sum += self.pieceValues[str(piece).lower()]
                else:
                    sum -= self.pieceValues[str(piece).lower()]

                if piece.piece_type == 1:
                    if piece.color == self.color:
                        if self.color:
                            sum += self.PAWN_TABLE[i // 8][i % 8]
                        else:
                            sum += self.PAWN_TABLE[7 - (i // 8)][(i % 8)]
                    else:
                        if self.color:
                            sum -= self.PAWN_TABLE[i // 8][i % 8]
                        else:
                            sum -= self.PAWN_TABLE[7 - (i // 8)][(i % 8)]

            if board.is_check():
                sum -= 50
            if (4 in board.piece_map() and board.piece_map()[4] == 6):
                if self.color == board.piece_map[4].color:
                    sum += 50
                else:
                    sum -= 50
            if (60 in board.piece_map() and board.piece_map()[60] == 6):
                if self.color == board.piece_map[60].color:
                    sum += 50
                else:
                    sum -= 50




        return sum

