import random
from Board import *
from Patterns import *

POPSIZE = 50
MUTPROB = .04
NUMSTEPS = 100
NUMGENS = 10
FRACTIONKEPTALIVE = 3
USEDPATTERN = BLINKERS

def generate():
    popL = []
    for i in range(POPSIZE):
        popL.append(Board())
    return popL

def mutateAll(popL):
    for board in popL:
        board.mutate(MUTPROB)

def calcFitnesses(popL):
    for board in popL:
        if USEDPATTERN != None:
            board.calcFitness(NUMSTEPS, USEDPATTERN)
        else:
            board.calcFitness(NUMSTEPS)

def makePopFitL(popL):
    calcFitnesses(popL)
    popL.sort(key = lambda x: x.fitness, reverse=True)

def makePopPool(popL):
    popPool = []
    initialCount = len(popL)//FRACTIONKEPTALIVE
    for i in range(len(popL)):
        if initialCount > 0:
            for j in range(initialCount):
                popPool.append(popL[i])
            initialCount -= 1
    return popPool

def evolve():
    popL = generate()
    for i in range(NUMGENS):
        makePopFitL(popL)
        print(popL[0].fitness)
        popL = popL[:len(popL)//FRACTIONKEPTALIVE]
        popPool = makePopPool(popL)
        newPop = []
        for i in range(POPSIZE):
            choice = random.choice(popPool)
            newPop.append(choice.getCopy())
        mutateAll(newPop)
        popL = newPop
    makePopFitL(popL)
    return popL[0]