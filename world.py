import wumpus
import random
width = 5
blocks = set()
pits = set()
wum = set()
gold = set()
probability = [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #0.15 확률

for x in range(width+1):
    blocks.add((0, x))
    blocks.add((x, 0))
    blocks.add((width,x))
    blocks.add((x, width))

def set_pits():
    for x in range (2,width):
        for y in range(2,width):
            setPit = random.choice(probability)
            if setPit == 1:
                pits.add((x,y))

def set_wumpus():
    for x in range(2,width):
        for y in range(2,width):
            setWum = random.choice(probability)
            if setWum == 1:
                wum.add((x,y))

def set_gold():
    x = random.randrange(2,width)
    y = random.randrange(2,width)
    gold.add((x,y))

set_pits()
set_gold()
set_wumpus()
initial_location = (1,1)

world = wumpus.WumpusWorld(blocks = blocks, gold = gold, wumpus = wum, pits = pits, initial_location = initial_location)

