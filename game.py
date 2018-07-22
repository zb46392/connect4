from Board import Board
from RandomBot import RandomBot
from MctsBot import MCTS_BOT
from gui import GUI
import time
import threading

def guiPlay():
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

RANDOM_VS_MCTS_GUI = 0
RANDOM_VS_MCTS_NOGUI = 1
USER_VS_MCTS = 2
GAME_STYLE = 0
if __name__ == '__main__':
    
    if GAME_STYLE is RANDOM_VS_MCTS_GUI:
        gui = GUI()
        t = threading.Thread(target=guiPlay)
        t.start()
        gui.root.mainloop()
        gui = None
        thread_stop = True
        t.join()
    elif GAME_STYLE is RANDOM_VS_MCTS_NOGUI:
        nbrOfPlays = 100
        board = Board()
        bot1 = RandomBot()
        bot2 = MCTS_BOT()
        bot1Score = 0
        bot2Score = 0        
        
        for i in range(nbrOfPlays):
            board = Board()
            while (board.checkGameState() == board.STILL_PLAYING):
                if board.turn == 1:
                    board.move(bot1.makeMove(board.copy()))
                else:
                    board.move(bot2.makeMove(board.copy()))
            if board.checkGameState() == board.PLAYER_1_WIN:
                bot1Score += 1
            elif  board.checkGameState() == board.PLAYER_2_WIN:
                bot2Score += 1
            print("rndBot: " + str(bot1Score) + " - " + "mctsBot: " + str(bot2Score))
            
        print("\nrndBot: " + str(float(bot1Score)/nbrOfPlays) + " - " + "mctsBot: " + str(float(bot2Score)/nbrOfPlays))
    else:
        pass