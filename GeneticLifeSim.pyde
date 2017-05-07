import random
from Board import *
from Genetics import *

FRAMERATE = 200
THREAD = "ON"

def setup():
    global bestBoard
    bestBoard = evolve()
    bestBoard.reset()
    size(Board.DIM*Board.CELLDIM+10, Board.DIM*Board.CELLDIM+10)
    background(0)
    frameRate(FRAMERATE)

def keyPressed():
    global bestBoard, THREAD
    if key == "r":
        bestBoard.reset()
        THREAD = "OFF"
    if key == " ":
        if THREAD == "OFF":
            THREAD = "ON"
        else:
            THREAD = "OFF"

def draw():
    bestBoard.showBoard()
    if THREAD == "ON":
        bestBoard.updateBoard()