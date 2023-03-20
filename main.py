#! bin/python3


import os
import sys

with open(os.devnull, 'w') as f:
    oldstdout = sys.stdout  # disable standart output to avoid 'hello'-message
    sys.stdout = f          # ...
    import pygame
    sys.stdout = oldstdout  # re-enable standart output



pygame.init()
display_width, display_height = 1440, 810
pygame.display.set_mode((display_width, display_height))


input_image = "resources/images/example4x4.png"



class App(object):
    def __init__(self):
        pass

    
    def menu(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    
    def run(self) -> None:
        self.menu()
    


if __name__ == "__main__":
    app = App()
    app.run()
