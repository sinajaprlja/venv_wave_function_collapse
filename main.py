#! bin/python3


import os
import sys
import time

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
pygame.font.init()
pygame.mixer.init()
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

PATTERN_NUM = len(wfc._tile_model.patterns)


_mouse_lock = False



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
    
    @property
    def _ui_x_offset(self) -> int:
        return display_width / 3 * 2
    
    @property
    def _ui_y_offset(self) -> int:
        return display_height / 3 

    def _tile_x_offset(self, x_index: int) -> int:
        return self._grid_x_offset + x_index * self._tile_size

    def _tile_y_offset(self, y_index: int) -> int:
        return self._grid_y_offset + y_index * self._tile_size

    def _quit_handler(self, event: pygame.event.Event) -> None:
        "Quitting the program on esc/quit_event"
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
    def _click_handler(self):
        # Stop constant click events by locking mouse press status till button is released
        global _mouse_lock
        if not pygame.mouse.get_pressed()[0]:
            _mouse_lock = False
            return
        if _mouse_lock:
            return
        x, y = self._mouse_to_tile_index()
        if x >= 0 and x < wfc.size[1] and y >= 0 and y < wfc.size[0]:
            wfc._collapse((x, y))
            wfc._propagate((x, y), wfc.size)
            _mouse_lock = True

    def _mouse_to_tile_index(self) -> None:
        x, y = pygame.mouse.get_pos()
        return (int((x - self._grid_x_offset) // self._tile_size), int((y - self._grid_y_offset) // self._tile_size))
        

    def _draw_grid_border(self) -> None:
        # Draw grid border
        grid_color_index = 1
        grid_border_rect = pygame.Rect((self._grid_x_offset - GRID_BORDER, (display_height - self._grid_height) // 2 - GRID_BORDER, self._grid_width + 2 * GRID_BORDER, self._grid_height + 2 * GRID_BORDER))
        pygame.draw.rect(display, COLOR_PALETTE[grid_color_index], grid_border_rect, GRID_BORDER, 8, 8, 8, 8)
        
        # Draw tiles
        for x in range(wfc.size[1]):
            a, b = (self._tile_x_offset(x), self._grid_y_offset), (self._tile_x_offset(x), self._grid_y_offset + self._grid_height)
            pygame.draw.line(display, COLOR_PALETTE[grid_color_index], a, b)
            a, b = (self._tile_x_offset(x) - 1, self._grid_y_offset), (self._tile_x_offset(x) - 1, self._grid_y_offset + self._grid_height)
            pygame.draw.line(display, COLOR_PALETTE[grid_color_index], a, b)
         
        for y in range(wfc.size[0]):
            a, b = (self._grid_x_offset, self._tile_y_offset(y)), (self._grid_x_offset + self._grid_width, self._tile_y_offset(y))
            pygame.draw.line(display, COLOR_PALETTE[grid_color_index], a, b)
            a, b = (self._grid_x_offset, self._tile_y_offset(y) - 1), (self._grid_x_offset + self._grid_width, self._tile_y_offset(y) - 1)
            pygame.draw.line(display, COLOR_PALETTE[grid_color_index], a, b)
    

    def _draw_containers(self) -> None:
        # Grid container
        pygame.draw.rect(display, COLOR_PALETTE[0], (DISPLAY_BORDER, DISPLAY_BORDER, display_width // 3 * 2, display_height - 2 * DISPLAY_BORDER), 0, 0, 8, 0, 8, 0)
        
        # UI Container
        pygame.draw.rect(display, COLOR_PALETTE[1], (display_width // 3 * 2, DISPLAY_BORDER, display_width // 3 - DISPLAY_BORDER, display_height - 2 * DISPLAY_BORDER), 0, 0, 0, 8, 0, 8)
        
        # InputImage container
        pygame.draw.rect(display, COLOR_PALETTE[3], (display_width//3*2, display_height//3*2, display_width//3 - DISPLAY_BORDER, display_height//3 - DISPLAY_BORDER), 0, 0, 0, 0, 0, 8)
        
        # RuleViewer container
        pygame.draw.rect(display, COLOR_PALETTE[3], (display_width//3*2, DISPLAY_BORDER, display_width//3 - DISPLAY_BORDER, display_height//3 - DISPLAY_BORDER), 0, 0, 0, 8, 0, 0)
        

    def _draw_input_image(self) -> None:
        rect = pygame.Rect(INPUT_IMAGE_POS_X - 4, INPUT_IMAGE_POS_Y - 4, INPUT_IMAGE.get_width() + 8, INPUT_IMAGE.get_height() + 8)
        pygame.draw.rect(display, COLOR_PALETTE[4], rect, 0, 4)
        display.blit(INPUT_IMAGE, (INPUT_IMAGE_POS_X, INPUT_IMAGE_POS_Y))

    def _draw_hovered_tile(self, tile: tuple) -> None:
        x, y = tile
        if x >= 0 and x < wfc.size[0] and y >= 0 and y < wfc.size[1]:
            pygame.draw.rect(display, COLOR_PALETTE[4], (self._tile_x_offset(x), self._tile_y_offset(y), self._tile_size, self._tile_size), 4, 2)
    
    def _draw_legend(self) -> None:
        font = pygame.font.SysFont("monospace", 24)
        for x in range(wfc.size[0]):
            text = font.render(str(x), 1, COLOR_PALETTE[1])
            rect = text.get_rect(center=(self._tile_x_offset(x)+self._tile_size//2, self._grid_y_offset - 24))
            display.blit(text, rect)
            
        for y in range(wfc.size[1]):
            text = font.render(str(y), 1, COLOR_PALETTE[1])
            rect = text.get_rect(center=(self._grid_x_offset - 24, self._tile_y_offset(y)+self._tile_size//2))
            display.blit(text, rect)
                


    def _draw_tile_status(self) -> None:
        _tile_size = (wfc.output[0][0][0].width * len(wfc.output[0][0][0].pixels[0]), wfc.output[0][0][0].height * len(wfc.output[0][0][0].pixels))
        font = pygame.font.SysFont("monospace", int(self._tile_size/2))
        for x in range(wfc.size[1]):
            for y in range(wfc.size[0]):
                c = str(hex(int(255 - 255 / PATTERN_NUM * len(wfc.output[x][y]))))[2:]
                if len(c) < 2:
                    c = f"0{c}"
                color = f"#{c}{c}{c}"
                pygame.draw.rect(display, color, (self._tile_x_offset(x), self._tile_y_offset(y), self._tile_size, self._tile_size), 0, 8)
                
                # Draw number of patterns left
                color = "#448844"
                if len(wfc.output[x][y]) == 1:
                    color = "#44ff44"
                text = font.render(str(len(wfc.output[x][y])), 1, color)
                rect = text.get_rect(center=(self._tile_x_offset(x)+self._tile_size//2, self._tile_y_offset(y) + self._tile_size//2))
                display.blit(text, rect)
                
                # Draw pixeldata of collapsed tiles
                if len(wfc.output[x][y]) == 1:
                    _pixel_data = wfc.output[x][y][0].pixels
                    tile = pygame.Surface(_tile_size)
                    for i in range(wfc.output[0][0][0].width):
                        for j in range(wfc.output[0][0][0].height):
                            pattern = translated_image.tile_map[_pixel_data[i][j]].pixels
                            for k in range(len(pattern[0])):
                                for l in range(len(pattern)):
                                    tile.set_at((i * len(pattern[0]) + k, j * len(pattern) + l), (pattern[k][l][0], pattern[k][l][1], pattern[k][l][2], 128))
                            
                    
                    tile = pygame.transform.scale(tile, (self._tile_size * wfc.output[0][0][0].width, self._tile_size * wfc.output[0][0][0].height))
                    display.blit(tile.subsurface((0, 0, self._tile_size, self._tile_size)), (self._tile_x_offset(x), self._tile_y_offset(y)))

                

    def draw(self) -> None:
        display.fill("#111111")
        
        self._draw_containers()
        self._draw_grid_border()    
        self._draw_legend()
        self._draw_input_image()
        self._draw_tile_status()
        self._draw_hovered_tile(self._mouse_to_tile_index())

        pygame.display.update()

    def menu(self) -> None:
        self._get_tile_size()
        while True:
            for event in pygame.event.get():
                self._quit_handler(event)
            
            self._click_handler()

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


