#
# Example Code GPIO Events
# Hagen Richter <hagen.richter@informatik.uni-hamburg.de> 
# <https://github.com/hagenr/gpio-events>
#

import rotary_encoder_events
import button_events
import time

CW_PIN  = 35
ACW_PIN  = 36
SW_PIN = 37

def cb_up(CallingPin):
    btn_new = btn.gpio.input(CallingPin)
    print 'UP Pin: %d val: %d, count: %d' % (CallingPin, btn_new, btn.counter)
    return

def cb_down(CallingPin):
    btn_new = btn.gpio.input(CallingPin)
    print 'DN Pin: %d val: %d, count: %d' % (CallingPin, btn_new, btn.counter)
    return

btn = button_events.Button(SW_PIN, callback_down=cb_down, callback_up=cb_up)
encoder = rotary_encoder_events.RotaryEncoder(CW_PIN, ACW_PIN)

start = 0

while True:

    delta = encoder.get_delta()
    if delta!=0:
        start=start + delta
        print ("rotate %d, count = %d" % (delta, start))
    time.sleep(0.01)
    
