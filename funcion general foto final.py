import cv2
import numpy as np
from SerialControl import SerialControl
import time
import sys
from get_data import camara
from principal2 import obtener_fuga
from picamera import PiCamera
from hexagonosverdes import detect_green_hexagon

sys.path.append('../')

def main():
    # Lectura de la imagen
    ret, frame = cv2.imread('image.jpg')

    if not ret:
        print("No se pudo leer el fotograma")
        exit()
    else:
        return frame

#########################################################################################################################################
#la siguiente funcion detecta si estamos dentro de las lineas correctas.

camino=obtener_fuga(main())

    
#########################################################################################################################################
    #la siguiente funcion detecta si tenemos un pato dentro del frame
def detectarpatos(frame):
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# Define the lower and upper thresholds for the orange color
    lower_orange = np.array([0, 40, 90])
    upper_orange = np.array([4, 255, 255])

    orange_mask = cv2.inRange(hsv_image, lower_orange, upper_orange)

# Find contours of orange regions
    orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# Draw bounding boxes around orange ducks
    for cnt in orange_contours:
        area = cv2.contourArea(cnt)
    if area > 25000:  # Ignore small contours
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  #pato bounding box 
        patos=1  
    else:
        patos=0   
    return patos

#funcion para determinar el cruce patonal
def warpImg(frame, points, w, h, inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(frame, matrix, (w, h))
    return imgWarp

def countWhitePixels(frame):
    frame = cv2.resize(frame, (640, 480))  # RESIZE
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 168])
    upper_white = np.array([172, 111, 255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white) 
    white_pixels = np.sum(frame == 255)
    frameThres = mask_white
    h, w, c = frame.shape
    points = [[100, 100], [w-100, 100], [w//2-50, h-100], [w//2+50, h-100]]  # Define specific points for warp transformation
    frameWarp = warpImg(frameThres, points, w, h)
    white_pixels = np.sum(frameWarp == 255)
    if white_pixels > 40000:
        cruce=1
    else:
        cruce=0
        return cruce

#funcion de deteccion signo pare.    
pare=detect_green_hexagon(main())


#########################################################################################################################################
#funcion de movimiento 
def movimiento(camino,patos,cruce,pare): 
        camino=round(camino)
        patos=round(patos)
        cruce=round(cruce)
        pare=round(pare)

        if (camino==0 and patos==0 and cruce==0):
            base_comm.forward()


        elif (camino==1 and patos==0 and cruce==0):
            base_comm.spin_left()
            time.sleep(0.25)
            base_comm.forward()


        elif (patos==1):
            base_comm.stop()
            time.sleep(1)
            base_comm.lateral_left()
            time.sleep(2)
            base_comm.forward()
            time.sleep(2)
            base_comm.lateral_right()
            time.sleep(2)
            base_comm.forward()
        
        elif (camino==0 and patos==0 and cruce==1):
            base_comm.stop()
            time.sleep(2)
            base_comm.forward() 
            time.sleep(2)
            base_comm.forward() 

        elif (camino==1 and patos==1 and cruce==0):
            base_comm.spin_left()
            time.sleep(0.5)            
            base_comm.stop()
            time.sleep(2)
            base_comm.lateral_left()
            time.sleep(2)
            base_comm.forward()
            time.sleep(2)
            base_comm.lateral_right()
            time.sleep(2)
            base_comm.forward()  

        elif (camino==1 and patos==0 and cruce==1):
            base_comm.spin_left()
            time.sleep(0.5) 
            base_comm.stop()
            time.sleep(2)
            base_comm.forward() 
            time.sleep(2)
            base_comm.forward()

        elif(camino==2): 
            base_comm.diagonal_front_left()
            time.sleep(3)
            base_comm.spin_left()  
            time.sleep(0.5)  
            base_comm.forward  

        elif(pare==1):
            base_comm.stop()
            time.sleep(1)
            base_comm.lateral_left
            time.sleep(1)
            base_comm.stop()



if __name__ == "__main__":
    base_comm = SerialControl()
    base_comm.open_serial()
    time.sleep(0.5) 
    main()
    camara()

    
