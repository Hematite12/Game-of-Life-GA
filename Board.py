import random

class Board:
    DIM = 120
    CELLDIM = 7
    NUMSEEDS = 50
    BOXDIM = 10
    MARGIN = (DIM-BOXDIM)/2
    
    def makeNineActive(self, board, x, y):
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                board[i][j] = True
    
    def __init__(self, inBoard=[], inBoardInert=[]):
        if inBoard==[]:
            self.b1 = [[False for i in range(Board.DIM)] for j in range(Board.DIM)]
            self.bInert = [[False for i in range(Board.DIM)] for j in range(Board.DIM)]
            seeds = 0
            while seeds < Board.NUMSEEDS:
                x = random.randrange(Board.MARGIN, Board.DIM-Board.MARGIN)
                y = random.randrange(Board.MARGIN, Board.DIM-Board.MARGIN)
                if not self.b1[x][y]:
                    self.b1[x][y] = True
                    self.makeNineActive(self.bInert, x, y)
                    seeds += 1
        else:
            self.b1 = inBoard
            self.bInert = inBoardInert
        self.b2 = [row[:] for row in self.b1]
        self.bInitial = [row[:] for row in self.b1]
        self.bInitialInert = [row[:] for row in self.bInert]
        self.fitness = 0
    
    def reset(self):
        self.b1 = [row[:] for row in self.bInitial]
        self.b2 = [row[:] for row in self.bInitial]
        self.bInert = [row[:] for row in self.bInitialInert]
    
    def showBoard(self):
        for i in range(Board.DIM):
            for j in range(Board.DIM):
                if self.b1[i][j]:
                    fill(0, 0, 255)
                else:
                    fill(255)
                rect(i*Board.CELLDIM+5,j*Board.CELLDIM+5,Board.CELLDIM,Board.CELLDIM)
    
    def sumNine(self, board, x, y):
        sum = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if board[i][j]:
                    sum += 1
        return sum
    
    def updateInerts(self):
        for i in range(1, Board.DIM-1):
            for j in range(1, Board.DIM-1):
                self.bInert[i][j] = False

    def updateBoard(self):
        changes = []
        for i in range(1, Board.DIM-1):
            for j in range(1, Board.DIM-1):
                if self.bInert[i][j]:
                    num = self.sumNine(self.b1, i, j)
                    if self.b1[i][j]:
                        if num<3 or num>4:
                            self.b2[i][j] = False
                            changes.append([False, i, j])
                    else:
                        if num==3:
                            self.b2[i][j] = True
                            changes.append([True, i, j])
        self.updateInerts()
        for change in changes:
            self.b1[change[1]][change[2]] = change[0]
            self.makeNineActive(self.bInert, change[1], change[2])
    
    def flipState(self, x, y):
        if self.b1[x][y]:
            self.b1[x][y] = False
            self.b2[x][y] = False
            self.bInitial[x][y] = False
        else:
            self.b1[x][y] = True
            self.b2[x][y] = True
            self.bInitial[x][y] = True
    
    def getCopy(self):
        newb1 = [row[:] for row in self.bInitial]
        newbInitial = [row[:] for row in self.bInitial]
        return Board(newb1, newbInitial)
    
    def mutate(self, mutProb):
        for i in range(Board.MARGIN, Board.DIM-Board.MARGIN):
            for j in range(Board.MARGIN, Board.DIM-Board.MARGIN):
                if random.random() < mutProb:
                    self.flipState(i, j)
    
    def checkForPatterns(self, pattern):
        pWidth = len(pattern[0])
        pHeight = len(pattern)
        sum = 0
        for i in range(Board.DIM-pWidth):
            for j in range(Board.DIM-pHeight):
                isPattern = True
                for x in range(i, i+pWidth):
                    for y in range(j, j+pHeight):
                        pVal = pattern[y-j][x-i]
                        if pVal!=None and pVal!=self.b1[x][y]:
                            isPattern = False
                            break
                    else:
                        continue
                    break
                if isPattern:
                    sum += 1
        return sum
    
    def calcFitness(self, numSteps, patterns=[]):
        for i in range(numSteps):
            self.updateBoard()
        sum = 0
        for i in range(1, Board.DIM-1):
            for j in range(1, Board.DIM-1):
                if self.b1[i][j]:
                    sum += 1
        self.fitness = sum
        if isinstance(patterns, tuple):
            pSum = 0
            for pattern in patterns:
                pSum += self.checkForPatterns(pattern)
            self.fitness *= sum
        else:
            self.fitness *= self.checkForPatterns(patterns)