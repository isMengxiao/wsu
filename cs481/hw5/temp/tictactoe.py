#! /usr/bin/env python3

from tkinter import *
place = {"nw", "n", "ne", "w", "center", "e", "sw", "s", "se"}

# Insert code for TicTacToeBoard or import it from a separate module.
# Your choice.

class TicTacToeBoard(Frame):
    def __init__(self, title='TicTacToe'):
        super().__init__()
        self.empty = ""
        self.buttons = [[None for i in range(3)] for j in range(3)]
        self.mark = [[None for i in range(3)] for j in range(3)]
        self.player = 'human'
        self.steps = 0
        self.c = [0 ,0]
        self.var = StringVar()
        self.infolab = None
        self.initwindow()

    def initwindow(self):
        self.master.title('Tic Tac Toe')
        self.pack(fill=BOTH, expand=1)
        for i in range(3):
            for j in range(3):
            #tframe.pack(side=TOP, expand=YES, fill=BOTH)
                self.buttons[i][j] = Button(self, height=1, width=2,
                    text=self.empty, font=('Courier', 50),
                    command = lambda i=i, j=j : self.callback(self.buttons[i][j]))
                self.buttons[i][j].grid(row=i, column=j)
#            tbtn.pack(side=LEFT, expand=YES, fill=BOTH)
        clearbtn = Button(self, text='clear', command=self.emptyall)
        clearbtn.grid(row=4, column=2)
        infolab = Label(self, width=10, textvariable=self.var)
        self.var.set('gaming')
        infolab.grid(row = 3, column=0, columnspan = 2, rowspan = 2)
        quitbtn =  Button(self, text='quit', command =self.quit)
        quitbtn.grid(row=3, column=2)
        self.cpumove(self.buttons[0][1])

    def emptyall(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text=self.empty)
        self.__init__()

    def callback(self, button):
        if self.steps < 9:
            if button["text"] == '':
                button["text"] = 'O'
                info = button.grid_info()
                self.mark[info["row"]][info["column"]] = 1
                self.steps += 1
                self.var.set("Your turn!")
                self.cpumove(button)
        else:
            self.var.set("Game is over!")
            #self.infolab["text"] = "Error!The game is over!"
            #print("Error!The game is over!")

    def cpumove(self, button):
        if self.steps < 9:
            self.nextmove(button)
            self.steps += 1
            if self.checkgame():
                self.steps = 9
            if self.steps == 9:
                self.gameover()
        else:
            self.gameover()
            return

    def nextmove(self, button):
        info = button.grid_info()
        r = info["row"]
        c = info["column"]
        rb, cb = self.c
        s = [(r+1, c), (r+1, c-1), (r, c-1),
             (r-1, c-1), (r-1, c), (r-1, c+1),
             (r, c+1), (r+1, c+1)]
        """
        if (rb-1)>=0 and (cb-1)>=0 and (not self.buttons[rb-1][cb-1]["text"]):
            self.buttons[rb-1][cb-1]["text"] = 'X'
            return
        if 0<=(rb+1)<3  and 0<=(cb+1)<3  and (not self.buttons[rb+1][cb+1]["text"]):
            self.buttons[rb+1][cb+1]["text"] = 'X'
            return
        """
        for (a, b) in s:
            #print("(%d,%d)"%(a,b))
            if 0<=a<3 and 0<=b<3 and (not self.buttons[a][b]["text"]):
                self.buttons[a][b]["text"] = 'X'
                self.c = [a,b]
                return
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == '':
                    self.buttons[i][j]["text"] = 'X'
                    self.c = [i,j]
                    return


    def gameover(self):
        if not self.checkgame():
            self.var.set("Cat's game!!!")
            #print("Cat's game!!!")
        return

    def checkgame(self):
        for i in range(3):
            if self.buttons[i][1]["text"] == self.buttons[i][2]["text"] == self.buttons[i][0]["text"]!='':
                self.var.set("I win!!!")
                return True
            if self.buttons[1][i]["text"] == self.buttons[2][i]["text"]== self.buttons[0][i]["text"]!='':
                self.var.set("I win!!!")
                return True
        if self.buttons[1][1]["text"] == self.buttons[2][2]["text"] == self.buttons[0][0]["text"]!='':
            self.var.set("I win!!!")
            return True
        return False





root = Tk()
root.title("Tic Tac Toe")

board = TicTacToeBoard(root)
#board.pack(expand=1, fill=BOTH)
#board.grid(sticky = N + S + E + W)
board.grid()

root.mainloop()
#print("done")
