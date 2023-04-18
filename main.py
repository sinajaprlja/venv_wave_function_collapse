#! bin/python3


import os
import sys

with open(os.devnull, 'w') as f:
    oldstdout = sys.stdout  # disable standart output to avoid 'hello'-message
    sys.stdout = f          # ...
    import pygame
    sys.stdout = oldstdout  # re-enable standart output


import src.image_translator
import src.tile_model
import src.wave_function_collapse



pygame.init()
display_width, display_height = 1920, 1200
display = pygame.display.set_mode((display_width, display_height), pygame.NOFRAME)
display_width, display_height = display.get_width(), display.get_height()
pygame.display.set_caption("Wave Function Collapse Alogorithm")
clock = pygame.time.Clock()

input_image = "resources/images/example4x4.png"
translated_image = src.image_translator.ImageTranslator.breakdown_image(input_image, 1)
tile_model = src.tile_model.ModelBuilder.build_model(translated_image, (2, 2))
wfc = src.wave_function_collapse.WaveFunctionCollapse(tile_model)
wfc._init_output((16, 16))



GRID_BORDER = 4
GRID_MARGIN = 64
DISPLAY_BORDER = 4

MAX_GRID_WIDTH = display_width // 3 * 2 - 2 * GRID_MARGIN
MAX_GRID_HEIGHT = display_height - 2 * GRID_MARGIN






class App(object):
    def __init__(self):
        self._tile_size = None
    
    @property
    def _grid_height(self) -> int:
        return 0 if self._tile_size is None else self._tile_size * wfc.size[0]
    
    @property
    def _grid_width(self) -> int:
        return 0 if self._tile_size is None else self._tile_size * wfc.size[1]
    
    @property
    def _grid_y_offset(self) -> int:
        return (display_height - self._grid_height) // 2
    
    @property
    def _grid_x_offset(self) -> int:
        return ((display_width / 3 * 2) - self._grid_width) // 2
   


    def _quit_handler(self, event: pygame.event.Event) -> None:
        "Quitting the program on esc/quit_event"
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
    def _draw_grid_border(self) -> None:
        # Draw grid border
        grid_border_rect = pygame.Rect((self._grid_x_offset - GRID_BORDER, (display_height - self._grid_height) // 2 - GRID_BORDER, self._grid_width + 2 * GRID_BORDER, self._grid_height + 2 * GRID_BORDER))
        pygame.draw.rect(display, "#456789", grid_border_rect, GRID_BORDER, 8, 8, 8, 8)

        # Draw tiles
        for x in range(wfc.size[1]):
            a, b = (self._grid_x_offset + x * self._tile_size, self._grid_y_offset), (self._grid_x_offset + x * self._tile_size, self._grid_y_offset + self._grid_height)
            pygame.draw.line(display, "#987654", a, b)
            a, b = (self._grid_x_offset + x * self._tile_size + self._tile_size - 1, self._grid_y_offset), (self._grid_x_offset + x * self._tile_size + self._tile_size - 1, self._grid_y_offset + self._grid_height)
            pygame.draw.line(display, "#987654", a, b)
         
        for y in range(wfc.size[0]):
            a, b =(self._grid_x_offset, self._grid_y_offset + y * self._tile_size), (self._grid_x_offset + self._grid_width, self._grid_y_offset + y * self._tile_size)
            pygame.draw.line(display, "#987654", a, b)
            a, b = (self._grid_x_offset, self._grid_y_offset + y * self._tile_size + self._tile_size - 1), (self._grid_x_offset + self._grid_width, self._grid_y_offset + y * self._tile_size + self._tile_size - 1)
            pygame.draw.line(display, "#987654", a, b)

    def menu(self) -> None:
        self._get_tile_size()
        while True:
            display.fill("#111111")
            for event in pygame.event.get():
                self._quit_handler(event)
            

            
            pygame.draw.rect(display, "#222222", (DISPLAY_BORDER, DISPLAY_BORDER, display_width // 3 * 2, display_height), 8, 0, 8, 0)
            pygame.draw.rect(display, "#333333", (display_width // 3 * 2, DISPLAY_BORDER, display_width // 3, display_height), 0, 8, 0, 8)

            self._draw_grid_border()    
            
            pygame.display.update()

    
    def _get_tile_size(self):
        if (MAX_GRID_WIDTH / wfc.size[1]) * wfc.size[0] < MAX_GRID_HEIGHT:
            self._tile_size = MAX_GRID_WIDTH / wfc.size[1]
        else:
            self._tile_size = MAX_GRID_HEIGHT / wfc.size[0]

    def run(self) -> None:
        self.menu()
    


if __name__ == "__main__":
    app = App()
    app.run()
