import chess
import chess.pgn
import time
import miniMaxMover as player1
import quiescent as player2

game = chess.pgn.Game()
node = game
board = chess.Board()
board1 = board.copy()
board2 = board.copy()
p1_time = 120
p2_time = 120

start = time.time()
p1 = player1.Player(board1, chess.WHITE, p1_time)
end = time.time()
p1_time -= end - start

start = time.time()
p2 = player2.Player(board2, chess.BLACK, p2_time)
end = time.time()
p2_time -= end - start
# move = p2.move(board, p1_time)
# print("finished")
# minigame = ['g1f3', 'g8f6', 'b1c3', 'b8c6', 'e2e4', 'h8g8', 'd2d4', 'g8h8', 'c1d2', 'h8g8', 'f1c4', 'g8h8', 'e1g1', 'h8g8', 'a1c1', 'g8h8', 'd1e1', 'h8g8', 'a2a3', 'g8h8', 'f3e5', 'c6e5', 'd4e5', 'f6g4', 'e5e6', 'g4e5', 'e6f7', 'e5f7', 'b2b4', 'f7e5', 'e1e2', 'a8b8', 'e2h5', 'e5g6', 'd2e3', 'b8a8', 'f1e1', 'a8b8', 'e3a7', 'b8a8', 'e1e3', 'a8a7', 'c1a1', 'a7a8', 'a1c1', 'a8a3', 'e4e5', 'a3a7', 'c3e4', 'a7a8', 'h2h3', 'a8a7', 'c1e1', 'a7a8', 'b4b5', 'a8a7', 'e3g3', 'a7a8', 'g3g6', 'd7d6', 'g6d6', 'g7g6', 'd6d8', 'e8d8']
#
# for i in minigame:
#     board.push(move.from_uci(i))

legal_move = True

while p1_time > 0 and p2_time > 0 and not board.is_game_over() and legal_move:
    board_copy = board.copy()
    if board.turn == chess.WHITE:
        start = time.time()
        move = p1.move(board_copy, p1_time)
        end = time.time()
        # print("move = " + str(move))
        p1_time -= end - start
    else:
        start = time.time()
        move = p2.move(board_copy, p2_time)
        end = time.time()
        # print("move = " + str(move))
        p2_time -= end - start

    if move in board.legal_moves:
        board.push(move)
        node = node.add_variation(move)
    else:
        legal_move = False

if not legal_move:
    if board.turn == chess.WHITE:
        print("Black wins - illegal move by white")
    else:
        print("White wins - illegal move by black")
elif p1_time <= 0:
    print("Black wins on time")
    board.pop()
elif p2_time <= 0:
    print("White wins on time")
    board.pop()
elif board.is_checkmate():
    if board.turn == chess.WHITE:
        print("Black wins - Checkmate!")
    else:
        print("White wins - Checkmate!")
elif board.is_stalemate():
    print("Draw - Stalemate")
elif board.is_insufficient_material():
    print("Draw - Insufficient Material")
elif board.is_seventyfive_moves():
    print("Draw - 75 moves without capture/pawn advancement")
elif board.is_fivefold_repetition():
    print("Draw - position repeated 5 times")
print(game)
print(p1_time)
print(p2_time)