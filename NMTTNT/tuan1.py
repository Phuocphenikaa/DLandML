import numpy as np
import random
class tacanh:
    def __init__(self,size=3):
        self.size = size
        x = np.arange(0,size*size)
        random.shuffle(x)
        self.board = x.reshape(size,size)
        self.zeros = np.array([np.where(self.board==0)[0].squeeze(),np.where(self.board==0)[1].squeeze()])
    def print(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.board[i][j],end = " ")
            print()
    def swap(self,ope):
        if ope == 'u':
            if self.zeros[0] == 0:
                print("Can't up")
                return
            print("up")
            self.board[self.zeros[0]-1,self.zeros[1]],self.board[self.zeros[0],self.zeros[1]] = self.board[self.zeros[0],self.zeros[1]],self.board[self.zeros[0]-1,self.zeros[1]]
            self.zeros[0] -= 1
        elif ope == "d":
            if self.zeros[0] == self.size-1:
                print("Can't down")
                return
            print("down")
            self.board[self.zeros[0] + 1, self.zeros[1]], self.board[self.zeros[0], self.zeros[1]] = self.board[
                self.zeros[0], self.zeros[1]], self.board[self.zeros[0] + 1, self.zeros[1]]
            self.zeros[0] += 1
        elif ope == "r":
            if self.zeros[1] == self.size-1:
                print("Cant' right")
                return
            print("Right")
            self.board[self.zeros[0],self.zeros[1]+1] ,self.board[self.zeros[0],self.zeros[1]] = self.board[self.zeros[0],self.zeros[1]],self.board[self.zeros[0],self.zeros[1]+1]
            self.zeros[1] +=1
        elif ope == "l":
            if self.zeros[1] == 0:
                print("cant' left")
                return
            print("left")
            self.board[self.zeros[0], self.zeros[1] - 1], self.board[self.zeros[0], self.zeros[1]] = self.board[
            self.zeros[0], self.zeros[1]], self.board[self.zeros[0], self.zeros[1] - 1]
            self.zeros[1] -= 1
        self.print()

class dongnuoc:
    def __init__(self,vx = 3,vy = 5, z = 4):
        self.vx = 0
        self.vy = 0
        self.z = z
        self.xmax = vx
        self.ymax = vy
    def donuoc(self,binh = 'y',mode = 'them'):
        if binh=='x':
            if mode == 'them':
                self.vx = self.xmax
                print("them nuoc binh x")
            else:
                self.vx = 0
                print("do nuoc binh x")
        else:
            if mode == 'them':
                self.vy = self.ymax
                print("them nuoc binh y")
            else:
                self.vy = 0
                print("do nuoc binh y")

        self.print()
    def print(self):
        print(f"vx: {self.vx}, vy:{self.vy}")
    def swap(self,source = 'x'):
        if source == 'x':
            du = self.ymax- self.vy
            if du>self.vx:
                self.vy += self.vx
                self.vx = 0
            else:
                self.vy = self.ymax
                self.vx -= du
        else:
            du = self.xmax-self.vx
            if du>self.vy:
                self.vx += self.vy
                self.vy = 0
            else:
                self.vx = self.xmax
                self.vy -= du
        self.print()
    def check(self):
        if self.vx == self.z or self.vy == self.z:
            return True
        return False




