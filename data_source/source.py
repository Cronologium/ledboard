import traceback


class Source:
    def __init__(self, key, observable):
        self.key = key
        self.observable = observable
        self.old_source = None
        self.data = None

    def _fetch(self):
        raise NotImplementedError

    def update(self):
        self.old_source = self.data
        try:
            self.data = self._fetch()
            if self.data is None and self.old_source is not None \
                    or self.data is not None and self.old_source is None \
                    or self.data is not None and self.old_source is not None and self.data != self.old_source:
                self.observable.notify(self.key)
        except Exception:
            print(traceback.format_exc())


