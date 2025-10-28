import RPi.GPIO as GPIO

class TouchSensor:
    def __init__(self, pin=17, pull_up=True, bouncetime_ms=200):
        self.pin = pin
        self.bouncetime_ms = bouncetime_ms

        pud = GPIO.PUD_UP if pull_up else GPIO.PUD_DOWN
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=pud)

        self._cb_registered = False

    def _on_touch(self, channel):
        print("Touch wurde erkannt")

    def run(self):
        try:
            GPIO.add_event_detect(
                self.pin, GPIO.FALLING, callback=self._on_touch, bouncetime=self.bouncetime_ms
            )
            self._cb_registered = True
        except KeyboardInterrupt:
            pass

    def readTouch(self) -> int:
        return 0 if GPIO.input(self.pin) == GPIO.LOW else 1

    def cleanup(self):
        try:
            if self._cb_registered:
                GPIO.remove_event_detect(self.pin)
        except Exception:
            pass
        try:
            GPIO.cleanup(self.pin)
        except Exception:
            pass