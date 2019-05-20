from PIL import Image as pil

class Image:
    def resize(self, image, tileWidth):
        return image.resize((int(0.8*tileWidth),int(0.8*tileWidth)))

    def __init__(self, tileWidth):                
        try:
            self.flagImage = pil.open("images/flag.png")            
            self.flagImage=self.resize(self.flagImage, tileWidth)            
        except:
            print("Flag icon file not found.")
            self.flagImage=None
        try:
            self.mineImage = pil.open("images/mine.png")
            self.mineImage=self.resize(self.mineImage, tileWidth)
        except:
            print("Mine icon file not found.")
            self.mineImage=None            
                        
if __name__ == "__main__":
    image=Image(200)
    image.flagImage.show()
    image.mineImage.show()