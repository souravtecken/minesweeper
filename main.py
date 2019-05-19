from graphics import *
from random import choice

unclickedColor="grey"
clickedColor="white"
windowHeight=900

class Tile:    
    def __init__(self, x, y, value=0, width=100):
        self.x=x
        self.y=y
        self.width=width
        self.topLeft=Point(x-width//2, y-width//2)
        self.bottomRight=Point(x+width//2, y+width//2)
        self.val=value    
        self.mine=False
        self.clicked=False
        self.flagged=False            

    def drawTile(self, window):
        r=Rectangle(self.topLeft,self.bottomRight)         
        r.setFill(unclickedColor)        
        if self.clicked:
            r.setFill(clickedColor)                    
        t=Text(Point(self.x,self.y),self.val)        
        if self.flagged:            
            t=Text(Point(self.x,self.y),'F')
        r.draw(window)
        if self.clicked and self.val or self.flagged:        
            t.draw(window)        
                            


class Minesweeper:
    def __init__(self, gridSize):        
        self.flags=0
        self.clickedTiles=0
        self.gridSize=gridSize
        self.tileWidth=windowHeight//gridSize
        self.numberOfMines=10
        self.tiles=[[Tile(self.tileWidth*j + self.tileWidth//2, self.tileWidth*i + self.tileWidth//2, 0, self.tileWidth)
                                                     for j in range(gridSize)] for i in range(gridSize)]   
        self.window= GraphWin("Minesweeper",self.tileWidth*self.gridSize,self.tileWidth*gridSize)        

    def drawGrid(self):
        for tileRow in self.tiles:
            for tile in tileRow:
                tile.drawTile(self.window)

    def increment(self, neighbours):
        for pair in neighbours:
            self.tiles[pair[0]][pair[1]].val+=1

    def findNeighbours(self, i, j, callback):
        neighbours=list()
        if i>0:
            neighbours.append((i-1,j))        
            if j>0:
                neighbours.append((i-1,j-1))                   
            if j<self.gridSize-1:
                neighbours.append((i-1,j+1))            
        if i<self.gridSize-1:
            neighbours.append((i+1,j))        
            if j>0:
                neighbours.append((i+1,j-1))            
            if j<self.gridSize-1:
                neighbours.append((i+1,j+1))            
        if j>0:
            neighbours.append((i,j-1))        
        if j<self.gridSize-1:
            neighbours.append((i,j+1))

        if callback==self.increment:    
            callback(neighbours)        
        else:
            callback(i,j,neighbours)

    def initTileValues(self):
        tileNumbers=list(range(self.gridSize*self.gridSize))
        for __ in range(self.numberOfMines):
            tileNumber=choice(tileNumbers)
            tileNumbers.remove(tileNumber)
            i=tileNumber//self.gridSize
            j=tileNumber%self.gridSize
            self.tiles[i][j].mine=True
            self.findNeighbours(i, j, self.increment)

    def propagate(self, i, j, neighbours):
        self.tiles[i][j].clicked=True
        self.clickedTiles+=1
        if self.tiles[i][j].flagged==True:
            self.tiles[i][j].flagged=False
            self.flags-=1
        self.tiles[i][j].drawTile(self.window)
        if self.tiles[i][j].val==0 and self.tiles[i][j].mine==False:
            for pair in neighbours:
                if self.tiles[pair[0]][pair[1]].clicked==False:
                    self.findNeighbours(pair[0],pair[1],self.propagate)

    def findClickedIndex(self, clickedPoint):
        i=int(clickedPoint.y//self.tileWidth)
        j=int(clickedPoint.x//self.tileWidth)
        if i<self.gridSize and j<self.gridSize:
            return i,j
        return False,False        

    def play(self):
        self.initTileValues()
        self.drawGrid()
        while not self.clickedTiles == self.gridSize*self.gridSize-self.numberOfMines:
            clickedPoint,leftOrRight=self.window.getMouse()
            i,j=self.findClickedIndex(clickedPoint)
            if leftOrRight=='L':
                if self.tiles[i][j].mine==True and self.tiles[i][j].flagged==False:
                    print("Mine, oops :P")
                    break            
                elif self.tiles[i][j].clicked==False and self.tiles[i][j].flagged==False:
                    self.findNeighbours(i,j,self.propagate)
            else:
                if self.tiles[i][j].clicked==False and self.flags<self.numberOfMines or self.tiles[i][j].flagged==True:
                    self.tiles[i][j].flagged = not self.tiles[i][j].flagged                                        
                    if self.tiles[i][j].flagged==False:
                        self.flags-=1
                    else:
                        self.flags+=1
                    self.tiles[i][j].drawTile(self.window)


def main():
    minesweeper=Minesweeper(8)
    minesweeper.play()
    minesweeper.window.close()

main()