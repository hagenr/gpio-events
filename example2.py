#
# Example Code GPIO Events 2
# Hagen Richter <hagen.richter@informatik.uni-hamburg.de> 
# <https://github.com/hagenr/gpio-events>
#
# 
#

import rotary_encoder_events
import button_events
import threading
import time
import gpio

CW_PIN  = 35
ACW_PIN  = 36
SW_PIN = 37


# Settings class for saving and changing values from different threads
class Settings:
    VAL = 0
    MIN = 1
    MAX = 2
    DEFAULT = 3
    LOCK = 4
    tempMax = [25,0,100,25,threading.Lock()]
    
    def get_tempMax(self):
        return self.tempMax[self.VAL]
        
    def set_tempMax(self, newVal):
        with self.tempMax[self.LOCK]:
            if newVal > self.tempMax[self.MAX]:      
                self.tempMax[self.VAL] = self.tempMax[self.MAX]
            elif newVal < self.tempMax[self.MIN]:
                self.tempMax[self.VAL] = self.tempMax[self.MIN]
            else:
                self.tempMax[self.VAL] = newVal
            
    def reset_tempMax(self,dummy=None):
        with self.tempMax[self.LOCK]:
            self.tempMax[self.VAL] = self.tempMax[self.DEFAULT]

            
# Worker thread in/output while the main thread works
class IOWorker(threading.Thread):
    def __init__(self, settings):
        threading.Thread.__init__(self)
        self.settings = settings
        self.stopping = False
        self.daemon = True
        self.delay = 0.1
        self.gpio = gpio.GPIO()
        self.encoderTempMax = rotary_encoder_events.RotaryEncoder(CW_PIN, ACW_PIN, gpioObject=self.gpio)
        self.buttonTempMax = button_events.Button(SW_PIN, callback_down=self.settings.reset_tempMax, gpioObject=self.gpio)

    def run(self):
        while not self.stopping:
            self.settings.set_tempMax(self.settings.get_tempMax()+self.encoderTempMax.get_delta())
            time.sleep(self.delay)

    def stop(self):
        self.gpio.cleanup()
        self.stopping = True

        
# Main Program doing everything
class Program:
    sleeptime = 1
    settings = Settings()
    IOWorker = IOWorker(settings)
    
    def __init__(self):
        print "init"
        self.IOWorker.start()
        
    def loop(self):
        while True:
            print "TempMax: %d" % self.settings.get_tempMax()
            time.sleep(self.sleeptime)

    def destroy(self):
        print "destroy"
        self.IOWorker.stop()


# start it        
if __name__ == "__main__":
    program = Program()
    try:
        program.loop()
    except KeyboardInterrupt:
        program.destroy()
    