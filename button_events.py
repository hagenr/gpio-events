#
# GPIO Wrapper Class
# Hagen Richter <hagen.richter@informatik.uni-hamburg.de> 
# <https://github.com/hagenr/gpio-events>
#
# This class is for reading button inputs (e.g rotary encoder push switch) with a bit of bounce resistance via software.
# The whole thing depends on a gpio wrapper and events.
# 
# callbacks can be given for button down and button up events
# 

import gpio
import threading
import time

class Button:

    def __init__(self, btn_pin, callback_down=None, callback_up=None, bouncetime=25, gpioObject = None):
        self.btn_pin = btn_pin
        
        self.bouncetime = bouncetime
        
        self.callback_down = callback_down
        self.callback_up = callback_up

        self.btn_curr = 1
        
        self.counter = 0

        self.interrupt_lock = threading.Lock()
        
        # gpio wrapper class for better portability
        if gpioObject <> None:
            self.gpio = gpioObject
        else:
            self.gpio = gpio.GPIO()

        self.gpio.setup(self.btn_pin, self.gpio.IN, self.gpio.PUD_UP)
 
        self.gpio.add_event_detect(self.btn_pin, self.gpio.BOTH, callback=self.btn_callback, bouncetime=self.bouncetime)         
                 
    def btn_callback(self,CallingPin):
        btn_new = self.gpio.input(self.btn_pin)
        with self.interrupt_lock:
            if btn_new <> self.btn_curr:
                self.btn_curr=btn_new
                if btn_new:
                    if (self.callback_up <> None):
                        self.callback_up(CallingPin)
                else:
                    self.counter = self.counter + 1                    
                    if (self.callback_down <> None):
                        self.callback_down(CallingPin)
        return       
                 

        
