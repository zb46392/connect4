import Tkinter
from Tkinter import Frame, Canvas

class GUI(object):
    cellSize = 50
    BOT_PLAY = 0
    USER_PLAY = 1
    USER_POS = 0
    
    
    def __init__(self, gamePlay):
        self.root = Tkinter.Tk()
        
        self.root.title("CONNECT 4")
        self.boardView = None
        self.root.bind('<Right>', self.handleRightKeyPressed)
        self.root.bind('<Left>', self.handleLeftKeyPressed)
        self.root.bind('<Return>', self.handleReturnKeyPressed)
        self.gamePlay = gamePlay
        
    def show(self, board):
        if self.gamePlay is self.BOT_PLAY:
            if self.boardView == None:
                frame = Frame(self.root)
                frame.pack()
                self.boardView = Canvas(frame, bg='blue', height=board.ROWS*self.cellSize, width=board.COLLUMNS*self.cellSize)
                self.boardView.pack(side=Tkinter.TOP)
            
            self.boardView.children.clear()
            b = board.toArray()
            for i in range(board.COLLUMNS * board.ROWS):
                x, y = (i%board.COLLUMNS) * self.cellSize, (i//board.COLLUMNS) * self.cellSize
                start = self.cellSize//10
                end = self.cellSize-start
                oval = x+start, y+start, x+end, y+end
                if(b[i] == 0):
                    self.boardView.create_oval(oval, fill='white')
                elif(b[i] == 1):
                    self.boardView.create_oval(oval, fill='red')
                else:
                    self.boardView.create_oval(oval, fill='yellow')
        elif self.gamePlay is self.USER_PLAY:
            if self.boardView == None:
                frame = Frame(self.root)                
                frame.pack()
                self.boardView = Canvas(frame, bg='blue', height=board.ROWS*self.cellSize+self.cellSize, width=board.COLLUMNS*self.cellSize)
                self.boardView.pack(side=Tkinter.TOP)
            
            self.boardView.children.clear()
            b = board.toArray()
            
            if(self.USER_POS == board.COLLUMNS):
                self.USER_POS = 0
            elif(self.USER_POS < 0):
                self.USER_POS = board.COLLUMNS - 1
            
            o = (self.USER_POS%board.COLLUMNS) * self.cellSize + self.cellSize//10, self.cellSize//10, (self.USER_POS%board.COLLUMNS) * self.cellSize + self.cellSize - self.cellSize//10, self.cellSize - self.cellSize//10
            
            self.boardView.create_oval(o, fill='green')
            
            for i in range(board.COLLUMNS * board.ROWS):
                x, y = (i%board.COLLUMNS) * self.cellSize, (i//board.COLLUMNS) * self.cellSize + self.cellSize
                start = self.cellSize//10
                end = self.cellSize-start
                oval = x+start, y+start, x+end, y+end
                if(b[i] == 0):
                    self.boardView.create_oval(oval, fill='white')
                elif(b[i] == 1):
                    self.boardView.create_oval(oval, fill='red')
                else:
                    self.boardView.create_oval(oval, fill='yellow')
    
    def handleRightKeyPressed(self, event):
        self.USER_POS += 1
        
    def handleLeftKeyPressed(self, event):
        self.USER_POS -= 1
        
    def handleReturnKeyPressed(self, event):
        self.close()
        
    def waitUserMove(self, board):
        pass
            
    
    def close(self):
        print("Exiting...")
        self.root.destroy()