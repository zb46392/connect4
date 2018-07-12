from Board import Board
from RandomBot import RandomBot
from MctsBot import MCTS_BOT
from gui import GUI
import time
import threading

def play():
    board = Board()
    bot1 = RandomBot()
    bot2 = MCTS_BOT()
    while (board.checkGameState() == board.STILL_PLAYING):
        if board.turn == 1:
            board.move(bot1.makeMove(board.copy()))
        else:
            board.move(bot2.makeMove(board.copy()))
        if gui is not None:
            gui.show(board)
            
        time.sleep(0.5)

if __name__ == '__main__':
    gui = GUI()
    t = threading.Thread(target=play)
    t.start()
    gui.root.mainloop()
    gui = None
    thread_stop = True
    t.join()