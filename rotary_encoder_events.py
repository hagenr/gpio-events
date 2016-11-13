#----------------------------------------------------------------------
# rotary_encoder_events.py 
# Hagen Richter <hagen.richter@informatik.uni-hamburg.de> 
# <https://github.com/hagenr/gpio-events>
#
# This is an event driven (rudimentarily) bounce correcting class for rotary encoders
#
# It is advised to put an additional ~100nF capacitor between ground and each input pin to add hardware debouncing
# 
# usage:
#
#     import rotary_encoder_events
#     CW_PIN = 7  # use pin numbers here as defined in gpio.py wrapper class mapping
#     ACW_PIN = 9
#     encoder = rotary_encoder_events.RotaryEncoder(A_PIN, B_PIN, callback=None)
#
#     while True:
#       delta = encoder.get_delta() # returns current delta and resets it (can be higher (negative) number if more clicks were made since last read)
#       if delta!=0: 
#           print delta 
#       time.sleep(0.01)            # might need to be adjusted to prevent accidental bounces and jumps this timeout has proven to be good
#
#     Best use would be a thread for reading all inputs
#     See also: button_events.py class
#

import gpio
import math
import threading

class RotaryEncoder:

    def __init__(self, a_pin, b_pin, callback=None, gpioObject=None):
        # set up
        self.a_pin = a_pin
        self.b_pin = b_pin

        self.callback = callback

        self.a_curr = 1
        self.b_curr = 1

        self.delta = 0

        self.interrupt_lock = threading.Lock()
        
        # gpio wrapper class for better portability
        if gpioObject <> None:
            self.gpio = gpioObject
        else:
            self.gpio = gpio.GPIO()

        self.gpio.setup(self.a_pin, self.gpio.IN, self.gpio.PUD_UP)
        self.gpio.setup(self.b_pin, self.gpio.IN, self.gpio.PUD_UP)
        
        # register events to turns no bouncetime used here
        self.gpio.add_event_detect(self.a_pin, self.gpio.RISING, callback=self.rotary_interrupt)
        self.gpio.add_event_detect(self.b_pin, self.gpio.RISING, callback=self.rotary_interrupt)        
        
    # interrupt wrapper for turning event
    def rotary_interrupt(self, CallingPin):
        # get switch values
        a_new = self.gpio.input(self.a_pin)
        b_new = self.gpio.input(self.b_pin)
        
        # additional bounce check
        if self.a_curr == a_new and self.b_curr == b_new:
            return                                  # abort on bounce

        # save new switch values
        self.a_curr = a_new
        self.b_curr = b_new                        

        if (a_new and b_new):                       # both active? sequence ended
            with self.interrupt_lock:               # get lock 
                if CallingPin == self.b_pin:        # turn direction check
                    self.delta += 1
                else:
                    self.delta -= 1
        if self.callback <> None:                   # call callback if exists
            self.callback(self)
        return       

    # getter for delta
    def get_delta(self):
        self.interrupt_lock.acquire()
        delta = self.delta
        self.delta = 0
        self.interrupt_lock.release()
        return delta

