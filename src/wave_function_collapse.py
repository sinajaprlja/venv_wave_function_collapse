#! /usr/bin/python3

import sys
import math
import time
import random

import image_translator
import tile_model
import directions

def progressbar(progress, maximum, text_front='', text_back='', filler_main='#', filler_back='-', bar_lenght=50):
    '''
    *args
        progress:---current value of process
        maximum:----max value process can reach
    **kwargs
        text_front:-text in front of the progressbar (TEXT_FRONT[####     ])
        text_back:--text behind the progressbar ([###     ]TEXT_BACK)
        filler_main:-----char used in the progressbar ([####     ], [++++    ], [====    ], ...)
        filler_back:-----char used as background-filler ([###-----], [###     ], ([###.....]), ...)
        bar_lenght:-lenght of progressbar ([   <-"space between square brackets"->   ])
    '''
    percentage = round((progress / maximum) * bar_lenght)
    inside = f"{percentage*filler_main}{(bar_lenght - percentage) * filler_back}"
    output = "\r{}[{:{}s}]{}".format(text_front, inside, bar_lenght, text_back)
    if progress >= maximum:
        output = "\r{}[{:{}s}]{}\n".format(text_front, bar_lenght*filler_main, bar_lenght, text_back)
    sys.stdout.write(output)
    sys.stdout.flush()


class UnsolvableException(Exception):
    def __init__(self):
        super().__init__("At least one tile exists that has no matching pattern")

class NotInitializedException(Exception):
    def __init__(self, msg="unknown"):
        super().__init__(f"Has not been initialized - <{msg}>")



class WaveFunctionCollapse(object):
    def __init__(self, tile_model: tile_model.TileModel):
        self._tile_model = tile_model
        self._output = None

    @property
    def output(self) -> list:
        if self._output is None:
            raise NotInitializedException("output")
        return self._output

    @property
    def number_of_collapsed_tiles(self):
        s = 0
        for row in self.output:
            for cell in row:
                if len(cell) == 1:
                    s += 1
        return s


    def _is_fully_collapsed(self) -> bool:
        """
        Returns true when the algorithm finished and produced a valid output
        """
        for column in self.output:
            for tile in column:
                if len(tile) > 1:
                    return False
        return True


    def _get_possible_patterns(self, pos: tuple) -> list:
        """
        Returns all valid patters at specific position
        """
        patterns = self._output[pos[0]][pos[1]]
        if patterns == []:
            raise ValueError(f"no possible patterns at {pos}")
        return patterns

    def _get_shannon_entropy(self, pos: tuple) -> float:
        """
        Calculate the shannon entropy at a specific position
        Tiles with only one pattern available have 0 entropy

        """
        entropy = 0
        if len(self.output[pos[0]][pos[1]]) == 1 and self.output[pos[0]][pos[1]][0].collapsed:
            return 9999
        
        if self.output[pos[0]][pos[1]] == []:
            raise UnsolvableException()

        for pattern in self.output[pos[0]][pos[1]]:
            entropy += pattern.probability * math.log(pattern.probability, 2)
        entropy *= -1

        # Add some random noise for more natural distribution of collapse
        entropy -= random.uniform(0, 0.1)
        return entropy
    

    def _get_minimum_entropy_position(self) -> tuple:
        """
        Returns the position with the smallest entropy, classical approach of looping over every element 
        and overwriting the smallest element when smaller element has been found.
        ! There will be minor differences when entropy table is printed afterwards because        !
        ! of adding a little random offset to every value for a more natural generating algorithm !
        """
        minimum_entropy = self._get_shannon_entropy((0, 0))
        minimum_entropy_position = (0, 0)
        for row in range(len(self.output)):
            for col in range(len(self.output[0])):
                if (entropy := self._get_shannon_entropy((row, col))) < minimum_entropy:
                    minimum_entropy = entropy
                    minimum_entropy_position = (row, col)
        return minimum_entropy_position       

    def _get_maximum_probability(self, pos: tuple) -> int:
        """
        Returns the highest probabilty a pattern can have at given position, classical approach of looping 
        over every element and overwriting the the maximum element when bigger element has been found.
        Pattern probability is constant for same input
        """
        maximum_probability = 0
        for pattern in self.output[pos[0]][pos[1]]:
            if (probability := pattern.probability) > maximum_probability:
                maximum_probability = probability
        return maximum_probability

    def _collapse(self, pos):
        """
        Collapse the tile at a specific position by taking the most probable patterns
        and randomly choose one.
        """
        maximum_probability = self._get_maximum_probability(pos)
        maximum_probability_patterns = [p for p in self.output[pos[0]][pos[1]] if p.probability >= maximum_probability]
        #self.output[pos[0]][pos[1]] = [random.choice(maximum_probability_patterns)]
        self.output[pos[0]][pos[1]] = [random.choice(self.output[pos[0]][pos[1]])]
        self.output[pos[0]][pos[1]][0].collapsed = True

    def _propagate(self, start: tuple, size: tuple):
        """
        """
        stack = [start]
        while stack:
            pos = stack.pop()
            patterns = self.output[pos[0]][pos[1]]
            for direction in directions.Directions:
                if direction.is_valid(pos, size):
                    adjacent_pos = (pos[0] + direction.value[0], pos[1] + direction.value[1])
                    
                    tmp = []
                    for adjacent_pattern in self.output[adjacent_pos[0]][adjacent_pos[1]]:
                        possible = any([pattern in self._tile_model.rules[adjacent_pattern][direction.negate()] for pattern in patterns])
                        
                        if possible:
                            tmp.append(adjacent_pattern)
                        elif adjacent_pos not in stack:
                            stack.append(adjacent_pos)
                    self.output[adjacent_pos[0]][adjacent_pos[1]] = tmp 
                        
                
    def next(self, size):
        """
        Builds the next step of the output by collapsing and propagating threw every change
        """
        solution = []
        try:
            if not self._is_fully_collapsed():
                minimum_entropy_position = self._get_minimum_entropy_position()
                self._collapse(minimum_entropy_position)
                self._propagate(minimum_entropy_position, size)
        except UnsolvableException as e:
            self._init_output(size)

        except Exception as e:
            raise e

    def generate_map(self, size):
        """
        Generate a new bitmap accordingly to the ruleset of tile_model at given size.
        Do so by collapsing and propagating(next()-method) until the map is completly collapsed
        """
        self._init_output(size)
        start = time.time()
        while not self._is_fully_collapsed():
            self.next(size)
            progressbar(self.number_of_collapsed_tiles, size[0]*size[1], bar_lenght=100, text_back=f" {time.time()-start:.2f} sec")


    def _init_output(self, size):
        """
        Initialize output map where every tile contains every possible pattern
        """
        self._output = []
        for y in range(size[1]):
            self._output.append([])
            for x in range(size[0]):
                self._output[-1].append(self._tile_model.patterns)
    
    def __str__(self):
        result = ""
        for line in self._output:
            try:
                result = f"{result}{list(map(lambda x: '<>' if len(x) > 1 else '{:2d}'.format(x[0].index), line))}\n"
            except IndexError as e:
                raise UnsolvableException()
            except Exception as e:
                raise e
        return result

if __name__ == "__main__":
    filename = "../resources/images/example4x4.png"

    it = image_translator.ImageTranslator()
    it.breakdown_image(filename, 1)

    tm = tile_model.TileModel(it)
    tm.build_patterns((2, 2))
    tm.build_rules()

    wfc = WaveFunctionCollapse(tm)
    
    for i in range(4):
        wfc.generate_map((32, 32))

        reversed_map = tm.reverse_patterns(wfc.output)

        rebuild_image = it.rebuild_image(reversed_map, f"{filename[:-3]}result{i}.png")
