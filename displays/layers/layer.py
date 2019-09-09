class Layer:
    def __init__(self, maxx, maxy, sx=0, sy=0):
        self.maxx = maxx
        self.maxy = maxy
        self.sx = sx
        self.sx = sy
        self.board = [
            [None for _ in range(self.maxy)] for _ in range(self.maxx)
        ]

    def update(self, data):
        raise NotImplementedError

    def set(self, x, y, color):
        self.board[x][y] = color

    def clear(self):
        self.board = [
            [None for _ in range(self.maxy)] for _ in range(self.maxx)
        ]



