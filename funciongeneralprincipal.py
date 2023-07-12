import cv2
import numpy as np
from SerialControl import SerialControl
import time
import sys
from get_data import camara
from principal21 import obtener_fuga
from picamera import PiCamera

sys.path.append('../')    

# El funcionamiento general del codigo consiste en la declaracion de variables de control, las cuales comienzan tomando el valor "0",
# pero a medida que el frame es analizado por las funciones presentes en main(), dichas funciones modifican el valor de las variables de control en base al analisis de los elementos
# capturados por la camara de la base omnidireccional, para que finalmente la funcion movimiento entregue las ordenes a realizar segun los valores de las variables de control.
    
#########################################################################################################################################
#la siguiente funcion permite detectar patos presentes en la imagen capturada por la camara mediante analisis de color, en este caso naranja.
def detectarpatos(frame):
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #valores de treshold del naranja

    lower_orange = np.array([0, 40, 90])
    upper_orange = np.array([4, 255, 255])

    orange_mask = cv2.inRange(hsv_image, lower_orange, upper_orange)

# Definimos los contornos de objetos naranja
    orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# Dibujar cajas en items naranja de area mayor a 20000.
    for cnt in orange_contours:
        if cv2.contourArea(cnt) > 20000:  # Ignore small contours
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  #pato bounding box 
            patos=1  #si patos==1, significa que se ve un pato en el frame y debe ser esquivado.
        else:
            patos=0  #no se ven aptos en el frame. 
        return patos

#las siguientes funciones son empleadas para detectar el cruce peatonal presente en la duckiepista.

#esta primera funcion cambia la perspectiva de la imagen para facilitar el trabajo de la fuincion CountWhitePixels.

def warpImg(frame, points, w, h, inv=False):
    pts1 = np.float32(points) 
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(frame, matrix, (w, h))
    return imgWarp

#esta funcion cuenta la cantidad de pixeles blancos presentes en una zona del frame, y asi detectar un posible cruce peatonal.
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
    if white_pixels > 40000: #si es mayor a este umbral la deteccion de blanco existe cruce
        cruce=1 #existe cruce peatonal
    else:
        cruce=0 #no existe cruce
        return cruce


#la funcion a continuacion es utilizada para detectar el signo pare que da fin al recorrido de la base omnidireccional, se basa en detectar un item de gran area de color azul.
#Es similar a patos pero con color azul.
def signopare_azul(frame):
    #------------  ADD YOUR CODE HERE   -----------
    # Convert the frame to the HSV color space    
    ##elegir puntos para transformacion perspectiva REGIÓN DE INTERÉS

    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    #Definir contornos para el azul
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # Dibujar el contorno azul alrededor del signo pare
    for cnt in blue_contours:
        area = cv2.contourArea(cnt)
        if area > 10000:  # Ignorar pequeños elementos azules
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  #forma del contorno del signo pare
            return 1 #si se detecta el signo pare azul, la variable cambia a 1
        else:
            return 0 #no se detecta signo pare



#########################################################################################################################################
#funcion de movimiento 

#La funcion a continuacion determina las acciones a realizar por la base segun la situacion descrita por el frame, los posibles casos importantes se describen en base a 
#las variables de control definidas previamente.

def movimiento(camino,patos,cruce,pare): 

        if (camino==0 and patos==0 and cruce==0):#camino Despejado
            base_comm.forward()


        elif (camino==1 and patos==0 and cruce==0): #desviado
            base_comm.spin_left() #alineamos la base
            time.sleep(0.1)
            base_comm.forward()
            time.sleep(0.1)
            base_comm.forward()

        elif (camino==2 and patos==0 and cruce==0): #CURVA, se "toma" la curva mediante un corto spin a la izquierda y un avance.
            base_comm.spin_left()
            time.sleep(0.2)
            base_comm.forward()
            time.sleep(0.1)
            base_comm.forward()    


        elif (patos==1): #se detecta un pato en el camino, se inicia la maniobra evasiva
            base_comm.stop()
            time.sleep(1)
            base_comm.lateral_left()
            time.sleep(2)
            base_comm.forward()
            time.sleep(2)
            base_comm.lateral_right()
            time.sleep(2)
            base_comm.forward()
        
        elif (camino==0 and patos==0 and cruce==1): #se detecta un cruce peatonal, se detiene la base unos segundos y sigue el camino.
            base_comm.stop()
            time.sleep(2)
            base_comm.forward() 
            time.sleep(2)
            base_comm.forward() 

        elif (camino==1 and patos==1 and cruce==0): ##se detecta un pato en el camino, se inicia la maniobra evasiva, pero al hallarnos desviados del camino, primeramente se alinea la base
            base_comm.spin_left() #esto alinea la base previamente al esquive.
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

        elif (camino==1 and patos==0 and cruce==1): #Estamos desviados de la pista y existe cruce, primero enderezamos la base y luego nos detenemos.
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
            base_comm.forward()

        elif(pare==1): #se detecta el signo pare, se mueve la abse hacia la izquierda y detenemos el movimiento.
            base_comm.stop()
            time.sleep(1)
            base_comm.lateral_left()
            time.sleep(1)
            base_comm.stop()
            time.sleep(200000)

# la siguietne funcion es la responsable del funcionamiento de la base y la inclusion de todas las funciones definidas en este codigo y en principal21, describe el curso de accion
# mencionado al inicio del codigo.
def main():
    global base_comm
    camino=0
    patos=0
    cruce=0
    pare=0
    # Lectura de la imagen
    camara() #activa la captura de la camara
    frame = cv2.imread('image.jpg') #lee la imagen creada por la camara
    #se aplican las distintas funciones que modifican a las variables de control.
    camino=obtener_fuga(frame)
    patos=detectarpatos(frame)
    cruce=countWhitePixels(frame)
    pare=signopare_azul(frame)
    movimiento(camino,patos,cruce,pare) #se inicia movimiento para decidir que acciones debe realizar la base omnidireccional.

#a continuacion se determina la perpetuidad de la funcion main.
if __name__ == "__main__":
    base_comm = SerialControl()
    base_comm.open_serial()
    time.sleep(0) 
    while True:
        main()   

    
