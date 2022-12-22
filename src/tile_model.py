#! /usr/bin/python3


import image_translator
import directions

def rotate_list_clockwise(l):
    return [list(reversed(col)) for col in zip(*l)]

class TileModel(object):
    def __init__(self, translated_image: image_translator.ImageTranslator):
        self._translated_image = translated_image
        self._probabilities = []
        self._patterns = []
        self._rules = []

    def _is_overlap_equal(self, direction, pattern, questioned_pattern) -> bool:
        for y in range(0, len(pattern)):
            if y >= 0 and y < len(pattern) + direction.value[1]:
                for x in range(0, len(pattern[0])):
                    if x >= 0 and x < len(pattern[0]) + direction.value[0]:
                        if pattern[y][x] != questioned_pattern[y - direction.value[1]][x - direction.value[0]]:
                            return False
        return True
    
    def _get_pattern(self, pos, size):
        x, y = pos
        pattern = []
        for j in range(size[1]):
            pattern.append([])
            for i in range(size[0]):
                pattern[-1].append(self._translated_image.translated_image[y + j][x + i])
        return pattern
    
    def build_patterns(self, pattern_size):
        if pattern_size[0] <= 1 or pattern_size[1] <= 1:
            raise ValueError(f"pattern_size must be at least 2x2, got {pattern_size[0]}x{pattern_size[1]}")
        image_map = self._translated_image.translated_image
        amount_list = []
        for y in range(len(image_map) - (pattern_size[1] - 1)):
            for x in range(len(image_map[y]) - (pattern_size[0] - 1)):
                pattern = self._get_pattern((x, y), pattern_size)

                for _ in range(4):
                    pattern = rotate_list_clockwise(pattern)
                    if not pattern in self._patterns:
                        amount_list.append(1)
                        self._patterns.append(pattern)
                    else:
                        amount_list[self._patterns.index(pattern)] += 1
        
        for amount in amount_list:
            self._probabilities.append(amount / sum(amount_list))

    def build_rules(self):
        self._rules = [{}] * len(self._patterns)
        for pattern in self._rules:
            for direction in directions.Directions:
                pattern[direction] = []
        for pattern in self._patterns:
            for direction in directions.Directions:
                for questioned_pattern in self._patterns:
                    if self._is_overlap_equal(direction, pattern, questioned_pattern):
                        if not questioned_pattern in self._rules[self._patterns.index(pattern)][direction]:
                            self._rules[self._patterns.index(pattern)][direction].append(questioned_pattern)
        
        
if __name__ == "__main__":
    it = image_translator.ImageTranslator()
    it.translate_image("../resources/images/streets32x32.png", 8)
    it.translate_image("../resources/images/river32x32.png", 1)
    it.translate_image("../resources/images/example4x4.png", 1)

    print(it)

    tm = TileModel(it)
    tm.build_patterns((2, 2))
    tm.build_rules()
