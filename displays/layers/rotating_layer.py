from displays.layers.layer import Layer


class RotatingLayer(Layer):
    def __init__(self, maxx, maxy, pattern, direction, sx=0, sy=0):
        super().__init__(maxx, maxy, sx=sx, sy=sy)
        self.accumulated_delta = (0, 0)
        self.direction = direction
        for square in pattern:
            self.board[square[0]][square[1]] = square[2]

    def tick(self):
        self.accumulated_delta = tuple(sum(item) for item in zip(self.direction, self.accumulated_delta))
        delta = (0, 0)
        if self.accumulated_delta[0] <= -1:
            delta = (-1, 0)
            self.board = self.board[1:] + self.board[0]
        elif self.accumulated_delta[0] >= 1:
            delta = (1, 0)
            self.board = self.board[-1] + self.board[:-1]
        if self.accumulated_delta[1] <= -1:
            delta = (0, 1)
            self.board = [b[1:] + b[0] for b in self.board]
        elif self.accumulated_delta[1] >= 1:
            delta = (0, -1)
            self.board = [b[-1] + b[:-1] for b in self.board]
        self.accumulated_delta = tuple(sum(item) for item in zip(delta, self.accumulated_delta))

