#! /usr/bin/python3

from PIL import Image


class Tile(object):
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

    def load(self) -> None:
        raise NotImplementedError()

    def save(self) -> None:
        raise NotImplementedError()

    def breakdown_image(self, image_path: str, tile_size: int) -> None:  
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
        
        self.translation_map = list(map(lambda x: Tile(x), self.translation_map))

        return self

if __name__ == "__main__":
    it = ImageTranslator()
    images = [
        ["../resources/images/streets32x32.png", 8],
        ["../resources/images/river32x32.png", 1],
        ["../resources/images/river64x64.png", 1]
    ]
    
    it.breakdown_image(*images[0]).save()

    print(it)
    
