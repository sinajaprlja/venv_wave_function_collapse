#! /usr/bin/python3

import math
import random

import image_translator
import tile_model
import directions

class UnsolvableException(Exception):
    def __init__(self):
        super().__init__("At least one tile exists that has no matching pattern")


class WFCGenerator(object):
    def __init__(self, tile_model):
        self._tile_model = tile_model


    def _is_fully_collapsed(self):
        """
        Returns true when the algorithm finished and produced a valid output
        """
        for column in self._output:
            for tile in column:
                if len(tile) > 1:
                    return False
                if len(tile) == 0:
                    raise UnsolvableException()
        return True


    def _get_possible_patterns(self, pos):
        """
        Returns all valid patters at specific position
        """
        patterns = self._output[pos[0]][pos[1]]
        if patterns == []:
            raise ValueError(f"no possible patterns at {pos}")
        return patterns

    def _get_shannon_entropy(self, pos):
        """
        Calculate the shannon entropy at a specific position
        Tiles with only one pattern available have 0 entropy

        """
        entropy = 0
        if len(self._output[pos[0]][pos[1]]) == 1:
            return entropy

        for pattern in self._output[pos[0]][pos[1]]:
            entropy += self._tile_model.probabilities[pattern] * math.log(self._tile_model.probabilities[pattern], 2)
        entropy *= -1

        # Add some random noise for more natural distribution of collapse
        entropy -= random.uniform(0, 0.1)
        return entropy
    

    def _get_minimum_entropy_position(self):
        """
        Returns the position with the smallest entropy
        """
        raise NotImplementedError()  

    def _get_maximum_probability(self, pos):
        """
        Returns the highest probabilty a pattern can have at given position
        """
        raise NotImplementedError()  

    def _collapse(self, pos):
        """
        Collapse the tile at a specific position by taking the most probable patterns
        and randomly choose one.
        """
        raise NotImplementedError()  

    def _propagate(self, pos, size):
        """

        """
        raise NotImplementedError()  

    
        
    def generate_map(self, size):
        """
        Generate a new tile map of given size, the tilemap can be post processed to fill in corresponding patterns
        """
        raise NotImplementedError()  

    def _init_output(self, size):
        """
        Initilaize output map where every tile contains every possible pattern
        """
        self._output = []
        for y in range(size[1]):
            self._output.append([])
            for x in range(size[0]):
                self._output[-1].append(list(range(len(self._tile_model.patterns))))
    
    def __str__(self):
        result = ""
        for line in self._output:
            result = f"{result}{list(map(lambda x: 'n' if len(x) > 1 else x, line))}\n"
        return result

if __name__ == "__main__":
    it = image_translator.ImageTranslator()
    it.translate_image("../resources/images/example4x4.png", 1)
    
    tm = tile_model.TileModel(it)
    tm.build_patterns((2, 2))
    tm.build_rules()

    wfc = WFCGenerator(tm)
    wfc.generate_map((8, 8))
    for line in wfc._output:
        print(line)
