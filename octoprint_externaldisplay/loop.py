import threading


class RenderLoop(threading.Thread):
    def __init__(self, plugin, refresh_interval=1):
        super().__init__()

        self.plugin = plugin
        self.refresh_interval = refresh_interval
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            self.render()
            self.stop_event.wait(self.refresh_interval)

    def render(self):
        self.plugin.draw_frame()

        if self.plugin.framebuffer:
            image = self.plugin.canvas.get_image()
            self.plugin.framebuffer.write(image)

    def stop(self):
        self.stop_event.set()
        self.join()
