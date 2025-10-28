import os
import time
import RPi.GPIO as GPIO
from typing import Callable, Optional

def _ensure_mode(setup_mode: int):
    current = GPIO.getmode()
    if current is None:
        GPIO.setmode(setup_mode)

class PirSensor:
    def __init__(
        self,
        pin: int | None = None,
        pull: str | None = None,
        setup_mode: int = GPIO.BCM,
        bouncetime_ms: int = 100,
    ):
        self.pin = pin or int(os.getenv("PIR_PIN", "27"))
        pull = (pull or os.getenv("PIR_PULL", "DOWN")).upper()
        self._bouncetime_ms = bouncetime_ms

        _ensure_mode(setup_mode)
        pud = GPIO.PUD_DOWN if pull == "DOWN" else GPIO.PUD_UP if pull == "UP" else GPIO.PUD_OFF
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=pud)

    def readMotion(self) -> bool:
        return bool(GPIO.input(self.pin))

    def add_event_callback(self, on_change: Callable[[bool], None]) -> None:
        def _cb(_ch: int):
            on_change(self.readMotion())
        GPIO.add_event_detect(self.pin, GPIO.BOTH, bouncetime=self._bouncetime_ms, callback=_cb)

    def wait_for_motion(self, timeout_s: Optional[float] = None) -> bool:
        ch = GPIO.wait_for_edge(self.pin, GPIO.RISING, timeout=int(timeout_s * 1000) if timeout_s else None)
        return ch is not None

    def cleanup(self) -> None:
        try:
            GPIO.remove_event_detect(self.pin)
        except Exception:
            pass
        GPIO.cleanup(self.pin)