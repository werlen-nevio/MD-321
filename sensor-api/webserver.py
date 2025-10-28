from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from air_sensor import AirSensor
from light_sensor import LightSensor
from touch_sensor import TouchSensor
from pir_sensor import PirSensor
from ultrasonic_sensor import UltrasonicSensor
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

airSensor = AirSensor()
lightSensor = LightSensor()
touchSensor = TouchSensor()
pirSensor = PirSensor()
ultraSensor = UltrasonicSensor()

host = '0.0.0.0'
port = 8080

class Server(BaseHTTPRequestHandler):
    def sendJSON(self, obj: object, code: int = 200):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Vary', 'Origin')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode())

    def _send_text(self, text: str, code: int = 200, content_type: str = 'text/html'):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Vary', 'Origin')
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(text.encode())

    def do_GET(self):
        if self.path == '/':
            air = airSensor.readAir()
            lux = lightSensor.readLight()
            touch = bool(touchSensor.readTouch())
            motion = bool(pirSensor.readMotion())
            try:
                distance = float(ultraSensor.readDistance_cm())
            except Exception:
                distance = None
            self.sendJSON({
                'status': 'ok',
                'temperature': air.temperature,
                'humidity': air.humidity,
                'light': lux,
                'touch': touch,
                'motion': motion,
                'distance_cm': distance
            })
            return

        if self.path == '/raw':
            air = airSensor.readAir()
            lux = lightSensor.readLight()
            self._send_text(
                f'Temperature: {air.temperature}&deg;C '
                f'Humidity: {air.humidity}% '
                f'Light: {lux}lx'
            )
            return

        if self.path == '/light':
            self._send_text(f'Light: {lightSensor.readLight()}lx')
            return

        if self.path == '/touch':
            self._send_text(f'Touch: {bool(touchSensor.readTouch())}')
            return

        if self.path == '/pir':
            self._send_text(f'Motion: {bool(pirSensor.readMotion())}')
            return

        if self.path == '/ultrasonic':
            try:
                dist = ultraSensor.readDistance_cm()
                self._send_text(f'Distance: {dist}cm')
            except Exception as e:
                self._send_text(f'Error: {e}', code=503)
            return

        if self.path == '/metrics':
            air = airSensor.readAir()
            lux = lightSensor.readLight()
            touch = 1 if bool(touchSensor.readTouch()) else 0
            motion = 1 if bool(pirSensor.readMotion()) else 0
            try:
                distance = ultraSensor.readDistance_cm()
                distance_line = f'ultrasonic_distance_cm {distance}\n'
            except Exception:
                distance_line = ''

            response = (
                '# HELP light measured light intensity in lux\n'
                '# TYPE light gauge\n'
                f'light {lux}\n'
                '# HELP air_temperature measured temperature in celsius\n'
                '# TYPE air_temperature gauge\n'
                f'air_temperature {air.temperature}\n'
                '# HELP air_humidity measured humidity in percent\n'
                '# TYPE air_humidity gauge\n'
                f'air_humidity {air.humidity}\n'
                '# HELP touch_state digital touch sensor state (1/0)\n'
                '# TYPE touch_state gauge\n'
                f'touch_state {touch}\n'
                '# HELP pir_motion motion detected by PIR (1/0)\n'
                '# TYPE pir_motion gauge\n'
                f'pir_motion {motion}\n'
                '# HELP ultrasonic_distance_cm distance measured by HC-SR04 in centimeters\n'
                '# TYPE ultrasonic_distance_cm gauge\n'
                f'{distance_line}'
            )
            self._send_text(response, content_type='text/plain')
            return

        self._send_text('Not Found', code=404, content_type='text/plain')

def main():
    webServer = HTTPServer((host, port), Server)
    print(f'Server started and listen to {host}:{port}')

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    try:
        touchSensor.cleanup()
    except Exception:
        pass
    try:
        pirSensor.cleanup()
    except Exception:
        pass
    try:
        ultraSensor.cleanup()
    except Exception:
        pass

    webServer.server_close()
    print('Server stopped.')

if __name__ == '__main__':
    main()