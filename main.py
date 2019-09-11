from data_source.time_source import TimeSource
from displays.display import Display
from displays.layers.rotating_layer import RotatingLayer
from displays.layers.string_layer import StringLayer
from managers.singlescreen_manager import SingleScreenManager
from utils import hex2tuple

BOARD_SIZE = (16, 16)

TIMELAYER = 'timelayer-hhmm'
RAIN_LAYER = 'layer-rain'
WEATHERDISPLAY = 'display-weather'
DS_TIME = 'ds-time'
TIMEDISPLAY = 'display-time'
REFRESH_RATE = 5


def main():
    manager = SingleScreenManager(REFRESH_RATE, 16, 16)

    '''
    manager.add(TIME_LAYER, {
        'instance': StringLayer(BOARD_SIZE[0], BOARD_SIZE[1], (205, 127, 50))
    })
    manager.add(DS_TIME, {
        'instance': TimeSource(DS_TIME, manager),
        'repeat': 1,
        'start': True,
        'notifiable': [TIMELAYER]
    })
    '''
    manager.add(RAIN_LAYER, {
        'instance': RotatingLayer(BOARD_SIZE[0], BOARD_SIZE[1], [
            (6, 5, hex2tuple('256d7b')),
            (5, 5, hex2tuple('739ba5')),
            (4, 5, hex2tuple('95b4bb')),
            (3, 5, hex2tuple('b8ccd1'))
        ], (1 / REFRESH_RATE, 0))
    })

    '''
    manager.add(TIMEDISPLAY, {
        'instance': Display(BOARD_SIZE[0], BOARD_SIZE[1]),
        'layers': [TIMELAYER]
    })
    '''

    manager.add(WEATHERDISPLAY, {
        'instance': Display(BOARD_SIZE[0], BOARD_SIZE[1]),
        'layers': [RAIN_LAYER]
    })


    input()
    manager.loop()
    input()
    manager.stop()

if __name__ == '__main__':
    main()