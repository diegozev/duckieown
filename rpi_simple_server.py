import socket
import sys
sys.path.append('../')
from serial_control.SerialControl import SerialControl
import time

class DriveServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.base_comm = None

    def start(self):
        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set up the server address and port
        server_address = (self.host, self.port)
        self.server_socket.bind(server_address)

        self.base_comm = SerialControl()
        self.base_comm.open_serial()

        # Listen for incoming connections
        self.server_socket.listen(1)

        print('Server is up and listening for connections...')

        try:
            while True:
                # Wait for a client to connect
                print('Waiting for a client to connect...')
                client_socket, client_address = self.server_socket.accept()
                print(f'Client connected: {client_address}')

                while True:
                    # Receive data from the client
                    data = client_socket.recv(1024).decode().strip()
                    if not data:
                        # No more data from the client
                        break

                    # Process the received data and control the motors
                    if data == 'forward':
                        self.base_comm.forward()
                    elif data == 'backward':
                        self.base_comm.backward()
                    elif data == 'spin_L':
                        self.base_comm.spin_left()
                    elif data == 'spin_R':
                        self.base_comm.spin_right()
                    elif data == 'stop':
                        self.base_comm.stop()
                    else:
                        print(f'Invalid command: {data}')

                print(f'Client disconnected: {client_address}')

        finally:
            # Close the server socket
            self.server_socket.close()

if __name__ == '__main__':
    server = DriveServer('omni.local', 5000)
    server.start()
