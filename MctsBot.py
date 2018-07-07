#import time
from Board import Board
from math import sqrt, log



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
    
    
class Tree(object):
    def __init__(self):
        self.root = Node(None)
        self.states = [] # {board: Node}
        
    


class MCTS_BOT(object):
    NBR_OF_SIMULATIONS = 1000
        # 1) SELECTION -> selectNextNode until Node is unexplored (traverse tree)
        # 2) EXPANSION ? -> add new Node to tree
        # 3) ROLLOUT -> play random game 
        # 4) BACKPROPAGATION -> update nodes
    
    def __init__(self, timeToMakeMove = None):
        self.timeToMakeMove = 10 if timeToMakeMove is None else timeToMakeMove
        
    def makeMove(self, board):
        currentState = board.toString()
        states = {currentState : Node()}
        
        self.simulate(states, self.NBR_OF_SIMULATIONS)
        
        return self.pickBestMove(states, currentState)
        
    
    def simulate(self, states, nbrOfSimulations):
        
        expandetState = self.expandState(self.selectStateForExpansion())
        
        self.generateRollout(expandetState)
        
        # recursive function 
        # get ( end of selection phase )
        # 
        pass
    
    
    def selectStateForExpansion(self, observingState, states):
        while (len(states[observingState].nextStates < len(Board(observingState).generateLegalMoves()))):
            observingState = self.findStateForSelection(observingState, states)
            
        return observingState
    
    def findStateForSelection(self, observingState, states):
        stateForSelection = states[observingState].nextStates[0]
        for state in states[observingState].nextStates:
            pass 
    
    def makeExpansion(self):
        pass
    
    def makeRollout(self):
        pass