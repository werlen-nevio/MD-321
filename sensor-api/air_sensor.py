import threading
from time import sleep
import RPi.GPIO as GPIO
import dht11

class AirSensor:
    def __init__(self, pin=4, poll_sec=2):
        self.instance = dht11.DHT11(pin=pin)
        self.poll_sec = poll_sec
        self.result = self.instance.read()
        self._stop = False
        self._t = threading.Thread(target=self._update_loop, daemon=True)
        self._t.start()

    def _update_loop(self):
        while not self._stop:
            readout = self.instance.read()
            if readout.is_valid():
                self.result = readout
            sleep(self.poll_sec)

    def readAir(self):
        return self.result

    def cleanup(self):
        self._stop = True
        try:
            self._t.join(timeout=1)
        except Exception:
            pass