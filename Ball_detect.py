import cv2
import numpy as np

#HSV color ranges for billiard balls
COLOR_RANGES = {
    'yellow': ([15, 150, 150], [35, 255, 255]), 
    'blue': ([90, 50, 50], [130, 255, 255]),        
    'red_lower': ([0, 100, 100], [10, 255, 255]),  
    'red_upper': ([160, 100, 100], [180, 255, 255]), 
    'purple': ([110, 50, 50], [170, 255, 100]),     
    'orange': ([5, 150, 150], [25, 255, 255])       
}

rect_x1, rect_y1, rect_x2, rect_y2 = 29, 42, 780, 485

def detect_and_draw_rectangles(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    cropped_image = image[rect_y1:rect_y2, rect_x1:rect_x2]
    cropped_hsv_image = hsv_image[rect_y1:rect_y2, rect_x1:rect_x2]

    for color_name, (lower, upper) in COLOR_RANGES.items():
        lower_bound = np.array(lower)
        upper_bound = np.array(upper)

        color_mask = cv2.inRange(cropped_hsv_image, lower_bound, upper_bound)

        color_mask = cv2.dilate(color_mask, np.ones((5, 5), np.uint8), iterations=2)

        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100: 
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image, (x + rect_x1, y + rect_y1), (x + rect_x1 + w, y + rect_y1 + h), (0, 255, 0), 2) 

        cv2.imshow(f"{color_name} detection", color_mask)
        cv2.waitKey(0)

    cv2.imshow("Final Ball Detection by Color", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
