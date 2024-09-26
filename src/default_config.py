



# When set to True build additional patterns by rotating every previous found pattern, default=True
ROTATE = True

# A little noise is added to entropy for a more natural distribution of patterns, default=0.01
ENTROPY_NOISE = 0.01

# When set to True only choose between patterns with the maximum probability during collapse default=False
# When set to True result will looks kinda strange and uniform
USE_MAX_PROBABILITY = False

# Maximum Number of tries the algorithm gets before terminating
MAX_TRIES = 3

# The higher the level the more info is printed to the user, default=1, !maximum=3 
# Level intentions:
# 0 Off
# 1 Getting an overview of the most important steps
# 2 More detailed overview, mostly "public" methods tho
# 3 Get all steps the algorithm takes, include "private" methods 
DEBUG_LEVEL = 1

