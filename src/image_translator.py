#! /usr/bin/python3

from PIL import Image
import numpy as np
import pickle
import dataclasses

import utils



class DimensionException(Exception):
    """
    DimensionException is a custom exception class for when an array has unexcpected dimensions
    """
    def __init__(self, msg="Array has unexpected dimensions"):
        super().__init__(msg)    


@dataclasses.dataclass(slots=True)
class _Tile(object):
    """
    Class representing a little image called a tile.
    Image data is saved as Pixelgrid in Tile.pixels.
    Every Tile thats created receives an individual index.
    Tiles are are always quadratic, which means "height == width"
    ! Tiles with equal pixeldata can have different indicies when created seperatly !
    """
    
    pixels: list

    def __post_init__(self):
        if len(self.pixels) != len(self.pixels[0]):
            raise DimesionException("Tile has wrong dimension, width and height are expected to be equal - got ({len(self.pixels)}|{self.pixels[0]})")

    @property
    def size(self) -> int:
        return len(self.pixels)
    
    def __str__(self):
        s = str(index)
        for line in pixels:
            s = f"{s}\n{line}"
        return s

@dataclasses.dataclass(slots=True)
class TranslatedImage(object):
    """
    Class containing all data of a translated image, also provides methods for saving
    and loading such data.
    Tiles are stored in tile_map.
    the translated image is saved as bitmap consisting of the corresponding
    tile indicies.
    """
    tile_map: list
    bitmap: list
    
    def __str__(self) -> str:
        result = "Translated Image"
        for line in self.bitmap:
            result = f"{result}\n"
            for value in line:
                result = f"{result} {value:{len(str(len(self.tile_map) - 1))}}"
        return result
    
    def load(self, filename: str) -> None:
        """
        Loads all data from given binary file, look for *.imd files
        Overwrites currently saved data
        """
        utils.verbose(f"Loading translation data from '{filename}'", 1)
        with open(filename, "rb") as file:
            data = pickle.load(file)
            self.tile_map = data["tile_map"]
            self.bitmap = data["bitmap"]

    def save(self, filename: str) -> None:
        """
        Saves all data to given filename as binary, adds extension .imd
        """
        utils.verbose(f"Saving translation data to '{filename}.imd'", 1)
        with open(f"{filename}.imd", "wb") as file:
            pickle.dump(dataclasses.asdict(self), file, pickle.HIGHEST_PROTOCOL)


class ImageTranslator(object):
    """
    Class that simplifies images by breaking the image into chunks of given size. 
    Every chunk is called a tile, tiles with the same pixeldata get the same index.
    The simplified bitmap only contains the indicies of the tiles.
    Data of translated images is stored via the TranslatedImage dataclass
    """
    
    @staticmethod
    def breakdown_image(image_path: str, tile_size: int) -> None:  
        utils.verbose(f"breaking down {image_path} into tiles of size {tile_size}", 1)
        image = Image.open(image_path)
        
        # Ensure the tile size fits the image dimensions
        if image.width / tile_size != image.width // tile_size and image.height / tile_size != image.height // tile_size:
            raise DimensionException(f"image dimensions are not a multiple of the tile dimensions - img=({image.width},{image.height}), tile=({tile_size},{tile_size})")
        
        translated_image = []
        translation_map = []

        # Loop over tile grid and extract pixel values, store every unique tile to a list
        for x in range(image.width // tile_size):
            translated_image.append([])
            for y in range(image.height // tile_size):
                tile = []
                for i in range(tile_size):
                    tile.append([])
                    for j in range(tile_size):
                        tile[-1].append(image.getpixel((y * tile_size + j, x * tile_size + i)))          
                
                if not tile in translation_map:
                    translation_map.append(tile)

                translated_image[-1].append(translation_map.index(tile))
        
        # Convert pixel lists to Tile type
        translation_map = list(map(lambda x: _Tile(x), translation_map))

        utils.verbose(f"Brokedown image into {len(translation_map)} different tiles", 1)
        return TranslatedImage(translation_map, translated_image)

    @staticmethod 
    def rebuild_image(image: TranslatedImage, filename: str) -> list:
        utils.verbose(f"Rebuilding image from image.bitmap and saving it to {filename}", 1)

        # Build blank result array
        result = []
        for _ in range(len(image.bitmap) * image.tile_map[0].size):
            result.append([])
            for _ in range(len(image.bitmap[0]) * image.tile_map[0].size):
                result[-1].append([])
        
        # Fill result array corresponding to pixel data in the corresponding tiles
        for image.bitmap_row_index, image.bitmap_row in enumerate(image.bitmap):
            for image.bitmap_col_index, tile in enumerate(image.bitmap_row):
                for tile_row_index, tile_row in enumerate(image.tile_map[tile].pixels):
                    for tile_col_index, pixel in enumerate(tile_row):
                        result[image.bitmap_row_index * image.tile_map[0].size+ tile_row_index][image.bitmap_col_index *  image.tile_map[0].size + tile_col_index] = pixel
        
        # Convert array to image
        img = Image.fromarray(np.asarray(result, dtype=np.uint8))
        img.save(filename)
        utils.verbose(f"Successfully saved rebuild image to {filename}", 1)
        return result
    

if __name__ == "__main__":

    # Samples files with corresponding tile size
    images = [
        ["../resources/images/example4x4.png", 1],
        ["../resources/images/streets32x32.png", 8],
        ["../resources/images/river32x32.png", 1],
        ["../resources/images/river64x64.png", 1]
    ]
    
    ti = ImageTranslator.breakdown_image(*images[1])
    ti.save("image")
    print(ti)
    
    ti.load("image.imd")
    print(ti)
