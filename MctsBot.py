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
    NBR_OF_SIMULATIONS = 1000
    
    def __init__(self):
        self.states = {}

        
    def makeMove(self, board):
        self.playerNbr = board.turn
        currentState = board.toString()
        
        if currentState not in self.states:
            self.states[currentState] = Node()
        
        
        self.simulate(currentState)
        
        return self.pickBestMove(currentState)
        
    
    def simulate(self, rootState):
        for i in range(self.NBR_OF_SIMULATIONS):
            self.runSimulation(rootState)      
            
            
    def runSimulation(self, observingState):
        score = 0        
        self.addExistingNextStatesNotInNextStates(observingState)
        
        if((len(self.states[observingState].nextStates) == len(Board(observingState).generateLegalMoves())) and (not self.stateIsTerminal(observingState))):
            score = self.runSimulation(self.selectNextObservingState(observingState))            
        else:
            
            
            if self.stateIsTerminal(observingState):
                score = self.calculateScore(Board(observingState))
            else:
                expandedState = self.expandState(observingState)

                if self.stateIsTerminal(expandedState):
                    score = self.calculateScore(Board(expandedState))
                else:
                    score = self.generateRolloutScore(expandedState)
                
                self.states[expandedState].score += score
                self.states[expandedState].nbrOfSimulations += 1
        
        
        self.states[observingState].score += score
        self.states[observingState].nbrOfSimulations += 1
        
        return score
    
    def addExistingNextStatesNotInNextStates(self, observingState):
        allNextStates = self.generateNextStates(observingState)
        
        for state in allNextStates:
            if((state not in self.states[observingState].nextStates) and (state in self.states)):
                self.states[observingState].nextStates.append(state)
    
    def selectNextObservingState(self, observingState):
        nextState = None
        for state in self.states[observingState].nextStates:
            if nextState is not None:
                if self.states[state].calculateUCT(self.states[observingState].nbrOfSimulations) > self.states[nextState].calculateUCT(self.states[observingState].nbrOfSimulations):
                    nextState = state
            else:
                nextState = state
                
        return nextState
    
    def expandState(self, state):
        nextStates = self.generateNextStates(state)
            
        possibleStates = [possibleState for possibleState in nextStates if possibleState not in self.states] 

        expandedState = possibleStates[randint(0, (len(possibleStates) - 1))]
                
        self.states[state].nextStates.append(expandedState)
        self.states[expandedState] = Node()
        
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
        
    def pickBestMove(self, state):
        board = Board(state)
        moves = board.generateLegalMoves()
        bestState = self.selectNextObservingState(state)
        bestMove = None
        
        for move in moves:
            cBoard = board.copy()
            cBoard.move(move)
            if(cBoard.toString() == bestState):
                bestMove = move
                break
            
        
        return bestMove