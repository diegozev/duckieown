import cv2
import numpy as np

# Open the video file
video_path = "patovideobueno.mp4"
cap = cv2.VideoCapture(video_path)

# Check if the video file was successfully opened
if not cap.isOpened():
    print("Error opening video file")

# Read the first frame
ret, frame = cap.read()

def frame_processing(frame):
    #------------  ADD YOUR CODE HERE   -----------
    # Convert the frame to the HSV color space    
    ##elegir puntos para transformacion perspectiva REGIÓN DE INTERÉS

    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Find contours of red and green regions
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # Draw bounding boxes around red apples
    for cnt in blue_contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # Ignore small contours
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  #pato bounding box

    return frame

    # new_frame = np.zeros([720, 1280, 3])


    #------------ END -----------
    #return new_frame

new_video = []

# Loop through all frames
while ret:
    # Process the frame here    
    new_frame = frame_processing(frame)

    # Add new frame to list of new video
    new_video.append(new_frame)

    # Display the processed frame
    cv2.imshow("Processed Frame", new_frame)

    # Wait for the 'q' key to exit
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

    # Read the next frame
    ret, frame = cap.read()

# Create video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('Tareas/t2_output.avi', fourcc, 30, (1280, 720))

for i in range(len(new_video)):
    video.write(new_video[i])

# Release the video file and close windows
cap.release()
video.release()  
cv2.destroyAllWindows()



