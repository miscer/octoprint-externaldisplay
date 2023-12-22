import logging

from gpiozero import LED


class Backlight:
    def turn_on(self):
        raise NotImplementedError()

    def turn_off(self):
        raise NotImplementedError()


class GPIOBacklight(Backlight):
    def __init__(self, pin: int, logger: logging.Logger):
        self.pin = pin
        self.logger = logger
        self.led = LED(pin, initial_value=True)

    def turn_on(self):
        self.led.on()

    def turn_off(self):
        self.led.off()


class DummyBacklight(Backlight):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def turn_on(self):
        self.logger.info("Backlight turned on")

    def turn_off(self):
        self.logger.info("Backlight turned off")
