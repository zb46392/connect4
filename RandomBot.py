from random import randint

class RandomBot(object):
    def __init__(self):
        pass
    
    def makeMove(self, board):
        moves = board.generateLegalMoves()
        m = randint(0, (len(moves) - 1))
        
        return moves[m]