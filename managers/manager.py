import datetime
import time
from threading import Thread, Lock

import board

from ledboard.data_source.source import Source
from ledboard.displays.display import Display
from ledboard.displays.layers.layer import Layer
from ledboard.screen import ScreenDriver
from queue import PriorityQueue

class MyPriorityQueue(PriorityQueue):
    def peek(self):
        item = None
        with self.mutex:
            if len(self.queue) > 0:
                item = self.queue[0]
        return item

class Manager:
    def __init__(self, refresh_rate, sx, sy):
        self.config = {}
        self.looping_thread = Thread(target=self.__loop)
        self.managing_thread = Thread(target=self.__manage)
        self.manager_lock = Lock()
        self.running = False
        self.refresh_rate = refresh_rate
        self.driver = ScreenDriver(board.D18, sx, sy)
        self.event_queue = MyPriorityQueue()

    def __do_display_tick(self):
        raise NotImplementedError

    def __loop(self):
        while self.running:
            self.__do_display_tick()
            time.sleep(1 / self.refresh_rate)

    def loop(self):
        self.running = True
        self.looping_thread.start()
        self.managing_thread.start()

    def stop(self):
        self.running = False
        self.looping_thread.join()
        self.managing_thread.join()
        self.looping_thread = Thread(target=self.__loop)
        self.managing_thread = Thread(target=self.__manage)

    def add(self, id, d):
        with self.manager_lock:
            self.config[id] = d
            if isinstance(d['instance'], Layer):
                self.config[id]['ds'] = None
                self.config[id]['ds_changed'] = False
            if isinstance(d['instance'], Display):
                l = [self.config[key]['instance'] for key in d['layers']]
                d['instance'].put_layers(l)

    def get_instance(self, key):
        with self.manager_lock:
            if key in self.config:
                return self.config[key]['instance']
            else:
                raise Exception(f"No instance with name {key} found")

    def update_display(self, key):
        with self.manager_lock:
            for layer_key in self.config[key]['layers']:
                if self.config[layer_key]['ds_changed'] is True:
                    self.config[layer_key]['instance'].update(self.config[layer_key]['ds'])
                    self.config[layer_key]['ds_changed'] = False

    def print_display(self, key):
        with self.manager_lock:
            self.driver.show(self.config[key].get_display_pixels())

    def save_ds_change(self, key, data):
        old = self.config[key]['ds']
        if old is None and data is not None \
                or old is not None and data is None \
                or old is not None and data is not None and old != data:
            self.config[key]['ds'] = data
            self.config[key]['ds_changed'] = True

    def get(self, id):
        return self.config[id]

    def notify(self, key):
        with self.manager_lock:
            for obs_layer_name in self.config[key]['notifiable']:
                self.config[obs_layer_name]['ds'] = self.config[key]['instance'].data

    def __manage(self):
        with self.manager_lock:
            for key in self.config:
                if isinstance(self.config[key]['instance'], Source):
                    if 'start' in self.config[key] and self.config[key]['start'] is True:
                        self.event_queue.put((datetime.datetime.now(), key))
        while self.running:
            while True:
                top = self.event_queue.peek()
                if top[0] <= datetime.datetime.now():
                    t, key = self.event_queue.get()
                    with self.manager_lock:
                        self.config[key]['instance'].update()
                        if 'repeat' in self.config[key] and self.config[key]['repeat'] > 0:
                            self.event_queue.put((datetime.datetime.now() + datetime.timedelta(seconds=self.config[key]['repeat'])))
                    self.event_queue.task_done()
                else:
                    break



