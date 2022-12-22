#! /usr/bin/python3

from PIL import Image
from tile import Tile

class ImageTranslator(object):
    def __init__(self) -> None:
        self.translation_map = []
        self.translated_image = []
    
    def __str__(self):
        result = "Translated Image"
        for line in self.translated_image:
            result = f"{result}\n"
            for value in line:
                result = f"{result} {value:{len(str(len(self.translation_map)))}d}"
        return result
    
    @property
    def number_of_patterns(self):
        return len(self.translation_map)

    def load(self) -> None:
        return self

    def save(self) -> None:
        return self
        
    def translate_image(self, image_path: str, tile_size: int) -> None:  
        image = Image.open(image_path)
        self.__init__()
        if image.width / tile_size != image.width // tile_size and image.height / tile_size != image.height // tile_size:
            raise ValueError(f"image dimensions are not a multiple of the tile dimensions - img=({image.width},{image.height}), tile=({tile_size},{tile_size})")
        
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
        
        tmp = []
        for tile in self.translation_map:
            tmp.append(Tile(tile))
        self.translation_map = tmp

        return self

if __name__ == "__main__":
    it = ImageTranslator()
    images = [
        ["../resources/images/streets32x32.png", 8],
        ["../resources/images/river32x32.png", 1],
        ["../resources/images/river64x64.png", 1]
    ]
    
    it.translate_image(*images[0]).save()

    print(it)
    