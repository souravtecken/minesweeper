from graphics import *

gridSize=8
tileWidth=100

window= GraphWin("Minesweeper",tileWidth*gridSize,tileWidth*gridSize)


class Tile:
    def __init__(self, x, y, value=0):
        self.x=x
        self.y=y
        self.topLeft=Point(self.x-tileWidth//2, self.y-tileWidth//2)
        self.bottomRight=Point(self.x+tileWidth//2, self.y+tileWidth//2)
        self.val=value        

    def drawTile(self):
        r=Rectangle(self.topLeft,self.bottomRight) 
        r.draw(window)

tiles=[[Tile(tileWidth*j+tileWidth//2,tileWidth*i+tileWidth//2,i*gridSize+j) for j in range(gridSize)] for i in range(gridSize)]   

def drawGrid(tiles):
    for tileRow in tiles:
        for tile in tileRow:
            tile.drawTile()

drawGrid(tiles)

window.getMouse()
window.close()