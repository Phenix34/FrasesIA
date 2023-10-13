from PIL import Image
import numpy as np
from queue import Queue

def paint_bucket_fill(image, start_x, start_y, target_color, fill_color):
    width, height = image.size
    filled_image = image.copy()
    pixels = filled_image.load()

    queue = Queue()
    queue.put((start_x, start_y))

    while not queue.empty():
        x, y = queue.get()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        current_color = pixels[x, y]

        if current_color != target_color:
            continue

        pixels[x, y] = fill_color

        # Add adjacent pixels to the queue for processing
        queue.put((x + 1, y))
        queue.put((x - 1, y))
        queue.put((x, y + 1))
        queue.put((x, y - 1))

    return filled_image


def blanco_y_negro(image):
    width, height = image.size
    image_resultado = Image.new("RGB", (width, height))

    sobel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])

    sobel_y = np.array([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ])

    pixels_original = image.load()
    pixels_resultado = image_resultado.load()

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            gx = (
                -1 * pixels_original[x - 1, y - 1][0] +
                -2 * pixels_original[x - 1, y][0] +
                -1 * pixels_original[x - 1, y + 1][0] +
                1 * pixels_original[x + 1, y - 1][0] +
                2 * pixels_original[x + 1, y][0] +
                1 * pixels_original[x + 1, y + 1][0]
            )

            gy = (
                -1 * pixels_original[x - 1, y - 1][0] +
                -2 * pixels_original[x, y - 1][0] +
                -1 * pixels_original[x + 1, y - 1][0] +
                1 * pixels_original[x - 1, y + 1][0] +
                2 * pixels_original[x, y + 1][0] +
                1 * pixels_original[x + 1, y + 1][0]
            )

            gray_value = min(255, max(0, int(np.sqrt(gx * gx + gy * gy))))
            new_color = (gray_value, gray_value, gray_value)
            pixels_resultado[x, y] = new_color

    for x in range(width):
        for y in range(height):
            r, g, b = pixels_resultado[x, y]
            pixels_resultado[x, y] = (255, 255 - r, 255 - g, 255 - b)

    return image_resultado


# Ejemplo de uso
imagen_original = Image.open("E:\sobalo\ku.jpg")
imagen_resultado = blanco_y_negro(imagen_original)

start_x = 100
start_y = 100
target_color = (0, 0, 0)
fill_color = (0, 0, 255)
imagen_resultado = paint_bucket_fill(imagen_resultado, start_x, start_y, target_color, fill_color)

imagen_resultado.show()
