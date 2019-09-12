import math

from displays.layers.pixel_layer import PixelLayer


class RotatingGradientLayer(PixelLayer):
    def __init__(self, maxx, maxy, pattern, rotating_speed, sx=0, sy=0):
        super().__init__(maxx, maxy, pattern, sx=sx, sy=sy)
        self.rotating_speed = rotating_speed
        self.accumulated_delta = 0
        self.reference_points = {(p[0], p[1]): self.board[p[0]][p[1]] for p in pattern}
        self._make_mix()

    def _mix(self, mixer):
        ref_max = mixer[-1][0]
        total_proportion = sum([ref_max - mixer_color[0] for mixer_color in mixer])
        return (
            sum([self.reference_points[mixer_color[1]][k] * (ref_max - mixer_color[0]) for mixer_color in mixer]) / total_proportion
            for k in range(3)
        )

    def _make_mix(self):
        for x in range(self.maxx):
            for y in range(self.maxy):
                if (x, y) in self.reference_points:
                    continue
                self.board[x][y] = self._mix(
                    sorted([(abs(x - key[0]) ** 2 + abs(y - key[1]) ** 2, value) for key, value in
                            self.reference_points.items()])
                )

    def tick(self):
        self.accumulated_delta += self.rotating_speed
        sign = (lambda x: (1, -1)[x < 0])
        delta_val = sign(self.rotating_speed)
        while abs(self.accumulated_delta) >= 1:
            self.accumulated_delta += -1 * delta_val
            p = [key for key in self.reference_points]
            point_mapping = {}
            for point in p:
                d = (0, 0)
                if point[0] < point[1]: # above the main diagonal
                    if point[0] < self.maxy - 1 - point[1]: # above the secondary diagonal
                        d = (0, delta_val)
                    elif point[0] > self.maxy - 1 - point[1]: # under the secondary
                        d = (delta_val, 0)
                elif point[0] > point[1]: # under the main diagonal
                    if point[0] < self.maxy - 1 - point[1]: # above the secondary
                        d = (0, -delta_val)
                    elif point[0] > self.maxy - 1 - point[1]: # under the secondary
                        d = (-delta_val, 0)
                if sum(d) == 0: # it's placed on a diagonal, identify which
                    if point[0] == point[1]: # on first diagonal
                        if point[0] < self.maxy - 1 - point[1]: # above the secondary
                            d = (delta_val * (delta_val == -1), delta_val * (delta_val == 1))
                        elif point[0] > self.maxy - 1 - point[1]: # under the secondary
                            d = (-delta_val * (delta_val == -1), -delta_val * (delta_val == 1))
                    else: # on second diagonal
                        if point[0] < point[1]: # above main diagonal
                            d = (delta_val * (delta_val == 1), delta_val * (delta_val == -1))
                        else:
                            d = (-delta_val * (delta_val == 1), -delta_val * (delta_val == -1))
                point_mapping[point] = (point[0] + d[0], point[1] + d[1])
            self.reference_points = {
                point_mapping[p]: self.reference_points[p] for p in self.reference_points
            }
        self._make_mix()





