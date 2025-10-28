import os
import time
import RPi.GPIO as GPIO
from statistics import median

def _ensure_mode(setup_mode: int):
    current = GPIO.getmode()
    if current is None:
        GPIO.setmode(setup_mode)

class UltrasonicSensor:
    def __init__(
        self,
        trig_pin: int | None = None,
        echo_pin: int | None = None,
        setup_mode: int = GPIO.BCM,
        timeout_s: float = 0.03,
    ):
        self.trig = trig_pin or int(os.getenv("US_TRIG_PIN", "23"))
        self.echo = echo_pin or int(os.getenv("US_ECHO_PIN", "24"))
        self.timeout_s = float(os.getenv("US_TIMEOUT_S", str(timeout_s)))

        _ensure_mode(setup_mode)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trig, GPIO.LOW)
        time.sleep(0.05)

    def _pulse(self) -> float:
        GPIO.output(self.trig, GPIO.HIGH)
        time.sleep(10e-6)
        GPIO.output(self.trig, GPIO.LOW)

        start = time.perf_counter()
        while GPIO.input(self.echo) == 0:
            if time.perf_counter() - start > self.timeout_s:
                raise TimeoutError("Ultrasonic: waiting for echo start timed out")
        pulse_start = time.perf_counter()

        while GPIO.input(self.echo) == 1:
            if time.perf_counter() - pulse_start > self.timeout_s:
                raise TimeoutError("Ultrasonic: waiting for echo end timed out")
        pulse_end = time.perf_counter()

        return pulse_end - pulse_start

    def readDistance_cm(self, samples: int = 3, sample_delay_s: float = 0.05) -> float:
        readings = []
        for _ in range(max(1, samples)):
            dt = self._pulse()
            distance_cm = (dt * 34300.0) / 2.0
            readings.append(distance_cm)
            time.sleep(sample_delay_s)
        return round(median(readings), 2)

    def cleanup(self) -> None:
        GPIO.cleanup([self.trig, self.echo])