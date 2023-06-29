import queue
import hashlib
import pdb
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import deque
class tacanh:
    def __init__(self,size=3):

        self.size = size
        self.board_base = np.array(
            [
                [1,2,3],
                [4,5,6],
                [7,8,0]
            ]
        )
        self.target = np.array(
            [
            [1, 0, 3],
            [4, 2, 6],
            [7, 5,8]
            ]
        )
        self.board = np.copy(self.board_base)
        # x = np.arange(0,size*size)
        # random.shuffle(x)
        # self.board = x.reshape(size,size)
        # self.target = []
        # for i in range(size*size-1):
        #     self.target.append(i+1)


        # self.target.append(0)
        # self.target = np.array(self.target).reshape(size,size)
        self.zeros_base = np.array([np.where(self.board==0)[0].squeeze(),np.where(self.board==0)[1].squeeze()])

        self.board_targe = self.target
        self.target = self.hash_value(self.target)
        self.visited = []
        self.visited.append(self.hash_value(self.board))

        self.solvedfs = []

        self.reset()
        try:
            self.solve('dfs')
            cost = len(self.visited)
            self.reset()
            self.print()
            for ope in self.solvedfs:
                self.swap(ope)
                self.print()
            print(f"dfs costs {cost} move")
        except Exception as e :
            print('can t solve by dfs')
            pass
        self.reset()
        try:
            print("bfs solver")
            self.solve('bfs')
            bfs_solution = []
            bfs_solution.append(self.board_targe)
            son = self.target
            board = self.father.get(son)
            bfs_solution.append(board)

            while board is not None:
                son = self.hash_value(board)
                board = self.father.get(son)
                if board is not None:
                    bfs_solution.append(board)
            for board in bfs_solution[::-1]:
                self.board = board
                self.print()
            print(f"bfs costs {len(self.father)} move")
        except Exception as e:
                 print("can t solve by bfs")
        self.reset()

    def reset(self):
        self.board = np.copy(self.board_base)
        self.zeros = np.copy(self.zeros_base)
        self.visited = []
        self.visited.append(self.hash_value(self.board))
        self.father = {}
    def print(self):
        print("-------------------")
        for i in range(self.size):
            for j in range(self.size):
                print(self.board[i][j],end = " ")
            print()
    def check(self):
        if np.array_equal(self.board, self.target):
            return True
        return False
    def swap(self,ope):
        if ope == 'u':
            self.board[self.zeros[0]-1,self.zeros[1]],self.board[self.zeros[0],self.zeros[1]] = self.board[self.zeros[0],self.zeros[1]],self.board[self.zeros[0]-1,self.zeros[1]]
            self.zeros[0] -= 1
        elif ope == "d":
            self.board[self.zeros[0] + 1, self.zeros[1]], self.board[self.zeros[0], self.zeros[1]] = self.board[
                self.zeros[0], self.zeros[1]], self.board[self.zeros[0] + 1, self.zeros[1]]
            self.zeros[0] += 1
        elif ope == "r":
            self.board[self.zeros[0],self.zeros[1]+1] ,self.board[self.zeros[0],self.zeros[1]] = self.board[self.zeros[0],self.zeros[1]],self.board[self.zeros[0],self.zeros[1]+1]
            self.zeros[1] +=1
        elif ope == "l":
            self.board[self.zeros[0], self.zeros[1] - 1], self.board[self.zeros[0], self.zeros[1]] = self.board[
            self.zeros[0], self.zeros[1]], self.board[self.zeros[0], self.zeros[1] - 1]
            self.zeros[1] -= 1
    def get_ope(self):

        ope = {'u':1,'r':1,'l':1,'d':1}


        if self.zeros[0]==0:
            ope.pop('u')
        elif self.zeros[0]==self.size-1:
            ope.pop('d')
        if self.zeros[1] == 0:
            ope.pop('l')
        elif self.zeros[1] == self.size-1:
            ope.pop('r')
        ope1 = {}
        for action in ope.keys():
            if self.check_visited(action):
                ope1[action] = 1
        return ope1
    def check_visited(self,ope):
        boad = np.copy(self.board)
        zeros = np.copy(self.zeros)
        self.swap(ope)
        if self.hash_value(self.board) in self.visited:
            self.board = boad
            self.zeros = zeros
            return False
        self.board = boad
        self.zeros = zeros
        return True
    def solve(self,mode = 'dfs'):
        if mode == 'dfs':
            if self.target == self.hash_value(self.board):
                return True
            for ope in self.get_ope():
                zeros = np.copy(self.zeros)
                boad = np.copy(self.board)
                self.swap(ope)
                self.visited.append(self.hash_value(self.board))
                self.solvedfs.append(ope)
                if self.solve():
                    return True
                self.zeros = zeros
                self.board = boad
                self.solvedfs.pop()
            return False
        if mode == 'bfs':
            l = []
            l+=self.get_next_state([self.board,self.zeros])
            while(len(l)!=0):
                state = l.pop(0)
                if self.hash_value(state[0]) == self.target:
                    break
                l+=self.get_next_state(state)

    def get_next_state(self,state):
        l = []

        board,zeros = state
        self.board = np.copy(board)
        self.zeros = np.copy(zeros)

        for ope in  list(self.get_ope().keys()):

            old_board2 = np.copy(self.board)
            old_zeros2 = np.copy(self.zeros)

            self.swap(ope)

            hash_value = self.hash_value(self.board)
            self.father[hash_value] = np.copy(board)
            self.visited.append(hash_value)

            l.append([self.board,self.zeros])

            self.board = old_board2
            self.zeros = old_zeros2

        return l


    def hash_value(self,board):
        new_board  = np.copy(board)
        new_board = new_board.tobytes()
        hash_value = hashlib.md5(new_board).hexdigest()

        # Convert the hash value to an integer
        hash_integer = int(hash_value, 16)

        # Ensure the integer is within the desired range
        return hash_integer
