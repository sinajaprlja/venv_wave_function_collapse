#! /usr/bin/python3


import image_translator
import directions
import utils
import pickle
import dataclasses

from config import *

@dataclasses.dataclass(slots=True)
class Pattern(object):
    """
    Class for storing corresponding pattern data and providing basic functionality 
    for comparing in different ways(overlapping/equality/...) as well as simple
    transformation(rotating,...)
    """
    pixels: list
    index: list = None
    probability: float = .0
    weight: int = 1
    
    @property
    def width(self):
        return len(self.pixels[0])

    @property
    def height(self):
        return len(self.pixels)
    
    def set_probability(self, probability: float) -> None:
        if not (0 <= probability < 1):
            raise ValueError(f"Probability value is out of range: got {probability}")
        self.probability = probability

    def __str__(self) -> str:
        return str(self.index[0])
    
    def __eq__(self, other) -> bool:
        "Pattern objects are equal when the pixeldata is equal"
        return self.pixels == other.pixels
    
    def __hash__(self) -> int:
        "Hash method for enabling Pattern objects as dict-keys"
        return hash(self.index[0])

    def overlaps(self, other, direction: directions.Directions) -> bool:
        """
        Checks if two patterns overlapping parts are equal.
        The overlapping part is determined by the given direction(UP, UP_RIGHT, RIGHT, ...)
        Returns true when all pixel values in the overlapping range are equal.
        """
        # Get row/column range depending on direction for own pixel matrix
        range_row_self = range(1 if direction.value[0] == 1 else 0, self.width - 1 if direction.value[0] == -1 else self.width)
        range_col_self = range(1 if direction.value[1] == 1 else 0, self.width - 1 if direction.value[1] == -1 else self.width)
        
        # Get row/column range depending on direction for other pixel matrix
        range_row_other = range(1 if direction.value[0] == -1 else 0, self.width - 1 if direction.value[0] == 1 else self.width)
        range_col_other = range(1 if direction.value[1] == -1 else 0, self.width - 1 if direction.value[1] == 1 else self.width)
        
        # Actual comparison, using the above ranges
        for row_index in zip(range_row_self, range_row_other):
            for col_index in zip(range_col_self, range_col_other):
                if self.pixels[row_index[0]][col_index[0]] != other.pixels[row_index[1]][col_index[1]]:
                    return False
        return True
   
    def rotate(self):
        "Rotate the pixels 90° clockwise and returning a new Pattern instance"
        return Pattern(list(col[::-1] for col in zip(*self.pixels)))



class TileModel(object):
    def __init__(self, translated_image: image_translator.TranslatedImage):
        self._translated_image = translated_image
        self.patterns = []
        self.rules = {}

    def load(self):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

    def _get_pattern(self, pos: tuple, size: int) -> Pattern:
        """
        Returns a PatternObject containing a 2-dimensional list. Starting at <pos>
        from the top left corner, with width/height equal to <size>
        """
        x, y = pos
        pattern = []
        for j in range(size[1]):
            pattern.append([])
            for i in range(size[0]):
                pattern[-1].append(self._translated_image.bitmap[y + j][x + i])
        return Pattern(pattern)
    
    def _add_pattern(self, pattern: Pattern) -> None:
        """
        Adds the pattern to the pattern_list when its not already in there,
        else the patterns weight is just increased by 1
        """
        if not pattern in self.patterns:
            self.patterns.append(pattern)
        else:
            for existing_pattern in self.patterns:
                if pattern == existing_pattern:
                    existing_pattern.weight += 1
                    return

    def build_patterns(self, pattern_size: int) -> None:
        """
        Get all possible patterns in the translated_image of size <pattern_size> and rotate
        them 90/180 and 270 degrees when option ROTATE is enabled
        Save the corresponding occurance probabilties to as soon as all distinct patterns have been found
        """
        utils.verbose(f"Breakdown bitmap into {pattern_size}-sized patterns", 1)
        if pattern_size[0] <= 1 or pattern_size[1] <= 1:
            raise ValueError(f"pattern_size must be at least 2x2, got {pattern_size[0]}x{pattern_size[1]}")
        image_map = self._translated_image.bitmap
        for y in range(len(image_map) - (pattern_size[1] - 1)):
            for x in range(len(image_map[y]) - (pattern_size[0] - 1)):
                pattern = self._get_pattern((x, y), pattern_size)
                
                if ROTATE:
                    for _ in range(4):
                        pattern = pattern.rotate()
                        self._add_pattern(pattern)            
                else:
                    self._add_pattern(pattern)            

        weights = sum([pattern.weight for pattern in self.patterns])
        for index, pattern in enumerate(self.patterns):
            pattern.set_probability(pattern.weight / weights)
            pattern.index = [index]
        utils.verbose(f"Brokedown bitmap into {len(self.patterns)} patterns of size {pattern_size}", 1)

    def build_rules(self) -> None:
        """
        builds the rules for generating new images by overlapping patterns 
        for every direction(UP, UP_RIGHT, RIGHT, ...) 
        Add rule when overlapping pattern and overlapping questioned pattern are equal
        rules: dict 
            pattern -> dict
                direction -> corresponding pattern indicies
        """
        self.rules = {} 
        for pattern in self.patterns:
            self.rules[pattern] = {}
            for direction in directions.Directions:
                self.rules[pattern][direction] = []
                for questioned_pattern in self.patterns:
                    if pattern.overlaps(questioned_pattern, direction):
                        self.rules[pattern][direction].append(questioned_pattern)
        utils.verbose(f"Build {len(self)} rules", 1) 
    
    def reverse_patterns(self, bitmap: list) -> list:
        result = []
        for _ in range(len(bitmap) * bitmap[0][0][0].height): 
            result.append([])
            for _ in range(len(bitmap[0]) * bitmap[0][0][0].width):
                result[-1].append([])
        
        for bitmap_row_index, bitmap_row in enumerate(bitmap):
            for bitmap_col_index, pattern in enumerate(bitmap_row):
                for pattern_row_index, pattern_row in enumerate(pattern[0].pixels):
                    for pattern_col_index, pixel in enumerate(pattern_row):
                        result[bitmap_row_index * bitmap[0][0][0].height + pattern_row_index][bitmap_col_index * bitmap[0][0][0].width + pattern_col_index] = pixel
        return result    


    def __str__(self):
        result = "Patterns\n"
        for pattern in self.patterns:
            result = f"{result}  {pattern.index}\n    {pattern.pixels}\n"
        result = f"{result}\nRules\n"
        for pattern in self.rules:
            result = f"{result}  {pattern.index}\n"
            for direction in self.rules[pattern]:
                result = f"{result}    {direction}\n"
                result = f"{result}    - {[x.index for x in self.rules[pattern][direction]]}\n"
        return result
    
    def __len__(self):
        return sum([len(self.rules[pattern][direction]) for pattern in self.rules for direction in self.rules[pattern]])


class ModelBuilder(object):
    pass

if __name__ == "__main__":
    it = image_translator.ImageTranslator()
    ti = it.breakdown_image("../resources/images/streets32x32.png", 8)
    ti = it.breakdown_image("../resources/images/river32x32.png", 1)
    ti = it.breakdown_image("../resources/images/example4x4.png", 1)

    tm = TileModel(ti)
    tm.build_patterns((2, 2))
    tm.build_rules()
    
    print(tm)
    print(len(tm))
