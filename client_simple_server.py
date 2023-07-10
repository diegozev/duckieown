import socket
import keyboard

class RemoteControl:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            # Connect to the server
            self.client_socket.connect((self.server_address, self.server_port))
            print('Connected to the server.')

            while True:
                # Wait for a key press event
                key_event = keyboard.read_event()

                if key_event.event_type == 'down':
                    # Map key press events to commands
                    if key_event.name == 'w':
                        command = 'forward'
                    elif key_event.name == 's':
                        command = 'backward'
                    elif key_event.name == 'a':
                        command = 'spin_L'
                    elif key_event.name == 'd':
                        command = 'spin_R'
                    else:
                        command = 'stop'

                    # Send the command to the server
                    self.client_socket.sendall(command.encode())

                    if key_event.name == 'esc':
                        command = 'stop'
                        # Send the command to the server
                        self.client_socket.sendall(command.encode())
                        break

        finally:
            # Close the client socket
            self.client_socket.close()

# Usage example
server_address = 'omni.local'  # Replace with the IP/hostname address of your Raspberry Pi
server_port = 5000

rc = RemoteControl(server_address, server_port)
rc.connect()
