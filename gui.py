import Tkinter
from Tkinter import Frame, Canvas

class GUI(object):
    cellSize = 50
    
    def __init__(self):
        self.root = Tkinter.Tk()
        
        self.root.title("CONNECT 4")
        self.boardView = None
        
    def show(self, board):
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
    
    def close(self):
        print("Exiting...")
        self.root.destroy()