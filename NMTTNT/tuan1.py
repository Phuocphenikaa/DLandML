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
        self.target = np.array(
            [
                [0,1,2],
                [3,4,5],
                [6,7,8]
            ]
        )
        self.board_base= np.array(
            [
                [3, 1, 0],
                [6, 5, 2],
                [7, 4, 8]
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
        self.visited2 = {}
        self.visited2[self.hash_value(self.board)] = 1

        self.solvedfs = []

        self.reset()
        text = '''
        ---Select type of solver---
        1.Dfs
        2.Bfs
        3.Dfs with max deep
        4.Deep recursive search
        6.Show target and source
        ---Any other key for exit!---
        '''
        while True:
            option = input(text)
            if option == '1':
                try:
                    self.solve('dfs')
                    cost = len(self.visited2)
                    print(f"dfs costs {cost} move")
                    ok = input("Do you want to show results:(y/n)")
                    if ok == 'y':
                        self.board = np.copy(self.board_base)
                        self.zeros = np.copy(self.zeros_base)
                        self.print()
                        for ope in self.solvedfs:
                            self.swap(ope)
                            self.print()

                except Exception as e :
                    print(e)
                    pass
            elif option == '2':
                self.reset()
                try:
                    print("bfs solver")
                    self.solve('bfs')
                    print(f"bfs costs {len(self.father)} move")
                    ok = input("Do you want to show result:(y/n)")
                    if ok =='y':
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
                except Exception as e:
                    print(e)
            elif option =='3':
                self.reset()
                try:
                    n = int(input("nhap vao so n"))
                    print("deep n search")
                    if self.solve_deep_n(n_max= n):

                        cost = len(self.visited2)

                        print(f"deep n search costs {cost}")
                        ok = input("Do you want to show result:(y/n)")
                        if ok == 'y':
                            self.board = np.copy(self.board_base)
                            self.zeros = np.copy(self.zeros_base)
                            self.print()
                            for ope in self.solvedfs:
                                self.swap(ope)
                                self.print()
                    else:
                        print(f"can t solve by deep = {n} search")
                except Exception as e:
                    print(e)
                    print(f"can t solve by deep  search")
            elif option =='4':
                self.reset()
                print("deep recursive")


                try:
                    flag, i = self.deep_recusive_search()

                    if flag:
                        print(f"Solve with first deep {i}")
                        print(f"Solve with cost {len(self.visited2)}")
                        ok = input("Do you want to show result:(y/n)")
                        if ok == 'y':
                            self.board = np.copy(self.board_base)
                            self.zeros = np.copy(self.zeros_base)
                            self.print()
                            for ope in self.solvedfs:
                                self.swap(ope)
                                self.print()

                    else:
                        print("Cant solve with deep_recusive_search")
                except Exception as e:
                    print(e)
                    print('can t slove by deep recursive search')
            elif option == '6':
                self.show_source_and_destination()
            else:
                break


    def reset(self):
        self.board = np.copy(self.board_base)
        self.zeros = np.copy(self.zeros_base)
        self.father = {}
        self.solvedfs = []
        self.visited2  = {self.hash_value(self.board):1}
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
        if self.visited2.get(self.hash_value(self.board)) is not None:
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
                self.visited2[self.hash_value(self.board)] = 1
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
            self.visited2[hash_value] = 1

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
    def solve_deep_n(self,n  = 0,n_max = 5):

        if self.target == self.hash_value(self.board):
            return True
        if n>n_max:
            return False
        for ope in self.get_ope():
            zeros = np.copy(self.zeros)
            boad = np.copy(self.board)
            self.swap(ope)
            self.visited2[self.hash_value(self.board)] = 1
            self.solvedfs.append(ope)
            if self.solve_deep_n(n+1,n_max):
                return True
            self.zeros = zeros
            self.board = boad
            self.solvedfs.pop()
        return False
    def show_source_and_destination(self):
        size = self.board.shape[0]
        print('source')
        for i in range(size):
            print("")
            for j in range(size):
                print(self.board_base[i,j],end = " ")
        print("\ntarget")
        for i in range(size):
            print("")
            for j in range(size):
                print(self.board_targe[i,j], end=" ")
    def deep_recusive_search(self,max = 20):
        for i in range(max):
            if self.solve_deep_n(0,i):
                return True,i
            else:
                self.reset()
        return False,max
    def get_score(self,board):
        score = 0
        for i in range(self.size):
            for j in range(self.size):
                score += abs(board[i,j]-(i*3+j))
        return score


    def get_ope_heritic(self):
        ope = {'u': 1, 'r': 1, 'l': 1, 'd': 1}

        if self.zeros[0] == 0:
            ope.pop('u')
        elif self.zeros[0] == self.size - 1:
            ope.pop('d')
        if self.zeros[1] == 0:
            ope.pop('l')
        elif self.zeros[1] == self.size - 1:
            ope.pop('r')
        ope1 = {}
        for action in ope.keys():
            flag ,score = self.check_visited_heritic(action)

            if flag:
                ope1[action] = score
        return ope1
    def check_visited_heritic(self,ope):
        boad = np.copy(self.board)
        zeros = np.copy(self.zeros)
        self.swap(ope)
        if self.visited2.get(self.hash_value(self.board)) is not None:
            self.board = boad
            self.zeros = zeros
            return False,0
        score = self.get_score(self.board)
        hash_value = self.hash_value(self.board)
        self.visited2[hash_value] = 1
        self.board = boad
        self.zeros = zeros
        return True,score
    def heritic_search(self,n_deep,n_max ):
        if self.hash_value(self.board) == self.target:
            return True
        if n_deep>n_max:
            return False
        for ope in self.get_ope_heritic().keys():
            board = np.copy(self.board)
            zeros = np.copy(self.zeros)

            self.swap(ope)
            if self.heritic_search(n_deep+1,n_max):
                return True
            self.board = board
            self.zeros = zeros
        return False



