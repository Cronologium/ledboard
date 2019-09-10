import os

from displays.layers.layer import Layer

PATTERNS_DIR = 'displays/patterns'

class StringLayer(Layer):
    def __init__(self, maxx, maxy, color):
        super().__init__(maxx, maxy)
        self.color = color
        self.string_limit = (maxx // 8) * (maxy // 8)
        self.patterns = {
            key[0]: self.__read(key) for key in os.listdir(PATTERNS_DIR) if os.path.isfile(os.path.join(PATTERNS_DIR, key))
        }

    def __read(self, file):
        data = None
        with open(os.path.join(PATTERNS_DIR, file), "r") as f:
            data = f.readlines()
        return [d[:-1] for d in data]

    def update(self, data):
        for k in range(min(self.string_limit, len(data))):
            ch = " "
            if k < len(data):
                ch = data[k]
            if ch not in self.patterns:
                continue
            x = k // (self.maxy // 8)
            y = k % (self.maxy // 8)
            for xx in range(8):
                for yy in range(8):
                    if self.patterns[ch][xx][yy] == '*':
                        self.set(x * 8 + xx, y * 8 + yy, self.color)

