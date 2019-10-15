from enum import Enum
import random
import math
import queue

class Board:

    #constructor for board
    #puts board into 2D array
    def __init__(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        lines = [list(x.strip()) for x in lines]
        self.maze = []

        for row in lines:
            r = []
            for i in row:
                if (i != " "):
                    r.append(int(i))
            self.maze.append(r)
        #find the start
        self.start = [0]
        self.finish = [0]
        self.height = len(lines) #each line is a row
        self.width = len(self.maze[0]) #length of one row is the width
        i = 0
        for x in self.maze[len(self.maze) - 1]:
            if (x == 0):
                self.start = [i, len(self.maze) - 1]
                break
            i += 1
        #find the finish
        #look at top row...
        i = 0
        for x in self.maze[0]:
            if (x == 0):
                self.finish = [i, 0]
                break
            i += 1
        #look at sides (if not found already)
        if (len(self.finish) == 1):
            for y in range(0, len(self.maze) - 1):
                if (self.maze[y][0] == 0):
                    self.finish = [0, y]
                    break
                if (self.maze[y][len(self.maze) - 1] == 0):
                    self.finish = [len(self.maze) - 1, y]
                    break
        f.close()

    #to string method
    def toString(self):
        for row in self.maze:
            s = ""
            for i in row:
                s = s + str(i)
            print(s)

    #sends back 0 or 1
    def isWall(self, posx, posy):
        return self.maze[posy][posx]

    #sets spot on board to show where path is (for drawing results)
    def drawPath(self, posx, posy):
        self.maze[posy][posx] = "#"

class Robot:
    def __init__(self, x, y, board=None):
        self.x = x
        self.y = y
        self.board = board
        self.decisions = {}
        self.path=[]

    #makes key out of x and y to put into dictionary (key for dict)
    def hashcode(self, x , y):
        return ((x * x) + (3 * x) + (2 * x * y) + (y * y)) / 2

    #diff find neighbors method, doesn't use robot
    def findNeighbors(self,x,y):
        neighbors = []
        if(y != (self.board.height - 1) and self.board.isWall(x, y + 1) == 0):
            neighbors.append([x, y + 1])
        if(y != 0 and self.board.isWall(x, y - 1) == 0):
            neighbors.append([x, y - 1])
        if(x != 0 and self.board.isWall(x - 1, y) == 0):
            neighbors.append([x - 1, y])
        if(x != (self.board.width - 1) and self.board.isWall(x + 1, y) == 0):
            neighbors.append([x + 1, y])
        return neighbors

    #heuristic (spot to goal)
    def h(self, x, y):
        return abs(x - self.board.finish[0]) + abs(y - self.board.finish[1])

    #A* implementation, finds path to maze
    def solve(self):
        if((self.board.finish[0] == None) or (self.board.finish[1] == None)):
            return False,[]
        Q = queue.PriorityQueue()  #Q as in "Queue"
        Q.put([self.x, self.y], 0+self.h(self.x,self.y))  #adds start pos to queue
        prev = dict()  #maps the posent tile to the tile it came from (or the previous tile)
        g = dict()  #g hat, or the cost from the start to this coordinate (it's incremented by 1 each tile movement
        f = dict()   #f hat, an approximation from start, to this spot, to the goal
        prev[self.hashcode(self.x, self.y)] = None   #this is because theres nothing before the start pos
        g[self.hashcode(self.x, self.y)] = 0   #g hat for start pos
        found = False
        while not(Q.empty()):
           pos = Q.get()  #takes off from the queue
           if(pos[0] == self.board.finish[0] and pos[1] == self.board.finish[1]):  #found exit cond.
               found = True
           cost = g[self.hashcode(pos[0], pos[1])] + 1
           for neighbor in self.findNeighbors(pos[0], pos[1]):
               if (self.hashcode(neighbor[0], neighbor[1]) not in g.keys()) or (cost < g[self.hashcode(neighbor[0], neighbor[1])]):  
                   g[self.hashcode(neighbor[0], neighbor[1])] = cost
                   f[self.hashcode(neighbor[0], neighbor[1])] = cost + self.h(neighbor[0], neighbor[1])
                   Q.put(neighbor, f[self.hashcode(neighbor[0], neighbor[1])])
                   prev[self.hashcode(neighbor[0], neighbor[1])] = [pos[0], pos[1]] #pos will be connected to all neighbors
        if(found):
            trace = [self.board.finish[0], self.board.finish[1]]   #traceback, iterator that goes through the path used to get to finish
            while trace != None:  #when trace is none, that means its back at the start
                self.path.insert(0, trace)  #shoves spot into the beginning of insert, so it will be in reverse (cuz its traceback)
                self.board.drawPath(trace[0], trace[1])  #draws path
                trace = prev[self.hashcode(trace[0], trace[1])]  #find next position according to prev
            return True, self.path
        else:
            return False, []


board = Board("board_small.txt")
rob = Robot(board.start[0], board.start[1],board)
result1, result2 = rob.solve()
print(str(result1),str(result2))
board.toString()
