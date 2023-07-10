import asyncio
import websockets
import base64
import picamera
import io
import time

class VideoServer:
    def __init__(self):
        self.camera = None
        self.frame_count = 0
        self.max_frame_count = 2

    async def send_video(self, websocket, path):
        # Set up the Raspberry Pi camera
        self.camera = picamera.PiCamera()
        self.camera.resolution = (320, 240)
        self.camera.iso = 800
        self.camera.awb_mode = 'sunlight'
        self.camera.shutter_speed = 30000
        time.sleep(1)

        try:
            # Continuously capture and send video frames
            while True:
                # Capture a frame
                stream = io.BytesIO()
                self.camera.capture(stream, format='jpeg', use_video_port=True)

                # Skip frames according to the frame count
                self.frame_count += 1
                if self.frame_count % self.max_frame_count != 0:
                    # Delete the captured frame without sending it
                    stream.close()
                    continue

                # Read the captured frame
                stream.seek(0)
                encoded_image = base64.b64encode(stream.read()).decode('utf-8')

                try:
                    # Send the frame to the client
                    await websocket.send(encoded_image)
                except websockets.exceptions.ConnectionClosed:
                    # Connection closed by the client
                    print("Client connection closed")
                    break

                # Delete the captured frame
                stream.close()

        finally:
            # Clean up resources
            self.camera.close()

    async def start_server(self):
        server = await websockets.serve(self.send_video, '0.0.0.0', 8765)

        # Keep the server running until interrupted
        await server.wait_closed()

if __name__ == "__main__":
    video_server = VideoServer()
    asyncio.run(video_server.start_server())
