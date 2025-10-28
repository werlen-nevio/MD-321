import smbus

try:
    bus = smbus.SMBus(1)
except FileNotFoundError:
    bus = smbus.SMBus(0)

class LightSensor:
    def __init__(self, address=0x5C):
        self.DEVICE = address
        self.ONE_TIME_HIGH_RES_MODE_1 = 0x20

    def convertToNumber(self, data):
        return (data[1] + (256 * data[0])) / 1.2

    def readLight(self) -> float:
        data = bus.read_i2c_block_data(self.DEVICE, self.ONE_TIME_HIGH_RES_MODE_1, 2)
        return round(self.convertToNumber(data), 2)