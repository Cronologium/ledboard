from ledboard.data_source.time_source import TimeSource
from ledboard.displays.display import Display
from ledboard.displays.layers.string_layer import StringLayer
from ledboard.managers.singlescreen_manager import SingleScreenManager

BOARD_SIZE = (16, 16)

TIMELAYER = 'timelayer-hhmm'
DS_TIME = 'ds-time'
TIMEDISPLAY = 'display-time'

def main():
    manager = SingleScreenManager(1, 16, 16)

    manager.add('timelayer-hhmm', {
        'instance': StringLayer(BOARD_SIZE[0], BOARD_SIZE[1], (205, 127, 50))
    })
    manager.add(DS_TIME, {
        'instance': TimeSource(DS_TIME, TIMELAYER),
        'repeat': 1
    })
    manager.add(TIMEDISPLAY, {
        'instance': Display(BOARD_SIZE[0], BOARD_SIZE[1]),
        'layers': [TIMELAYER]
    })


if __name__ == '__main__':
    main()