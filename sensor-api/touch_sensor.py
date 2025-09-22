from RPi import GPIO
import signal

class TouchSensor:
    def __init__(self, pin=11):
        self.pin = pin
        self._setup_gpio()

    def _setup_gpio(self):
        """Initialisiert GPIO für den Touch-Sensor."""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _on_touch(self, channel):
        """Callback-Funktion bei Touch-Ereignis."""
        print("Touch wurde erkannt")

    def run(self):
        """Startet die Ereigniserkennung und wartet."""
        try:
            GPIO.add_event_detect(
                self.pin, GPIO.FALLING, callback=self._on_touch, bouncetime=200
            )
            signal.pause()
        except KeyboardInterrupt:
            pass
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    sensor = TouchSensor(pin=11)
    sensor.run()