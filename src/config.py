



# When set to True build additional patterns by rotating every previous found pattern, default=True
ROTATE = True

# A little noise is added to entropy for a more natural distribution of patterns, default=0.01
ENTROPY_NOISE = 0.01

# When set to True only choose between patterns with the maximum preobability during collapse
USE_MAX_PROBABILITY = True

# Maximum Number of tries the algorithm gets before terminating
MAX_TRIES = 3

# The higher the level the more info is printed to the user, default=1, !maximum=3 
# Level intentions:
# 0 Off
# 1 Getting an overview of the most important steps
# 2 More detailed overview, mostly "public" methods tho
# 3 Get all steps the algorithm takes, include "private" methods 
DEBUG_LEVEL = 1

# Automatically save translated_image/tile_model as they are static for given input
# and theres no need to create them multiple times. On the other hand translatation/modeling
# doesn't really take much resources...
AUTO_SAVE_TRANSLATED_IMAGE = True
AUTO_SAVE_TILE_MODEL = True
