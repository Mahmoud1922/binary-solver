
import pygame

EMPTY = '_'

class Cube:
    '''Representation of a cell in a playing board'''

    def __init__(self, value, row, col, dimension, width, height):
        self._value = value
        # Calculate the width (=height) of a cell
        self._gap = width / dimension
        # Calculate location of the cell in the window
        self._loc = (col * self._gap, row * self._gap)
        self._selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        if self._value != EMPTY:
            text = fnt.render(str(self._value), 1, (0, 0, 0))
            win.blit(text, (self._loc[0] + (self._gap / 2 - text.get_width() / 2),
                     self._loc[1] + (self._gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(
                win, (255, 0, 0), (self._loc[0], self._loc[1], self._gap, self._gap), 3)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        assert(value in {'0', '1', EMPTY})
        self._value = value
