#
# GPIO Wrapper Class
# Hagen Richter <hagen.richter@informatik.uni-hamburg.de> 
# <https://github.com/hagenr/gpio-events>
#

import RPi.GPIO

class GPIO:
    def __init__(self):
        self.gpio = RPi.GPIO
        self.setup = self.gpio.setup
        self.output = self.gpio.output
        self.input = self.gpio.input
        self.OUT = self.gpio.OUT
        self.IN = self.gpio.IN
        self.HIGH = self.gpio.HIGH
        self.LOW = self.gpio.LOW
        self.PUD_UP = self.gpio.PUD_UP
        self.PUD_DOWN = self.gpio.PUD_DOWN
        self.PUD_OFF = self.gpio.PUD_OFF
        self.RISING = self.gpio.RISING
        self.FALLING = self.gpio.FALLING
        self.BOTH = self.gpio.BOTH
        self.add_event_detect = self.gpio.add_event_detect
        self.gpio.setmode(self.gpio.BOARD)
        self.cleanup = self.gpio.cleanup
        