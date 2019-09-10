import datetime

from data_source.source import Source


class TimeSource(Source):
    def _fetch(self):
        return datetime.datetime.now().strftime("%M%S")