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

COLOR_PALETTE = ["#2a2d34", "#a2a7a5", "#dae2df", "#157145", "#eea243"]


pygame.init()
display_width, display_height = 1920, 1200
display = pygame.display.set_mode((display_width, display_height), pygame.NOFRAME)
display_width, display_height = display.get_width(), display.get_height()
pygame.display.set_caption("Wave Function Collapse Alogorithm")
clock = pygame.time.Clock()

input_image_path = "resources/images/example4x4.png"
translated_image = src.image_translator.ImageTranslator.breakdown_image(input_image_path, 1)
tile_model = src.tile_model.ModelBuilder.build_model(translated_image, (2, 2))
wfc = src.wave_function_collapse.WaveFunctionCollapse(tile_model)
wfc._init_output((16, 16))



GRID_BORDER = 4
GRID_MARGIN = 64
DISPLAY_BORDER = 4

MAX_GRID_WIDTH = display_width // 3 * 2 - 2 * GRID_MARGIN
MAX_GRID_HEIGHT = display_height - 2 * GRID_MARGIN

INPUT_IMAGE = pygame.image.load(input_image_path).convert()
INPUT_IMAGE_MAX_DISPLAY_SIZE = 256
_factor = INPUT_IMAGE_MAX_DISPLAY_SIZE // max(INPUT_IMAGE.get_width(), INPUT_IMAGE.get_height())
INPUT_IMAGE = pygame.transform.scale(INPUT_IMAGE, (INPUT_IMAGE.get_width() * _factor, INPUT_IMAGE.get_height() * _factor))
INPUT_IMAGE_POS_X = (display_width  - DISPLAY_BORDER) // 3 * 2 + ((display_width//3  - DISPLAY_BORDER - INPUT_IMAGE.get_width()) // 2)
INPUT_IMAGE_POS_Y = (display_height - DISPLAY_BORDER) // 3 * 2 + ((display_height//3 - DISPLAY_BORDER - INPUT_IMAGE.get_height()) // 2)

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
        grid_color_index = 1
        grid_border_rect = pygame.Rect((self._grid_x_offset - GRID_BORDER, (display_height - self._grid_height) // 2 - GRID_BORDER, self._grid_width + 2 * GRID_BORDER, self._grid_height + 2 * GRID_BORDER))
        pygame.draw.rect(display, COLOR_PALETTE[grid_color_index], grid_border_rect, GRID_BORDER, 8, 8, 8, 8)
        
        # Draw tiles
        for x in range(wfc.size[1]):
            a, b = (self._grid_x_offset + x * self._tile_size, self._grid_y_offset), (self._grid_x_offset + x * self._tile_size, self._grid_y_offset + self._grid_height)
            pygame.draw.line(display, COLOR_PALETTE[grid_color_index], a, b)
            a, b = (self._grid_x_offset + x * self._tile_size + self._tile_size - 1, self._grid_y_offset), (self._grid_x_offset + x * self._tile_size + self._tile_size - 1, self._grid_y_offset + self._grid_height)
            pygame.draw.line(display, COLOR_PALETTE[grid_color_index], a, b)
         
        for y in range(wfc.size[0]):
            a, b =(self._grid_x_offset, self._grid_y_offset + y * self._tile_size), (self._grid_x_offset + self._grid_width, self._grid_y_offset + y * self._tile_size)
            pygame.draw.line(display, COLOR_PALETTE[grid_color_index], a, b)
            a, b = (self._grid_x_offset, self._grid_y_offset + y * self._tile_size + self._tile_size - 1), (self._grid_x_offset + self._grid_width, self._grid_y_offset + y * self._tile_size + self._tile_size - 1)
            pygame.draw.line(display, COLOR_PALETTE[grid_color_index], a, b)
    

    def _draw_containers(self) -> None:
        # Grid container
        pygame.draw.rect(display, COLOR_PALETTE[0], (DISPLAY_BORDER, DISPLAY_BORDER, display_width // 3 * 2, display_height - 2 * DISPLAY_BORDER), 0, 0, 8, 0, 8, 0)
        
        # UI Container
        pygame.draw.rect(display, COLOR_PALETTE[1], (display_width // 3 * 2, DISPLAY_BORDER, display_width // 3 - DISPLAY_BORDER, display_height - 2 * DISPLAY_BORDER), 0, 0, 0, 8, 0, 8)
        
        # InputImage container
        pygame.draw.rect(display, COLOR_PALETTE[3], (display_width//3*2, display_height//3*2, display_width//3 - DISPLAY_BORDER, display_height//3 - DISPLAY_BORDER), 0, 0, 0, 0, 0, 8)

    def _draw_input_image(self) -> None:
        rect = pygame.Rect(INPUT_IMAGE_POS_X - 4, INPUT_IMAGE_POS_Y - 4, INPUT_IMAGE.get_width() + 8, INPUT_IMAGE.get_height() + 8)
        pygame.draw.rect(display, COLOR_PALETTE[4], rect, 0, 4)
        display.blit(INPUT_IMAGE, (INPUT_IMAGE_POS_X, INPUT_IMAGE_POS_Y))

    def _draw_current_cell(self, mouse_pos: tuple) -> None:
        cell_row = (mouse_pos[1] - self._grid_y_offset) // self._tile_size
        cell_column = (mouse_pos[0] - self._grid_x_offset) // self._tile_size
        if cell_row >= 0 and cell_row < wfc.size[0] and cell_column >= 0 and cell_column < wfc.size[1]:
            pygame.draw.rect(display, COLOR_PALETTE[4], (self._grid_x_offset + cell_column * self._tile_size, self._grid_y_offset + cell_row * self._tile_size, self._tile_size, self._tile_size), 4, 2)


    def draw(self) -> None:
        display.fill("#111111")
        
        self._draw_containers()
        self._draw_grid_border()    
        self._draw_input_image()
        self._draw_current_cell(pygame.mouse.get_pos())

        pygame.display.update()

    def menu(self) -> None:
        self._get_tile_size()
        while True:
            for event in pygame.event.get():
                self._quit_handler(event)
            
            self.draw()

    
    def _get_tile_size(self):
        if (MAX_GRID_WIDTH / wfc.size[1]) * wfc.size[0] < MAX_GRID_HEIGHT:
            self._tile_size = MAX_GRID_WIDTH / wfc.size[1]
        else:
            self._tile_size = MAX_GRID_HEIGHT / wfc.size[0]

    def run(self) -> None:
        self.menu()
    


if __name__ == "__main__":
    try:
        app = App()
        app.run()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
    except Exception as e:
        raise e


