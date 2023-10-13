import cv2
import numpy as np

def sobel_edge_detection(image):
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar el filtro de Sobel en los ejes X e Y
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Obtener la magnitud y la dirección del gradiente
    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    gradient_direction = np.arctan2(sobel_y, sobel_x)
    
    # Normalizar la magnitud a escala de 0-255
    gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    return gradient_magnitude

def main():
    # Cargar la imagen
    image = cv2.imread('E:\sobalo\ku.jpg')
    
    # Aplicar el método de detección de bordes de Sobel
    edges = sobel_edge_detection(image)
    
    # Mostrar la imagen original y el resultado en ventanas separadas
    cv2.imshow('Original', image)
    cv2.imshow('Sobel', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
