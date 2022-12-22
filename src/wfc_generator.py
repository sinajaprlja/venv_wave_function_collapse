#! /usr/bin/python3

import math
import random

import image_translator
import tile_model
import directions

class WFCGenerator(object):
    def __init__(self, tile_model):
        self._tile_model = tile_model
    
    def _is_fully_collapsed(self):
        for column in self._output:
            for tile in column:
                if len(tile) > 1:
                    return False
        return True
        
    def _get_possible_patterns(self, pos):
        return self._output[pos[0]][pos[1]]

    def _get_shannon_entropy(self, pos):
        entropy = 0
        if len(self._output[pos[0]][pos[1]]) == 1:
            return entropy

        for pattern in self._output[pos[0]][pos[1]]:
            entropy += self._tile_model._probabilities[self._tile_model._patterns.index(pattern)] * math.log(self._tile_model._probabilities[self._tile_model._patterns.index(pattern)], 2)
        entropy += -1
        entropy -= random.uniform(0, 0.1)
        return entropy
    
    def _get_minimum_entropy_position(self):
        minimum_entropy = 1
        minimum_entropy_position = None
        for position in zip(range(len(self._output[0])), range(len(self._output))):
            entropy = self._get_shannon_entropy(position)
            if entropy == 0:
                continue

            if entropy < minimum_entropy:
                mimimum_entropy = entropy
                minimum_entropy_position = position
        return minimum_entropy_position
    
    def _get_maximum_probability(self, pos):
        maximum_probability = 0
        for pattern in self._get_possible_patterns(pos):
            if self._tile_model._probabilities[self._tile_model._patterns.index(pattern)] > maximum_probability:
                maximum_probability = self._tile_model._probabilities[self._tile_model._patterns.index(pattern)]
        return maximum_probability

    def _collapse(self, pos):
        maximum_probability_patterns = []
        maximum_probability = self._get_maximum_probability(pos)
        for pattern in self._get_possible_patterns(pos):
            if self._tile_model._probabilities[self._tile_model._patterns.index(pattern)] == maximum_probability:
                maximum_probability_patterns.append(pattern)

        self._output[pos[0]][pos[1]] = [maximum_probability_patterns[random.randint(0, len(maximum_probability_patterns))]]

    def _propagate(self, pos):
        changed = [pos] 
        while len(changed) > 0:
            tmp = changed
            for tile in tmp:
                for direction in directions.Directions:
                    if direction.is_valid(tile, (len(self._output[0]), len(self._output)), (len(self._tile_model._patterns[0][0]), len(self._tile_model._patterns[0]))):
                        checked_tile = (tile[0] + direction.value[0], tile[1] + direction.value[1])
                        before = self._output[checked_tile[0]][checked_tile[1]]
                        new = []
                        for pattern in self._output[tile[0]][tile[1]]:
                            new.extend(self._tile_model._rules[self._tile_model._patterns.index(pattern)][direction])
                        final = [pattern for pattern in new if pattern in before]
                        print(final)
                        exit()
                        if final != before:
                            self._output[checked_tile[0]][checked_tile[1]] = final
                            changed.append(checked_tile)
                del changed[0]
            
    
    def _init_output(self, size):
        self._output = []
        for y in range(size[1]):
            self._output.append([])
            for x in range(size[0]):
                self._output[-1].append(self._tile_model._patterns)

    def generate_map(self, size):
        self._init_output(size)
        minimum_entropy_position = (random.randint(0, size[0]), random.randint(0, size[1]))
        try:
            while not self._is_fully_collapsed():
                self._collapse(minimum_entropy_position)
                self._propagate(minimum_entropy_position)
                minimum_entropy_position = self._get_minimum_entropy_position()

        except:
            raise








if __name__ == "__main__":
    it = image_translator.ImageTranslator()
    it.translate_image("../resources/images/example4x4.png", 1)
    
    tm = tile_model.TileModel(it)
    tm.build_patterns((2, 2))
    tm.build_rules()

    wfc = WFCGenerator(tm)
    wfc.generate_map((32, 32))
