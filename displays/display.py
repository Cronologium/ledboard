class Display:
    def __init__(self, maxx, maxy, layers=None):
        self.maxx = maxx
        self.maxy = maxy
        self.layers = []

    def put_layers(self,layers):
        self.layers = layers

    def get_display_pixels(self):
        board = [
            [None for _ in range(self.maxy)] for _ in range(self.maxx)
        ]
        for x in range(self.maxx):
            for y in range(self.maxy):
                for layer in self.layers[::-1]:
                    if layer.sx <= x < layer.sx + layer.maxx and layer.sy <= y < layer.sy and layer.board[x][y] is not None:
                        board[x][y] = layer.board[x][y]
                        break
        return board
