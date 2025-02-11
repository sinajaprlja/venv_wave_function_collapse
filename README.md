# Wave Function Collapse

TODO 

[X] Rebuild overlap checker, seems to have problems for lower side<br>
[X] Move overlap to Pattern class<br>
[X] rebuild propagation<br>
[ ] Add all the debug messages<br> 
[ ] Better commenting inside the code<br>


## Translating images
Images can be translated using the following code<br>

```python
from image_translator import ImageTranslator

# Initialize ImageTranslator
translator = ImageTranslator()

# Translate image
image_path = "PATH_TO_IMAGE_FILE"
tile_size = TILE_SIZE
translator.translate_image(image_path: str, tile_size: int)

# Access data
translated_image = translator.translated_image
translation_map = translator.translation_map
```

TILE\_SIZE
> Tiles are quadratic patterns, size is an integer, representing width/height in pixels.

translated\_image
> The translated image is made of a 2-dimensional matrix containing integers, every integer corresponds to
> a specific pattern at the elements location


translation\_map
> The translation map is a list containing all found patterns in the original image, the pattern index
> corresponds to the integer in the "translated\_image"-matrix

## Building the tile model
Use a translated\_image to generate a set of rules for generating new images
Rules are generated by the following code.<br>

```python
from image_translator import ImageTranslator
from tile_model import TileModel

# Initialize TileModel with translated_image
tm = TileModel(IMAGE_TRANSLATOR)

# Extract patterns of specific size
tm.build_patterns((PATTERN_WIDTH, PATTERN_HEIGHT))

# Build set of rules
tm.build_rules()
```

## Generating new images from model
Build procedurally generated bitmaps out of small input images.
```python
from image_translator import ImageTranslator
from tile_model import TileModel
from wave_function_collapse import WaveFunctionCollapse

# Initialize WaveFunctionCollapse with tile_model
wfc = WaveFunctionCollapse(TILE_MODEL)

# Build new bitmap
wfc.generate_map((OUTPUT_HEIGHT, OUTPUT_WIDTH))
```
TILE\_MODEL
>

OUT\_HEIGHT, OUTPUT\_WIDTH
> The dimensions of the output, important to note that height comes before width as 
> size and indexing is internally handled as (row, column) instead of (x, y)


## Configs
For a better overview and control of various aspects see the config.py file
Every config option is explained more detailed inside the file itself
