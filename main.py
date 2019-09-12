from data_source.time_source import TimeSource
from displays.display import Display
from displays.layers.rotating_gradient_layer import RotatingGradientLayer
from displays.layers.sliding_layer import SlidingLayer
from displays.layers.string_layer import StringLayer
from managers.singlescreen_manager import SingleScreenManager
from utils import hex2tuple

BOARD_SIZE = (16, 16)

TIME_LAYER = 'timelayer-hhmm'
RAIN_LAYER = 'layer-rain'
WEATHERDISPLAY = 'display-weather'
DS_TIME = 'ds-time'
TIMEDISPLAY = 'display-time'

GRADIENT_DISPLAY = 'display-gradient'
GRADIENT_LAYER = 'layer-gradient'
REFRESH_RATE = 5


DROPLETS_LOCATIONS = [
    (5, 6), (2, 0), (9, 3), (15, 10), (8, 14)
]

RAIN_NUANCES = [
    hex2tuple('256d7b'),
    hex2tuple('739ba5'),
    hex2tuple('95b4bb'),
    hex2tuple('b8ccd1')
]

def spread_gradient_points(gradient_colors):
    marginal_points = [
        (0, y) for y in range(BOARD_SIZE[1] - 1)
    ] + [
        (x, BOARD_SIZE[1] - 1) for x in range(BOARD_SIZE[0] - 1)
    ] + [
        (BOARD_SIZE[0] - 1, y) for y in range(BOARD_SIZE[1] - 1, 0, -1)
    ] + [
        (x, 0) for x in range(BOARD_SIZE[0] - 1, 0, -1)
    ]
    return [
        marginal_points[k * (len(marginal_points) // len(gradient_colors)) + 1 * (k < len(marginal_points) % len(gradient_colors))] + (gradient_colors[k], ) for k in range(len(gradient_colors))
    ]


def main():
    rain_board = []
    for droplet in DROPLETS_LOCATIONS:
        for k in range(0, 4):
            rain_board.append(((droplet[0] + BOARD_SIZE[0] - k) % BOARD_SIZE[0], droplet[1], RAIN_NUANCES[k]))

    manager = SingleScreenManager(REFRESH_RATE, 16, 16)

    '''
    manager.add(TIME_LAYER, {
        'instance': StringLayer(BOARD_SIZE[0], BOARD_SIZE[1], (205, 127, 50))
    })
    manager.add(DS_TIME, {
        'instance': TimeSource(DS_TIME, manager),
        'repeat': 1,
        'start': True,
        'notifiable': [TIME_LAYER]
    })

    manager.add(RAIN_LAYER, {
        'instance': SlidingLayer(BOARD_SIZE[0], BOARD_SIZE[1], rain_board, (5 / REFRESH_RATE, 0))
    })

    manager.add(TIMEDISPLAY, {
        'instance': Display(BOARD_SIZE[0], BOARD_SIZE[1]),
        'layers': [TIME_LAYER]
    })
    
    manager.add(WEATHERDISPLAY, {
        'instance': Display(BOARD_SIZE[0], BOARD_SIZE[1]),
        'layers': [RAIN_LAYER, TIME_LAYER]
    })'''
    gradient_starter = spread_gradient_points([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
    print(gradient_starter)
    manager.add(GRADIENT_LAYER, {
        'instance': RotatingGradientLayer(BOARD_SIZE[0], BOARD_SIZE[1], gradient_starter, (5 / REFRESH_RATE))
    })

    manager.add(GRADIENT_DISPLAY, {
        'instance': Display(BOARD_SIZE[0], BOARD_SIZE[1]),
        'layers': [GRADIENT_LAYER]
    })


    input()
    manager.loop()
    input()
    manager.stop()

if __name__ == '__main__':
    main()