from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from air_sensor import AirSensor
from light_sensor import LightSensor
from touch_sensor import TouchSensor

airSensor = AirSensor()
lightSensor = LightSensor()
touchSensor = TouchSensor()

host = '0.0.0.0'
port = 8080

class Server(BaseHTTPRequestHandler):
    def sendJSON(self, object: object, code: int = 200):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Vary', 'Origin')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(object).encode())


    def do_GET(self):
        if self.path == '/':
            values = airSensor.readAir()
            lightValue = lightSensor.readLight()
            self.sendJSON({
                'status': 'ok',
                'temperature': values.temperature,
                'humidity': values.humidity,
                'light': lightValue
            })

        if self.path == '/raw':
            values = airSensor.readAir()
            lightValue = lightSensor.readLight()
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(f'Temperature: {values.temperature}&deg;C Humidity: {values.humidity}% Light: {lightValue}lx', 'utf-8'))

        if self.path == '/light':
            lightValue = lightSensor.readLight()
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(f'Light: {lightValue}lx', 'utf-8'))
            
        if self.path == '/touch':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(f'Touch: {touchSensor.readTouch().touched}', 'utf-8'))

        if self.path == '/metrics':
            values = airSensor.readAir()
            lightValue = lightSensor.readLight()
            response = f'\
# HELP light measured light intensity in lux\n\
# TYPE light gauge\n\
light {lightValue}\n\
# HELP air_temperature measured temperature in celcius\n\
# TYPE air_temperature gauge\n\
air_temperature {values.temperature}\n\
# HELP air_humidity measured humidity in percent\n\
# TYPE air_humidity gauge\n\
air_humidity {values.humidity}'
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', '*')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.send_header('Vary', 'Origin')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(response.encode())

def main():
    webServer = HTTPServer((host, port), Server)
    print(f'Server started and listen to {host}:{port}')

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print('Server stopped.')

if __name__ == '__main__':
    main()