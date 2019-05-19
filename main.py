from graphics import *
from random import choice

gridSize=8
tileWidth=100
numberOfMines=10
unclickedColor="grey"
clickedColor="white"
window= GraphWin("Minesweeper",tileWidth*gridSize,tileWidth*gridSize)


class Tile:
    def __init__(self, x, y, value=0):
        self.x=x
        self.y=y
        self.topLeft=Point(self.x-tileWidth//2, self.y-tileWidth//2)
        self.bottomRight=Point(self.x+tileWidth//2, self.y+tileWidth//2)
        self.val=value    
        self.clicked=False            

    def drawTile(self):
        r=Rectangle(self.topLeft,self.bottomRight)         
        r.setFill(unclickedColor)        
        if self.clicked:
            r.setFill(clickedColor)            
        if self.val:
            if self.val>8:
                self.val='M'
        t=Text(Point(self.x,self.y),self.val)
        r.draw(window)
        if self.clicked and self.val:        
            t.draw(window)        
                            
tiles=[[Tile(tileWidth*j+tileWidth//2,tileWidth*i+tileWidth//2, 0) for j in range(gridSize)] for i in range(gridSize)]   

def findNeighbours(tiles, i, j, callback):
    neighbours=list()
    if i>0:
        neighbours.append((i-1,j))        
        if j>0:
            neighbours.append((i-1,j-1))                   
        if j<gridSize-1:
            neighbours.append((i-1,j+1))            
    if i<gridSize-1:
        neighbours.append((i+1,j))        
        if j>0:
            neighbours.append((i+1,j-1))            
        if j<gridSize-1:
            neighbours.append((i+1,j+1))            
    if j>0:
        neighbours.append((i,j-1))        
    if j<gridSize-1:
        neighbours.append((i,j+1))

    if callback==increment:    
        callback(tiles, neighbours)        
    else:
        callback(tiles,i,j,neighbours)
        
def increment(tiles,neighbours):
    for pair in neighbours:
        tiles[pair[0]][pair[1]].val+=1

def initTileValues(tiles):
    tileNumbers=list(range(gridSize*gridSize))
    for __ in range(numberOfMines):
        tileNumber=choice(tileNumbers)
        tileNumbers.remove(tileNumber)
        i=tileNumber//gridSize
        j=tileNumber%gridSize
        tiles[i][j].val=9
        findNeighbours(tiles, i, j, increment)

def drawGrid(tiles):
    for tileRow in tiles:
        for tile in tileRow:
            tile.drawTile()

def findClickedIndex(clickedPoint):
    i=int(clickedPoint.y//tileWidth)
    j=int(clickedPoint.x//tileWidth)
    if i<gridSize and j<gridSize:
        return i,j
    return False,False

def propogate(tiles, i, j, neighbours):
    tiles[i][j].clicked=True
    tiles[i][j].drawTile()
    if tiles[i][j].val==0:
        for pair in neighbours:
            if tiles[pair[0]][pair[1]].clicked==False:
                findNeighbours(tiles,pair[0],pair[1],propogate)
    


def play():
    initTileValues(tiles)
    drawGrid(tiles)
    while True:
        clickedPoint=window.getMouse()
        i,j=findClickedIndex(clickedPoint)
        if tiles[i][j].val=='M':
            print("Game Over.")
            break
        else:
            findNeighbours(tiles,i,j,propogate)


play()


window.close()