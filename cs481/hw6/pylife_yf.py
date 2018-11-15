#!  /usr/bin/env python3
from tkinter import *
from time import sleep
class CellCanvas(Canvas):
	def __init__(self,parent=None):
		super().__init__(parent,width=197,height=197,bg='white')
		self.arr = CellArray()
		self.bind("<Button-1>", self.paint)


	def paint(self,event):
		i = event.x//10
		j = event.y//10
		x1, y1 = (i*10), (j*10)
		x2, y2 = (x1+10), (y1+10)
		self.create_rectangle(x1, y1, x2, y2, fill="black")
		self.arr.currentArray[i+1][j+1]=1

	def updateCanvas(self):
		self.delete("all")
		self.arr.updateArray()
		for i in range(1,22):
			for j in range(1,22):
				if self.arr.currentArray[i][j]==1:
					x1, y1 = ((i-1)*10), ((j-1)*10)
					x2, y2 = (x1+10), (y1+10)
					self.create_rectangle(x1, y1, x2, y2, fill="black")

	def clearCanvas(self):
		self.delete("all")
		self.arr = CellArray()

class CellArray():
	def __init__(self):
		self.currentArray = [([0] * 22) for i in range(22)]
		self.arrayList = []
		self.arrayList.append(self.currentArray)

	def updateArray(self):
		newArray = [([0] * 22) for i in range(22)]
		self.updateBoard()
		for i in range(1,21):
			for j in range(1,21):
				newArray[i][j]=self.checkCell(i,j)

		self.arrayList.append(newArray)
		self.currentArray=newArray
		self.updateBoard()

	def updateBoard(self):
		for i in (0,21):
			for j in range(1,21):
				self.currentArray[i][j] = self.currentArray[abs(i-20)][j]
				self.currentArray[j][i] = self.currentArray[j][abs(i-20)]


	def checkCell(self,x,y):
		count = 0
		for i in (-1,0,1):
			for j in (-1,0,1):
				if self.currentArray[x+i][y+j]== 1:
					count+=1

		if self.currentArray[x][y]==1:
			count-=1
			if count<2 or count>3:
				return 0
			else:
				return 1

		if self.currentArray[x][y]==0:
			if count==3:
				return 1
			else:
				return 0

def creatWidget(root):

	reverseButton=Button(root,text='<<',command=canvas.updateCanvas)
	stepBackwarkButton=Button(root,text='<-',command=canvas.updateCanvas)
	stepForwarkButton=Button(root,text='->',command=canvas.updateCanvas)
	ForwardButton=Button(root,text='>>',command=trickit_controller)

	speedScale=Scale(root,from_=1,to=10,resolution=1,orient=HORIZONTAL,variable=speed)

	clearButton=Button(root,text='Clear',command=canvas.clearCanvas)
	quitButton=Button(root,text='Quit',command=root.quit)

	speedScale.grid(row=2,column=1,columnspan=8)

	reverseButton.grid(row=3,column=1,columnspan=2)
	stepBackwarkButton.grid(row=3,column=3,columnspan=2)
	stepForwarkButton.grid(row=3,column=5,columnspan=2)
	ForwardButton.grid(row=3,column=7,columnspan=2)

	clearButton.grid(row=4,column=5,columnspan=2)
	quitButton.grid(row=4,column=7,columnspan=2)

def trickit_controller():
	global isRun
	if isRun:
		isRun=False
	else:
		isRun=True
		trickit()

def trickit():
	global isRun
	if isRun:
		canvas.updateCanvas()
		root.after(1200-int(speed.get())*100,trickit)

isRun = False

root = Tk()
root.title("Life")
speed=StringVar()
canvas = CellCanvas(root)
canvas.grid(row=1,column=1,columnspan=8)
creatWidget(root)

root.mainloop()
