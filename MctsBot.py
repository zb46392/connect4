#import time
from Board import Board
from math import sqrt, log
from random import randint


class Node(object):
    C = 0.5 # sqrt(0.2)    
    
    def __init__(self):
        self.nbrOfSimulations = 0
        self.score = 0
        self.nextStates = []
        self.move = None
        
    def calculateExploitation(self):
        return (self.score/self.nbrOfSimulations)
        
    def calculateExploration(self, nbrOfSimulationsOnParent):
        return self.C * sqrt((log(nbrOfSimulationsOnParent))/(self.nbrOfSimulations))
        
    def calculateUCT(self, nbrOfSimulationsOnParent):
        return self.calculateExploitation() + self.calculateExploration(nbrOfSimulationsOnParent)


class MCTS_BOT(object):
    NBR_OF_SIMULATIONS = 1000
        # 1) SELECTION -> selectNextNode until Node is unexplored (traverse tree)
        # 2) EXPANSION ? -> add new Node to tree
        # 3) ROLLOUT -> play random game 
        # 4) BACKPROPAGATION -> update nodes
    
    def __init__(self):
        pass

        
    def makeMove(self, board):
        self.playerNbr = board.turn
        currentState = board.toString()
        states = {currentState : Node()}
        
        
        self.simulate(currentState, states)
        
        return self.pickBestMove(currentState, states)
        
    
    def simulate(self, rootState, states):
        for i in range(self.NBR_OF_SIMULATIONS):
            self.runSimulation(rootState, states)
            
            
    def runSimulation(self, observingState, states):
        if(len(states[observingState].nextStates) == len(Board(observingState).generateLegalMoves())):
            score = self.runSimulation(self.selectNextObservingState(observingState, states), states)            
        else:
            expandetState = self.expandState(observingState, states)            
            score = self.generateRolloutScore(expandetState)
            
            states[expandetState].score += score
            states[expandetState].nbrOfSimulations += 1
        
        states[observingState].score += score
        states[observingState].nbrOfSimulations += 1
        return score
    
    def selectNextObservingState(self, observingState, states):
        nextState = None
        for state in states[observingState].nextStates:
            
            if nextState is not None:
                if states[state].calculateUCT(states[observingState].nbrOfSimulations) > states[nextState].calculateUCT(states[observingState].nbrOfSimulations):
                    nextState = state
            else:
                nextState = state
                
        return nextState
    
    def expandState(self, state, states):
        board = Board(state)
        moves = board.generateLegalMoves()
        nextStates = []
        
        for move in moves:
            tmpBoard = board.copy()
            tmpBoard.move(move)
            nextStates.append(tmpBoard.toString())
        print(nextStates)
        possibleStates = [possibleState for possibleState in nextStates if possibleState not in states] 
        print(possibleStates)
        expandetState = possibleStates[randint(0, (len(possibleStates) - 1))]
                
        states[state].nextStates.append(expandetState)
        states[expandetState] = Node()
        print("\n\n")
        return expandetState
        
    
    def generateRolloutScore(self, expandedState):
        board = Board(expandedState)
        
        while (board.checkGameState() == board.STILL_PLAYING):
            self.makeRandomMove(board)
            
        if(self.hasWon(board)):
            return 1
        elif(board.checkGameState() == board.DRAW):
            return 0.5
        else:
            return 0
    
    
    def makeRandomMove(self, board):
        moves = board.generateLegalMoves()
        m = randint(0, (len(moves) - 1))
        
        board.move(moves[m])
        
    def hasWon(self, board):
        return board.checkGameState() == self.playerNbr
        
    def pickBestMove(self, state, states):
        return self.selectNextObservingState(state, states)

mc_bot = MCTS_BOT()
board = Board()
moves = board.generateLegalMoves()
state = board.toString()
states = {state : Node()}

print(mc_bot.makeMove(board.copy()))