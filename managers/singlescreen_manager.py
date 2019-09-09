from displays.display import Display
from managers.manager import Manager


class SingleScreenManager(Manager):
    def __init__(self, refresh_rate, sx, sy):
        super().__init__(refresh_rate, sx, sy)
        self.screen_key = None

    def add(self, id, d):
        if self.screen_key is None and isinstance(d['instance'], Display):
            self.screen_key = id
        super().add(id, d)

    def _do_display_tick(self):
        self.update_display(self.screen_key)
        self.print_display(self.screen_key)