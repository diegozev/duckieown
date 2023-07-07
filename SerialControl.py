import serial
from serial import Serial
import time

class SerialControl:

    def __init__(self, port="/dev/ttyUSB0"):
        self.port = port
        self.serial = None
        self.serial_port = ""

    def open_serial(self):
        try:
            self.serial = Serial(self.port, 9600, timeout=1, write_timeout=0.2)
            print("The port is available")
            self.serial_port = "Open"
            time.sleep(2)
        except serial.serialutil.SerialException:
            print("The port is at use")
            self.serial.close()
            self.serial.open()

    def close_serial(self):
        time.sleep(0.2)
        self.serial.close()
        self.serial_port = "Close"

    def forward(self):
        self.serial.write('FW\n'.encode())

    def backward(self):
        self.serial.write('BW\n'.encode())

    def spin_right(self):
        self.serial.write('SR\n'.encode())

    def spin_left(self):
        self.serial.write('SL\n'.encode())

    def lateral_right(self):
        self.serial.write('LR\n'.encode())

    def lateral_left(self):
        self.serial.write('LL\n'.encode())

    def diagonal_front_right(self):
        self.serial.write('DFR\n'.encode())

    def diagonal_front_left(self):
        self.serial.write('DFL\n'.encode())

    def diagonal_back_right(self):
        self.serial.write('DBR\n'.encode())

    def diagonal_back_left(self):
        self.serial.write('DBL\n'.encode())

    def stop(self):
        self.serial.write('STOP\n'.encode())
   