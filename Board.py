class Board(object):
    ROWS = 6
    COLLUMNS = 7
    WIN_CONNECT = 4
    INIT_BOARD = "".zfill(ROWS * COLLUMNS)
    STILL_PLAYING = 0
    PLAYER_1_WIN = 1
    PLAYER_2_WIN = 2
    DRAW = 3
    
    def __init__(self, init_str=None):
        if(init_str is None):
            self.setup(self.INIT_BOARD)
            self.turn = 1
        else:
            self.turn = self.calculateTurn(init_str)
            self.setup(init_str)        

    def calculateTurn(self, boardState):
        player1 = boardState.count('1')
        player2 = boardState.count('2')
        
        if(player1 > player2):
            return 2
        else:
            return 1
    
    def __str__(self):
        board = ""        
        for i in range((self.ROWS * self.COLLUMNS), 0, (0 - self.COLLUMNS)):
            for j in range((i-self.COLLUMNS), i, 1):
                '''
                if self.board[j] == 0:
                    board += " "
                else:
                    board += str(self.board[j])
                '''   
                board += str(self.board[j])
            board += "\n"            
        return board
        
    def toString(self):
        board = ""        
        for i in range(len(self.board)):
            board += str(self.board[i])
        return board
        
        
    def setup(self, bstr):
        if len(bstr) != self.ROWS * self.COLLUMNS:
            print('Board string length {}'.format(len(bstr)))
        else:
            self.board = [ int(c) for c in bstr ]
            
    def toArray(self):
        board = []
        for i in range((self.ROWS * self.COLLUMNS), 0, (0 - self.COLLUMNS)):
            for j in range((i-self.COLLUMNS), i, 1):
                board.append(self.board[j])
        return board

   
    def copy(self):
        cBoard = Board(self.toString()) 
        return cBoard
        
    def move(self, m):
        self.board[m] = self.turn
        self.turn = 1 if self.turn == 2 else 2    
        
    def generateLegalMoves(self):
        legalMoves = []
        for position in range(self.COLLUMNS):
            cell = position
            while((cell < self.COLLUMNS * self.ROWS) and (self.board[cell] != 0)):
                cell += self.COLLUMNS            
            if(cell < (self.COLLUMNS * self.ROWS)):
                legalMoves.append(cell)        
        return legalMoves
        
    def checkGameState(self):
        # 0 - still playing, 1 - player 1 wins, 2 - player 2 wins, 3 - draw
        state = self.STILL_PLAYING
        
        state = self.checkPlayerWonState()
        
        if state != self.STILL_PLAYING:
            return state
            
        state = self.checkDrawState()
            
        return state
    
    def checkPlayerWonState(self):
        state = self.STILL_PLAYING

        if (self.COLLUMNS >= self.WIN_CONNECT):
            state = self.checkPlayerWonInRow()
        
        if state != self.STILL_PLAYING:
            return state
        
        if (self.ROWS >= self.WIN_CONNECT):
            state = self.checkPlayerWonInCollumn()
        
        if state != self.STILL_PLAYING:
            return state
        
        if ((self.COLLUMNS >= self.WIN_CONNECT) and (self.ROWS >= self.WIN_CONNECT)):
            state = self.checkPlayerWonInDiagonal()
        
        return state
        
    def checkPlayerWonInRow(self):
        for i in range(self.ROWS):
            cnt = 0
            player = self.board[i * self.COLLUMNS]
            for j in range(self.COLLUMNS):
                if(self.board[((i * self.COLLUMNS) + j)] == player and player != 0):
                    cnt += 1               
                    if(cnt == self.WIN_CONNECT):
                        return player
                else:
                    cnt = 1
                    player = self.board[((i * self.COLLUMNS) + j)]
        return 0
        
    def checkPlayerWonInCollumn(self):
        for i in range(self.COLLUMNS):
            cnt = 0
            player = self.board[i]
            if player != 0:
                for j in range(self.ROWS):
                    if(self.board[((j * self.COLLUMNS) + i)] == player):
                        cnt += 1                 
                        if(cnt == self.WIN_CONNECT):
                            return player
                    elif(self.board[((j * self.COLLUMNS) + i)] != 0):
                        cnt = 1
                        player = self.board[((j * self.COLLUMNS) + i)]
                    else:
                        break
        return 0
        
    def checkPlayerWonInDiagonal(self):
        state = self.STILL_PLAYING
        
        state = self.checkAllForwardDiagonals()
        
        if state != self.STILL_PLAYING:
            return state
        
        state = self.checkAllBackwardDiagonals()
        
        return state
        
    
    def checkAllForwardDiagonals(self):
        topleft = (self.COLLUMNS * (self.ROWS - 1))   
        start = topleft - ((self.WIN_CONNECT - 1) * self.COLLUMNS)
        cells = self.WIN_CONNECT
        maxCells = self.COLLUMNS if self.COLLUMNS < self.ROWS else self.ROWS
        state = self.STILL_PLAYING
        
        while (start >= 0):
            state = self.checkForwardDiagonal(start, cells)
            if state != self.STILL_PLAYING:
                return state
            start -= self.COLLUMNS
            if cells < maxCells:
                cells += 1
            
                    
        start = 1
        cells = (self.COLLUMNS - 1) if ((self.COLLUMNS - 1) < maxCells) else maxCells
        
        while (start <= (self.COLLUMNS - self.WIN_CONNECT)):
            state = self.checkForwardDiagonal(start, cells)
            if state != self.STILL_PLAYING:
                return state
            start += 1
            if cells > self.WIN_CONNECT:
                cells -= 1
            
        return self.STILL_PLAYING
                    
                    
    def checkForwardDiagonal(self, start, cells):
        player = self.board[start]
        cnt = 0
        
        for i in range(cells):
            if(self.board[start + (i * (self.COLLUMNS + 1))] == player and player != 0):
                cnt += 1
                if(cnt == self.WIN_CONNECT):
                    return player
            else:
                cnt = 1
                player = self.board[start + (i * (self.COLLUMNS + 1))]                
        return self.STILL_PLAYING
        
    def checkAllBackwardDiagonals(self):
        topright = ((self.COLLUMNS * self.ROWS) - 1)
        start = topright - ((self.WIN_CONNECT - 1) * self.COLLUMNS)
        cells = self.WIN_CONNECT
        maxCells = self.COLLUMNS if self.COLLUMNS < self.ROWS else self.ROWS
        state = self.STILL_PLAYING
        
        
        while (start >= 0):
            state = self.checkBackwardDiagonal(start, cells)
            if state != self.STILL_PLAYING:
                return state
            start -= self.COLLUMNS
            if cells < maxCells:
                cells += 1
            
                    
        start = self.COLLUMNS - 2
        cells = (self.COLLUMNS - 1) if ((self.COLLUMNS - 1) < maxCells) else maxCells
        
        while (start >= (self.COLLUMNS - self.WIN_CONNECT)):
            state = self.checkBackwardDiagonal(start, cells)
            if state != self.STILL_PLAYING:
                return state
            start -= 1
            if cells > self.WIN_CONNECT:
                cells -= 1
            
        return self.STILL_PLAYING
        
    def checkBackwardDiagonal(self, start, cells):
        player = self.board[start]
        cnt = 0
        for i in range(cells):
            if(self.board[start + (i * (self.COLLUMNS - 1))] == player and player != 0):
                cnt += 1
                if(cnt == self.WIN_CONNECT):
                    return player
            else:
                cnt = 1
                player = self.board[start + (i * (self.COLLUMNS - 1))]                
        return 0
        
    def checkDrawState(self):
        if(len(self.generateLegalMoves()) == 0):
            return self.DRAW
        return self.STILL_PLAYING