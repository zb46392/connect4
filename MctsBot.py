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
        
        self.simulate(currentState, states, self.NBR_OF_SIMULATIONS)
        
        return self.pickBestMove(states, currentState)
        
    
    def simulate(self, rootState, states, nbrOfSimulations):
        
        if(nbrOfSimulations > 0):
            self.selectStateForExpansion(rootState, states)
            
            
            self.updateStates(self.generateRollout(self.expandState()))
            
        else:
            return
    
    
    def selectStateForExpansion(self, rootState, states):
        observingState = states[rootState]
        
        while(len(states[observingState].nextStates) == len(Board(observingState).generateLegalMoves())):
            observingState = self.selectNextObservingState(observingState, states)
            
        return observingState
    
    def selectNextObservingState(self, observingState, states):
        nextState = None
        for state in states[observingState].nextStates:
            if nextState is not None:
                if state.calculateUCT(observingState.nbrOfSimulations) > nextState.calculateUCT(observingState.nbrOfSimulations):
                    nextState = state
            else:
                nextState = state
                
        return nextState
    
    def expandState(self, state, states):
        
        board = Board(state)
        moves = board.generateLegalMoves()
        nextStates = [board.copy().move(move).toString() for move in moves]        
        possibleStates = [possibleState for possibleState in nextStates if possibleState not in states]
        
        expandetState = possibleStates[randint(0, (len(possibleStates) - 1))]
                
        states[expandetState] = Node()
        
        return expandetState
        
    
    def makeRollout(self):
        pass