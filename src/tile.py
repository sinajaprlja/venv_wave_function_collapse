#! /usr/bin/python3



class Tile(object):
    
    # Static object counter to give every a tile a unique identifier
    index = 0
    
    def __init__(self, pixels: list):
        self.pixels = pixels
        self.index = Tile.index
        Tile.index += 1


    @property
    def width(self) -> int:
        return len(self.pixels[0])

    @property
    def height(self) -> int:
        return len(self.pixels)
   

