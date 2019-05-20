from PIL import Image as pil

class Image:
    def resize(self, image, tileWidth):
        return image.resize((int(0.8*tileWidth),int(0.8*tileWidth)))

    def __init__(self, tileWidth):                
        try:
            self.flagImage = pil.open("images/flag.png")            
            self.flagImage=self.resize(self.flagImage, tileWidth)            
        except:
            print("Flag image file not found.")
            self.flagImage=None
                        
if __name__ == "__main__":
    image=Image(200)
    image.flagImage.show()