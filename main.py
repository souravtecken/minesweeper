from graphics import *
from random import choice
import image 

unclickedColor=color_rgb(160,160,160)
clickedColor=color_rgb(220,220,220)
borderColor=color_rgb(100,100,100)
hoverColor=color_rgb(190,190,190)
windowHeight=900
textColors={0:"none",1:"blue",2:"green",3:"red",4:"purple",5:"maroon",6:"turquoise",7:"black",8:"gray",'F':"black","M":"red"}

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

    def drawTile(self, window, image=None, gameOver=False,hover=False): # Draws tile at its coordinates with given width
        # Rectangle
        r=Rectangle(self.topLeft,self.bottomRight)         
        r.setFill(unclickedColor)    
        r.setOutline(borderColor)    
        r.setWidth(3)        
        if self.clicked:
            r.setFill(clickedColor)                    
        elif hover==True:
            r.setFill(hoverColor)
        r.draw(window)            
        # Text
        textString=self.val        
        if self.flagged:            
            textString='F'  
        elif self.mine:
            textString='M'
        t=Text(Point(self.x,self.y),textString)
        try:
            t.setSize(int(self.width*0.4)) # Largest size allowed is 36
        except:
            t.setSize(36)
        t.setFill(textColors[textString])
        # Image
        if gameOver==False:
            if self.flagged and image.flagImage:
                i=Image(Point(self.x,self.y),image.flagImage)
                i.draw(window)
            elif self.clicked and self.val or self.flagged:        
                t.draw(window)        
        else:            
            if self.mine and image.mineImage and not self.flagged:
                i=Image(Point(self.x,self.y),image.mineImage)                
            elif self.flagged and not self.mine:
                i=Image(Point(self.x,self.y),image.flagWrongImage)
            else:
                i=Image(Point(self.x,self.y),image.flagImage)
            i.draw(window)
                            
class Minesweeper:
    def __init__(self, gridSize): # Initialises game properties, gridsize, numberOfMines, so on        
        self.flags=0
        self.clickedTiles=0
        self.gridSize=gridSize
        self.tileWidth=windowHeight//gridSize
        self.numberOfMines=40
        self.previousTile=None
        self.icons=image.Image(self.tileWidth)
        self.tiles=[[Tile(self.tileWidth*j + self.tileWidth//2, self.tileWidth*i + self.tileWidth//2, 0, self.tileWidth)
                                                     for j in range(gridSize)] for i in range(gridSize)]   
        self.window=GraphWin("Minesweeper",windowHeight+300,windowHeight,autoflush=False)        

    def displayNumberOfFlags(self):
        t=Text(Point(self.gridSize*self.tileWidth+150,250),f"{self.flags} / {self.numberOfMines}")
        t.setSize(20)
        r=Rectangle(Point(self.gridSize*self.tileWidth+10,240),Point(self.gridSize*self.tileWidth+300,260))
        r.setFill(color_rgb(217,217,217))
        r.setOutline(color_rgb(217,217,217))
        r.draw(self.window)
        t.draw(self.window)

    def drawGrid(self): # Draws all the tiles 
        for tileRow in self.tiles:
            for tile in tileRow:
                tile.drawTile(self.window)
        i=Image(Point(self.gridSize*self.tileWidth+150,150),self.icons.flagImageUnResized)
        i.draw(self.window)
        self.displayNumberOfFlags()

    def increment(self, neighbours): #Increments all tiles given by these indices by 1 
        for pair in neighbours:
            self.tiles[pair[0]][pair[1]].val+=1

    def findNeighbours(self, i, j, callback):
        """ Finds all neighbours of given tile
            call back can be either incremet/propagate
            Increment - To increment values of tiles neighbouring the mines
            Propagate - To highlight all neighbouring mines recursively """
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
        """ Assigns mines to random tiles.
            Increments value of neighbouring tiles """
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

    def findClickedIndex(self, clickedPoint): # Given coordinates, returns index of tile
        i=int(clickedPoint.y//self.tileWidth)
        j=int(clickedPoint.x//self.tileWidth)
        if i<self.gridSize and j<self.gridSize:
            return i,j
        return False,False   
    
    def hover(self,mousePosition): # Given coordinates, triggers hover effect for tile in position
        i,j=self.findClickedIndex(mousePosition)
        if i<self.gridSize and j<self.gridSize:
            if (int(i),int(j))!=self.previousTile:
                if self.previousTile:
                    self.tiles[self.previousTile[0]][self.previousTile[1]].drawTile(self.window,image=self.icons)
                self.previousTile=i,j
                self.tiles[i][j].drawTile(self.window,image=self.icons,hover=True)

    def displayMines(self): # Once game's over, displays positions of all mines
        for tileRow in self.tiles:
            for tile in tileRow:
                if tile.mine==True or tile.flagged==True:
                    tile.drawTile(self.window,self.icons,gameOver=True)
        self.window.getMouseClick()                             

    def play(self):
        self.initTileValues()
        self.drawGrid()
        # Game continues until all tiles except mines have beel selected
        while not self.clickedTiles == self.gridSize*self.gridSize-self.numberOfMines: 
            mousePosition=self.window.getMouse()
            self.hover(mousePosition)         
            clickedPoint,leftOrRight=self.window.checkMouseClick()
            if clickedPoint!=None:
                i,j=self.findClickedIndex(clickedPoint)
                if leftOrRight=='L': # If Left mouse click
                    if self.tiles[i][j].mine==True and self.tiles[i][j].flagged==False:                        
                        break        
                    elif self.tiles[i][j].clicked==False and self.tiles[i][j].flagged==False:
                        self.findNeighbours(i,j,self.propagate)
                else: # If right mouse click
                    if self.tiles[i][j].clicked==False and self.flags<self.numberOfMines or self.tiles[i][j].flagged==True:
                        self.tiles[i][j].flagged = not self.tiles[i][j].flagged                                        
                        if self.tiles[i][j].flagged==False:
                            self.flags-=1
                        else:
                            self.flags+=1
                        self.tiles[i][j].drawTile(self.window,self.icons)
                    self.displayNumberOfFlags()
        self.displayMines() #Game's over, display mine locations


def main():
    minesweeper=Minesweeper(16)
    minesweeper.play()
    minesweeper.window.close()

main()