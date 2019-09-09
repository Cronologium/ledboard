import neopixel


class ScreenDriver:
    def __init__(self, gpio_port, maxx, maxy):
        self.led_map = {}
        self.leds = maxx * maxy

        if maxx != 16 and maxy != 16:
            raise NotImplementedError

        for x in range(16):
            for y in range(16):
                if x % 2 == 0:
                    self.led_map[(x, y)] = 16 * (15 - x) + 15 - y
                else:
                    self.led_map[(x, y)] = 16 * (15 - x) + y

        self.board = [None for _ in range(self.leds)]
        self.neo = neopixel.NeoPixel(gpio_port, self.leds, brightness=0.1, auto_write=False)
        self.neo.fill((0, 0, 0))
        self.neo.show()

    def show(self, new_board):
        b = [None for _ in range(self.leds)]

        for x in range(len(new_board)):
            for y in range(len(new_board[x])):
                b[self.led_map[(x,y)]] = new_board[x][y]

        for k in range(self.leds):
            if self.board[k] is None and b[k] is not None \
                or self.board[k] is not None and b[k] is None \
                or self.board[k] is not None and b[k] is not None and self.board[k] != b[k]:
                if b[k] is None:
                    self.neo[k] = (0, 0, 0)
                else:
                    self.neo[k] = b[k]

        self.board = b
        self.neo.show()

    def clear(self):
        self.neo.fill((0, 0, 0))
        self.neo.show()

