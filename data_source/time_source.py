import datetime

from ledboard.data_source.source import Source


class TimeSource(Source):
    def __fetch(self):
        now = datetime.datetime.now()

        return f"{now.minute}{now.second}"