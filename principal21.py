import cv2
import numpy as np
from SerialControl import SerialControl
import time
import sys
# import camera

sys.path.append('../')

# La siguiente funcion es la empleada a la hora de detectar si la trayectoria actual esta dentro de las vias, la base debe ubicarse entre la linea amarilla y la blanca del camino para 
# estar encarrilada, por lo que detectamos ambas lineas y calculamos el punto medio entre ambas detectado por la imagen, luego segun el valor que obtenemos sabremos si la base esta
#encarrilada o no.

def obtener_fuga(frame):    
    ## Elegir puntos para transformación perspectiva REGIÓN DE INTERÉS
    tl = (50,300) #top left
    bl = (5,472) #bottom left 
    tr = (550,300) #top right
    br = (635,472) #bottom right

    #

    ## Aplicar transformación de perspectiva
    pts1 = np.float32([tl, bl, tr, br])
    pts2 = np.float32([[0, 0], [0, 480], [640, 0], [640, 480]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    transformed_frame = cv2.warpPerspective(frame, matrix, (640, 480))

    #

    hsv_transformed_frame = cv2.cvtColor(transformed_frame, cv2.COLOR_BGR2HSV)

    l_h = 0  # Ajusta los valores de los trackbars aquí si es necesario
    l_s = 0
    l_v = 200
    u_h = 255
    u_s = 50
    u_v = 255

    # Rango para el blanco
    lower = np.array([l_h,l_s,l_v])
    upper = np.array([u_h,u_s,u_v])

    # Rangos de color para la línea amarilla
    lower_yellow = np.array([15, 50, 100])
    upper_yellow = np.array([35, 255, 255])

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Máscaras para la línea blanca y la línea amarilla
    mask_white = cv2.inRange(hsv_transformed_frame, lower, upper)
    mask_yellow = cv2.inRange(hsv_transformed_frame, lower_yellow, upper_yellow)

    # Unir las máscaras para detectar ambas líneas
    mask = cv2.bitwise_or(mask_white, mask_yellow)


#las siguientes lineas de codigo se encargan de obtener el punto medio en la imagen, y a la variable fuga le otorgan el valor del punto medio.
    histogram = np.sum(mask[mask.shape[0] // 2:, :], axis=0)
    midpoint = int(histogram.shape[0] / 2)
    left_base = np.argmax(histogram[:midpoint])
    right_base = np.argmax(histogram[midpoint:]) + midpoint
    fuga = (right_base + left_base) /2
    distancia = right_base - left_base #es una variable auxiliar que permite detectar si las lineas se solapan, implicando en que se detecta una curva.
    print(fuga)

    #los valores de fuga y distancia son utilizados para determinar el estado de encarrilamiento del bot y que acciones debera tomar a continuacion.
    
    if fuga>250 and distancia>100: #la base esta encarrilada, 
        return 0 #no se debe ajustar la orientacion de la base.
    elif fuga>250 and distancia<100: #la base esta encarrilada, pero se detecta una curva
        return 2 #curva
    else: #la base esta descarrilada.
        return 1 #enderezarse

