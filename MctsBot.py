#import time
from Board import Board
from math import sqrt, log
from random import randint


class Node(object):
    C = 0.5   
    
    def __init__(self):
        self.nbrOfSimulations = 0
        self.score = 0
        self.nextStates = []
        self.move = None
        
    def calculateExploitation(self):
        return (float(self.score)/self.nbrOfSimulations)
        
    def calculateExploration(self, nbrOfSimulationsOnParent):
        return self.C * sqrt((log(float(nbrOfSimulationsOnParent)))/(self.nbrOfSimulations))
        
    def calculateUCT(self, nbrOfSimulationsOnParent):
        return self.calculateExploitation() + self.calculateExploration(nbrOfSimulationsOnParent)


class MCTS_BOT(object):
    NBR_OF_SIMULATIONS = 10
    
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
        score = 0        
        self.addExistingNextStatesNotInNextStates(observingState, states)
        
        if((len(states[observingState].nextStates) == len(Board(observingState).generateLegalMoves())) and (not self.stateIsTerminal(observingState))):
            score = self.runSimulation(self.selectNextObservingState(observingState, states), states)            
        else:
            
            
            if self.stateIsTerminal(observingState):
                score = self.calculateScore(Board(observingState))
            else:
                expandedState = self.expandState(observingState, states)

                if self.stateIsTerminal(expandedState):
                    score = self.calculateScore(Board(expandedState))
                else:
                    score = self.generateRolloutScore(expandedState)
                
                states[expandedState].score += score
                states[expandedState].nbrOfSimulations += 1
        
        
        states[observingState].score += score
        states[observingState].nbrOfSimulations += 1
        
        return score
    
    def addExistingNextStatesNotInNextStates(self, observingState, states):
        allNextStates = self.generateNextStates(observingState)
        
        for state in allNextStates:
            if((state not in states[observingState].nextStates) and (state in states)):
                states[observingState].nextStates.append(state)
    
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
        nextStates = self.generateNextStates(state)
            
        possibleStates = [possibleState for possibleState in nextStates if possibleState not in states] 

        expandedState = possibleStates[randint(0, (len(possibleStates) - 1))]
                
        states[state].nextStates.append(expandedState)
        states[expandedState] = Node()
        
        return expandedState
        
    def generateNextStates(self, state):
        board = Board(state)
        moves = board.generateLegalMoves()
        nextStates = []
        
        for move in moves:
            tmpBoard = board.copy()
            tmpBoard.move(move)
            nextStates.append(tmpBoard.toString())
        
        return nextStates
        
    def generateRolloutScore(self, expandedState):
        board = Board(expandedState)
        
        while (board.checkGameState() == board.STILL_PLAYING):
            self.makeRandomMove(board)
            
        return self.calculateScore(board)
            
    def calculateScore(self, board):
        
        if(self.hasWon(board)):
            return 1
        elif(board.checkGameState() == board.DRAW):
            return 0.5
        else:
            return 0
        
    def stateIsTerminal(self, state):
        board = Board(state)
        
        return board.checkGameState() is not board.STILL_PLAYING
    
    def makeRandomMove(self, board):
        moves = board.generateLegalMoves()
        m = randint(0, (len(moves) - 1))
        
        board.move(moves[m])
        
    def hasWon(self, board):
        return board.checkGameState() == self.playerNbr
        
    def pickBestMove(self, state, states):
        board = Board(state)
        moves = board.generateLegalMoves()
        bestState = self.selectNextObservingState(state, states)
        bestMove = None
        
        for move in moves:
            cBoard = board.copy()
            cBoard.move(move)
            if(cBoard.toString() == bestState):
                bestMove = move
                break
            
        
        return bestMove