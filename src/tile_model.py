#! /usr/bin/python3


import image_translator
import directions


class Pattern(object):
    index = 0
    def __init__(self, pixels):
        self.pixels = pixels
        self.probability = None
        self.weight = 1
        self.index = Pattern.index
        Pattern.index += 1
        
    def set_probability(self, probability: float):
        self.probability = probability

    def __len__(self):
        return 1
    
    def __str__(self):
        return str(self.index)
    
    def __eq__(self, other):
        return self.pixels == other.pixels
    
    def overlap_is_equal(self, other, direction):
        pass
    
    def rotate(self):
        return Pattern(list(col[::-1] for col in zip(*self.pixels)))

class TileModel(object):
    def __init__(self, translated_image: image_translator.ImageTranslator):
        self._translated_image = translated_image
        self.patterns = []
        self.rules = []
    

    def _is_overlap_equal(self, direction, pattern, questioned_pattern) -> bool:
        """
        Checks if two patterns overlapping parts are equal.
        The overlapping part is determined by the given direction(UP, UP_RIGHT, RIGHT, ...)
        Returns true when all pixel values in the overlapping range are equal.
        """
        for y in range(0, len(pattern)):
            if y >= 0 and y < len(pattern) + direction.value[1]:
                for x in range(0, len(pattern[0])):
                    if x >= 0 and x < len(pattern[0]) + direction.value[0]:
                        if pattern[y][x] != questioned_pattern[y - direction.value[1]][x - direction.value[0]]:
                            return False
        return True


    def _get_pattern(self, pos, size):
        """
        Returns a PatternObject containing a 2-dimensional list. Starting at <pos>
        from the top left corner, with width/height equal to <size>
        """
        x, y = pos
        pattern = []
        for j in range(size[1]):
            pattern.append([])
            for i in range(size[0]):
                pattern[-1].append(self._translated_image.translated_image[y + j][x + i])
        return Pattern(pattern)
    

    def build_patterns(self, pattern_size):
        """
        Get all possible patterns in the translated_image of size <pattern_size> and rotate
        them 90/180 and 270 degrees
        Save the corresponding occurance probabilties to _probabilities
        Pattern and probabilty can be identified by their indicies
        """
        if pattern_size[0] <= 1 or pattern_size[1] <= 1:
            raise ValueError(f"pattern_size must be at least 2x2, got {pattern_size[0]}x{pattern_size[1]}")
        image_map = self._translated_image.translated_image
        for y in range(len(image_map) - (pattern_size[1] - 1)):
            for x in range(len(image_map[y]) - (pattern_size[0] - 1)):
                pattern = self._get_pattern((x, y), pattern_size)

                for _ in range(4):
                    pattern = pattern.rotate()
                    
                    if not pattern in self.patterns:
                        self.patterns.append(pattern)
                    else:
                        pattern.weight += 1
        
        weights = sum([pattern.weight for pattern in self.patterns])
        for pattern in self.patterns:
            pattern.set_probability(pattern.weight / weights)


    def build_rules(self):
        """
        builds the rules for generating new images by overlapping patterns 
        for every direction(UP, UP_RIGHT, RIGHT, ...) 
        Add rule when overlapping pattern and overlapping questioned pattern are equal
        rules: list 
            pattern: dict
                direction -> corresponding pattern indicies
        """
        self._rules = [] 
        for pattern in self.patterns:
            self.rules.append({})
            for direction in directions.Directions:
                self.rules[-1][direction] = []
                for questioned_pattern in self.patterns:
                    if self._is_overlap_equal(direction, pattern.pixels, questioned_pattern.pixels):
                        self.rules[-1][direction].append(self.patterns.index(questioned_pattern))
    
    def __str__(self):
        result = "Patterns\n"
        for index, pattern in enumerate(self.patterns):
            result = f"{result}  {index}\n    {pattern.pixels}\n"
        result = f"{result}\nRules\n"
        for index, pattern in enumerate(self.rules):
            result = f"{result}  {index}\n"
            for direction in pattern:
                result = f"{result}    {direction}\n"
                result = f"{result}    - {pattern[direction]}\n"
        return result
    
    def __len__(self):
        return sum([len(pattern[direction]) for pattern in self.rules for direction in pattern])

if __name__ == "__main__":
    it = image_translator.ImageTranslator()
    it.translate_image("../resources/images/streets32x32.png", 8)
    it.translate_image("../resources/images/river32x32.png", 1)
    it.translate_image("../resources/images/example4x4.png", 1)

    print(it)

    tm = TileModel(it)
    tm.build_patterns((2, 2))
    tm.build_rules()
    
    print(tm)
    print(len(tm))
