import threading


class RenderLoop(threading.Thread):
    daemon = True

    def __init__(self, plugin, refresh_interval=1):
        super().__init__()

        self.plugin = plugin
        self.refresh_interval = refresh_interval
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            self.plugin.draw_frame()
            self.stop_event.wait(self.refresh_interval)

    def stop(self):
        self.stop_event.set()
