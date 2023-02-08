#! /usr/bin/python3

from PIL import Image
import numpy as np

import utils



class DimensionException(Exception):
    """
    DimensionException is a custom exception class for when an array has unexcpected dimensions
    """
    def __init__(self, msg="Array has unexpected dimensions"):
        super().__init__(msg)    



class Tile(object):
    """
    Class representing a little image called a tile.
    Image data is saved as Pixelgrid in Tile.pixels
    Every Tile thats created receives an individual index.
    Tiles are are always quadratic, which means "height == width"
    ! Tiles with equal pixeldata can have different indicies when created seperatly !
    """
    index = 0
    
    def __init__(self, pixels: list):
        if len(pixels) != len(pixels[0]):
            raise DimesionException("Tile has wrong dimension, width and height are expected to be equal - got ({len(self.pixels)}|{self.pixels[0]})")
        self.pixels = pixels
        self.index = Tile.index
        Tile.index += 1
        self._iter_index = -1

    @property
    def size(self) -> int:
        return len(self.pixels)
    
    def __iter__(self):
        return self

    def __next__(self):
        self._iter_index += 1
        if self._iter_index < len(self.pixels):
            return self.pixels[self._iter_index]
        raise StopIteration

    def __str__(self):
        s = str(index)
        for line in pixels:
            s = f"{s}\n{line}"
        return s



class ImageTranslator(object):
    def __init__(self) -> None:
        self.translated_image = []
        self.translation_map = []

    def __str__(self):
        result = "Translated Image"
        for line in self.translated_image:
            result = f"{result}\n"
            for value in line:
                result = f"{result} {value:{len(str(Tile.index))}d}"
        return result
    
    @property
    def number_of_patterns(self):
        return Tile.index 

    def load(self, filename) -> None:
        raise NotImplementedError()

    def save(self, filename) -> None:
        try:
            with open(f"{filename}.imd", "w") as file:
                for index, tile in enumerate(self.translation_map):
                    file.write(f"\ntile - {index}\n")
                    for line in tile:
                        file.write(f"{str(line)}\n")
                file.write("\nimage\n")
                for line in self.translated_image:
                    file.write(f"{str(line)}\n")
        except IOError as e:
            self.save("tmp.imd")
        except:
            raise
        


    def breakdown_image(self, image_path: str, tile_size: int) -> None:  
        utils.verbose(f"breaking down {image_path} into tiles of size {tile_size}", 1)
        image = Image.open(image_path)
        self.__init__()
        if image.width / tile_size != image.width // tile_size and image.height / tile_size != image.height // tile_size:
            raise DimensionException(f"image dimensions are not a multiple of the tile dimensions - img=({image.width},{image.height}), tile=({tile_size},{tile_size})")
        
        for x in range(image.width // tile_size):
            self.translated_image.append([])
            for y in range(image.height // tile_size):
                tile = []
                for i in range(tile_size):
                    tile.append([])
                    for j in range(tile_size):
                        tile[-1].append(image.getpixel((y * tile_size + j, x * tile_size + i)))          
                
                if not tile in self.translation_map:
                    self.translation_map.append(tile)

                self.translated_image[-1].append(self.translation_map.index(tile))
        
        self.translation_map = list(map(lambda x: Tile(x), self.translation_map))
        utils.verbose(f"Brokedown image into {len(self.translation_map)} different tiles", 1)
        utils.verbose(self, 3)
        return self

    
    def rebuild_image(self, bitmap: list, filename: str) -> list:
        utils.verbose(f"Rebuilding image from bitmap and saving it to {filename}", 1)
        result = []
        for _ in range(len(bitmap) * self.translation_map[0].size):
            result.append([])
            for _ in range(len(bitmap[0]) * self.translation_map[0].size):
                result[-1].append([])

        for bitmap_row_index, bitmap_row in enumerate(bitmap):
            for bitmap_col_index, tile in enumerate(bitmap_row):
                for tile_row_index, tile_row in enumerate(self.translation_map[tile].pixels):
                    for tile_col_index, pixel in enumerate(tile_row):
                        result[bitmap_row_index * self.translation_map[0].size+ tile_row_index][bitmap_col_index *  self.translation_map[0].size + tile_col_index] = pixel
        
        img = Image.fromarray(np.asarray(result, dtype=np.uint8))
        img.save(filename)
        utils.verbose(f"Successfully save rebuild image to {filename}", 1)
        return result
    

if __name__ == "__main__":
    it = ImageTranslator()
    images = [
        ["../resources/images/example4x4.png", 1],
        ["../resources/images/streets32x32.png", 8],
        ["../resources/images/river32x32.png", 1],
        ["../resources/images/river64x64.png", 1]
    ]
    
    it.breakdown_image(*images[1]).save("image")

    print(it)
    
