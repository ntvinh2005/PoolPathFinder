import cv2
import numpy as np

start_point = None
end_point = None
is_drawing = False
image = None
transformed_image = None

def draw_rectangle(event, x, y, flags, param):
    global start_point, end_point, is_drawing, image, transformed_image

    if event == cv2.EVENT_LBUTTONDOWN:
        is_drawing = True
        start_point = (x, y)
        end_point = start_point

    elif event == cv2.EVENT_MOUSEMOVE and is_drawing:
        end_point = (x, y)
        temp_image = np.copy(transformed_image)
        cv2.rectangle(temp_image, start_point, end_point, (0, 255, 0), 2)
        cv2.imshow("Draw Rectangle", temp_image)

    elif event == cv2.EVENT_LBUTTONUP:
        is_drawing = False
        end_point = (x, y)

        width = abs(end_point[0] - start_point[0])
        height = abs(end_point[1] - start_point[1])
        
        print(f"Rectangle Width: {width} pixels, Height: {height} pixels")

        cv2.rectangle(transformed_image, start_point, end_point, (0, 255, 0), 2)
        cv2.imshow("Draw Rectangle", transformed_image)
