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
        """
        Returns true when the algorithm finished and produced a valid output
        """
        for column in self._output:
            for tile in column:
                if len(tile) > 1:
                    return False
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
        minimum_entropy = None
        minimum_entropy_position = None
        for x in range(len(self._output)):
            for y in range(len(self._output[0])):
                position = (x, y)
                entropy = self._get_shannon_entropy(position)
                if entropy == 0:
                    continue

                if minimum_entropy == None or entropy < minimum_entropy:
                    mimimum_entropy = entropy
                    minimum_entropy_position = position
        return minimum_entropy_position
    

    def _get_maximum_probability(self, pos):
        maximum_probability = 0
        for pattern in self._get_possible_patterns(pos):
            if self._tile_model.probabilities[pattern] > maximum_probability:
                maximum_probability = self._tile_model.probabilities[pattern]
        return maximum_probability


    def _collapse(self, pos):
        """
        Collapse the tile at a specific position by taking the most probable patterns
        and randomly choose one.
        """
        if pos == None:
            return
        maximum_probability_patterns = []
        maximum_probability = self._get_maximum_probability(pos)
        for pattern in self._get_possible_patterns(pos):
            if self._tile_model.probabilities[pattern] == maximum_probability:
                maximum_probability_patterns.append(pattern)
        
        r = random.randint(0, len(maximum_probability_patterns))
        print(maximum_probability_patterns, r)
        self._output[pos[0]][pos[1]] = [maximum_probability_patterns[r]]
        print(self)

    def _propagate(self, pos, size):
        stack = [pos]
        while len(stack) > 0:
            print(stack)
            pos = stack.pop()
            patterns = self._get_possible_patterns(pos)
            
            for direction in directions.Directions:
                if direction.is_valid(pos, size):
                    adjacent_pos = (pos[0] + direction.value[0], pos[1] + direction.value[1])
                    possible_patterns_at_adjacent = self._get_possible_patterns(adjacent_pos)

                    for pattern in possible_patterns_at_adjacent:
                        if len(patterns) > 1:
                            is_possible = any([pattern in self._tile_model.rules[p][direction] for p in patterns])
                        else:
                            is_possible = pattern in self._tile_model.rules[patterns[0]][direction]
                    
                    # Remove tile when not in any of the adjacent rules
                    if not is_possible:
                        self._output[pos[0]][pos[1]] = [p for p in self._output[pos[0]][pos[1]] if p != pattern]
                        
                        if adjacent_pos not in stack:
                            stack.append(adjacent_pos)

    def _init_output(self, size):
        """
        Initilaize output map where every tile contains every possible pattern
        """
        self._output = []
        for y in range(size[1]):
            self._output.append([])
            for x in range(size[0]):
                self._output[-1].append(list(range(len(self._tile_model.patterns))))
    
        
    def generate_map(self, size):
        """
        Generate a new tile map of given size, the tilemap can be post processed to fill in corresponding patterns
        """
        self._init_output(size)
        while not self._is_fully_collapsed():
            try:
                minimum_entropy_pos = self._get_minimum_entropy_position()
                self._collapse(minimum_entropy_pos)
                self._propagate(minimum_entropy_pos, size)
            except IndexError as e:
                print("unsolvable, try new one")
                self._init_output(size)

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
