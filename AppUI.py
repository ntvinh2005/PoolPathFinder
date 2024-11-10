import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from Ball_detect import detect_and_draw_rectangles
from utility import draw_rectangle  # Assuming your utility method handles actual rectangle drawing.

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Billiard Table Perspective Transformation")
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()
        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()
        self.points = []
        self.image = None
        self.image_tk = None
        self.rect_mode = False
        self.rect_start = None  # Starting point for drawing rectangles
        self.rect_end = None    # End point for drawing rectangles
        self.rect_id = None     # Track rectangle ID for canvas

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.original_image = self.image.copy()  
            self.resize_image()
            self.display_image()
            self.points.clear()

    def resize_image(self):
        max_width, max_height = 800, 600
        height, width, _ = self.image.shape
        scale = min(max_width / width, max_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        self.image = cv2.resize(self.image, (new_width, new_height))

    def display_image(self):
        self.image_pil = Image.fromarray(self.image)
        self.image_tk = ImageTk.PhotoImage(self.image_pil)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        self.canvas.bind("<Button-1>", self.get_click)
        self.canvas.bind("<B1-Motion>", self.update_rectangle)  # Track mouse movement while dragging
        self.canvas.bind("<ButtonRelease-1>", self.finalize_rectangle)  # Finalize the rectangle

    def get_click(self, event):
        if len(self.points) < 4:
            self.points.append((event.x, event.y))
            self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, fill='red')
            if len(self.points) == 4:
                self.transform_image()
        else:
             if self.rect_start is None:  # Only start a new rectangle if one isn't being drawn
                self.rect_start = (event.x, event.y)  # Store the start point
                self.rect_end = self.rect_start  # Initial rectangle end point
                self.rect_id = self.canvas.create_rectangle(self.rect_start[0], self.rect_start[1], self.rect_end[0], self.rect_end[1], outline="green", width=2)

    def update_rectangle(self, event):
        if self.rect_start:  # Only update the rectangle if drawing mode is active
            self.rect_end = (event.x, event.y)
            if self.rect_id:  # If a rectangle is being drawn, delete the old one
                self.canvas.delete(self.rect_id)
            self.rect_id = self.canvas.create_rectangle(self.rect_start[0], self.rect_start[1], self.rect_end[0], self.rect_end[1], outline="green", width=2)

    def finalize_rectangle(self, event):
        if self.rect_start:
            self.rect_end = (event.x, event.y)
            # After mouse release, store the rectangle coordinates
            print(f"Rectangle drawn with coordinates: {self.rect_start} to {self.rect_end}")
            self.rect_start = None  # Reset start to prevent re-drawing during another drag
            # Optionally, do something with the rectangle (like storing coordinates)

    def transform_image(self):
        scale_x = self.original_image.shape[1] / self.image.shape[1]
        scale_y = self.original_image.shape[0] / self.image.shape[0]
        adjusted_points = [(int(x * scale_x), int(y * scale_y)) for x, y in self.points]

        new_width = 800
        new_height = int(new_width * 15 / 23)

        pts1 = np.float32(adjusted_points)
        pts2 = np.float32([[0, 0], [new_width, 0], [new_width, new_height], [0, new_height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(self.original_image, matrix, (new_width, new_height))

        self.display_transformed_image(result)

    def display_transformed_image(self, result):
        result = detect_and_draw_rectangles(result)
        new_width = 800
        new_height = int(new_width * 15 / 23)
        result_pil = Image.fromarray(result)
        result_tk = ImageTk.PhotoImage(result_pil)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=result_tk)
        self.canvas.image = result_tk
        self.canvas.config(width=new_width, height=new_height)

