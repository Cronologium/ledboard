import datetime

from data_source.source import Source


class TimeSource(Source):
    def __fetch(self):
        now = datetime.datetime.now()

        return "{0}{1}".format(now.minute, now.second)