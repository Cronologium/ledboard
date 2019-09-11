from displays.layers.layer import Layer


class PixelLayer(Layer):
    def __init__(self, maxx, maxy, pattern, sx=0, sy=0):
        super().__init__(maxx, maxy, sx, sy)
        for square in pattern:
            self.board[square[0]][square[1]] = square[2]
