# -*- coding: utf-8 -*-
import numpy as np
from tkinter import *
from random import randint
from copy import deepcopy
import math


def norm_func(x):             
    return 1.0/(1+math.exp(-x))   #sigmoïde
    
def der_norm_func(x):
    y = math.exp(-x)               #dérivée de la sigmoïde
    return y/(1+y)**2


    
    
class App():
    def __init__(self, parent):
        self.root = parent
        self.quizzes = np.load('C:\\Users\\Hugo\\Documents\\python\\Sudoku\\sudoku.npy') 
        self.pixels = 50
        self.width = 9*self.pixels
        self.gameframe = Frame(self.root)
        self.gameframe.pack()
        self.canvas = Canvas(self.gameframe, width=self.width, height=self.width, bg='white')
        self.canvas.pack()
        self.new_game()
        self.buttonframe = Frame(self.root)
        self.buttonframe.pack()
        AIb = Button(self.buttonframe, text="AI", command=self.IA)
        AIb.pack(side=RIGHT, pady=20, padx=20)
        restartb = Button(self.buttonframe, text="Restart", command=self.restart)
        restartb.pack(side=RIGHT, pady=20, padx=20)
        newgameb = Button(self.buttonframe, text="New game", command=self.new_game)
        newgameb.pack(side=RIGHT, pady=20, padx=20)
        checkvictoryb = Button(self.buttonframe, text="Check victory", command=self.check_victory)
        checkvictoryb.pack(side=RIGHT, pady=20, padx=20)
        
    def run(self):
        self.root.mainloop()
        
    def restart(self):
        self.entries = [[0 for i in range(9)] for j in range(9)] 
        self.canvas.delete("all")
        for x in range(9):
            for y in range(9):
                if self.table[x][y]!=0:
                    self.canvas.create_text(x*self.pixels+self.pixels/2, y*self.pixels+self.pixels/2, text=self.table[x][y], font="Arial 16", fill="black")
                else:
                    self.entries[x][y] = Entry(self.canvas, bd=0, fg='#777', font="Arial 16", justify='center')
                    self.canvas.create_window(x*self.pixels+self.pixels/2, y*self.pixels+self.pixels/2, height=0.9*self.pixels, width=0.9*self.pixels, window=self.entries[x][y], tag='entryx'+str(x)+'y'+str(y))
        for i in [1,2,4,5,7,8]:
            self.canvas.create_line(i*self.pixels, 0, i*self.pixels, self.width, fill='gray')
            self.canvas.create_line(0, i*self.pixels, self.width, i*self.pixels, fill='gray')
        for i in [0,3,6,9]:
            self.canvas.create_line(i*self.pixels, 0, i*self.pixels, self.width, fill='black')
            self.canvas.create_line(0, i*self.pixels, self.width, i*self.pixels, fill='black')
        
    def new_game(self):
        self.index = randint(0,1000000)
        self.table = self.quizzes[self.index][0]
        self.solution = self.quizzes[self.index][1]
        self.restart()
        
    def check_victory(self):
        table_act = deepcopy(self.table)
        for x in range(9):
            for y in range(9):
                if table_act[x][y]==0:
                    table_act[x][y] = int(self.entries[x][y].get()) if self.entries[x][y].get()!='' else 0
        if np.array_equal(table_act,self.solution):
            self.new_game()
        else:
            print "Erreur"
            
    def IA(self):
        table_act = deepcopy(self.table)
        for i in range(100):
            while True:
                table_act = deepcopy(self.table)
                for x in range(9):
                    for y in range(9):
                        if table_act[x][y]==0:
                            table_act[x][y] = int(self.entries[x][y].get()) if self.entries[x][y].get()!='' else 0
                for x,column in enumerate(table_act):
                    for y,case in enumerate(column):
                        if case==0:
                            row = table_act[:,y]
                            carre = table_act[np.ix_([3*(x/3),3*(x/3)+1,3*(x/3)+2],[3*(y/3),3*(y/3)+1,3*(y/3)+2])]
                            
                            in_column = range(1,10)
                            in_row = range(1,10)
                            in_carre = range(1,10)
                            possible = range(1,10)
                            for i in range(1,10):
                                if i in column:
                                    in_column.remove(i)
                                if i in row:
                                    in_row.remove(i)
                                if i in np.reshape(carre,9):
                                    in_carre.remove(i)
                                if i in column or i in row or i in np.reshape(carre,9):
                                    possible.remove(i)
                            if len(in_column)==1 and table_act[x][y]==0:
                                self.entries[x][y].insert(0,in_column[0])
                                table_act[x][y] = in_column[0]
                            if len(in_row)==1 and table_act[x][y]==0:
                                self.entries[x][y].insert(0,in_row[0])
                                table_act[x][y] = in_row[0]
                            if len(in_carre)==1 and table_act[x][y]==0:
                                self.entries[x][y].insert(0,in_carre[0])
                                table_act[x][y] = in_carre[0]
                            if len(possible)==1 and table_act[x][y]==0:
                                self.entries[x][y].insert(0,possible[0])
                                table_act[x][y] = possible[0]
                self.root.update()
                if 0 not in np.reshape(table_act,81):
                    self.check_victory()
                    break
                        
        
        
        
app = App(Tk())
app.run()