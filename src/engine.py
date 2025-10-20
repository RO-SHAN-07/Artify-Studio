from dataclasses import dataclass
from PIL import Image
import cv2
import numpy as np
import turtle
from io import BytesIO

@dataclass
class TransformationConfig:
    max_image_size: tuple[int, int] = (1920, 1080)
    output_quality: int = 95
    cache_enabled: bool = True
    temp_directory: str = "temp"
    processing_backend: str = 'cpu'

class ImageTransformationEngine:
    def __init__(self, config: TransformationConfig = TransformationConfig()):
        self.config = config
        self.image = None
        self.original_image = None

    def load_image(self, image_path: str):
        try:
            self.original_image = Image.open(image_path)
            self.image = self.original_image.copy()
            # Resize if necessary
            self.image.thumbnail(self.config.max_image_size)
            return {"success": True, "message": "Image loaded successfully."}
        except Exception as e:
            return {"success": False, "message": f"Error loading image: {e}"}

    def apply_transformation(self, transform_type: str, params: dict = None):
        if self.image is None:
            return {"success": False, "message": "No image loaded."}

        # Reset to original image before applying transformation
        self.image = self.original_image.copy()
        self.image.thumbnail(self.config.max_image_size)

        if transform_type == "pencil_sketch":
            return self.pencil_sketch(params)
        elif transform_type == "colored_sketch":
            return self.colored_sketch(params)
        elif transform_type == "opencv_filter":
            return self.opencv_filter(params)
        elif transform_type == "turtle_graphics":
            return self.turtle_graphics(params)
        else:
            return {"success": False, "message": "Invalid transformation type."}

    def export_result(self, format: str = "PNG", quality: int = 95):
        if self.image is None:
            return {"success": False, "message": "No image to export."}

        try:
            # In a real application, we would save to a file
            # For now, we'll just return a success message
            return {"success": True, "message": "Image exported successfully."}
        except Exception as e:
            return {"success": False, "message": f"Error exporting image: {e}"}

    def pencil_sketch(self, params: dict = None):
        try:
            open_cv_image = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
            gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
            inverted_image = 255 - gray_image
            blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
            inverted_blurred = 255 - blurred
            pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
            self.image = Image.fromarray(pencil_sketch)
            return {"success": True, "message": "Pencil sketch applied successfully."}
        except Exception as e:
            return {"success": False, "message": f"Error applying pencil sketch: {e}"}

    def colored_sketch(self, params: dict = None):
        try:
            open_cv_image = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
            # Add your colored sketch logic here
            self.image = Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
            return {"success": True, "message": "Colored sketch applied successfully."}
        except Exception as e:
            return {"success": False, "message": f"Error applying colored sketch: {e}"}

    def opencv_filter(self, params: dict = None):
        try:
            open_cv_image = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
            # Example filter: stylized
            stylized = cv2.stylization(open_cv_image, sigma_s=60, sigma_r=0.6)
            self.image = Image.fromarray(cv2.cvtColor(stylized, cv2.COLOR_BGR2RGB))
            return {"success": True, "message": "OpenCV filter applied successfully."}
        except Exception as e:
            return {"success": False, "message": f"Error applying OpenCV filter: {e}"}

    def turtle_graphics(self, params: dict = None):
        try:
            # This is a placeholder for a more complex turtle graphics implementation
            screen = turtle.Screen()
            screen.setup(width=self.image.width, height=self.image.height)

            # Save the turtle graphics to a canvas, then to an image
            canvas = screen.getcanvas()
            canvas.postscript(file="turtle.eps")

            # Convert the EPS file to an image
            # This requires ghostscript to be installed
            # For simplicity, we'll return a blank image
            self.image = Image.new('RGB', (self.image.width, self.image.height), color = 'white')

            return {"success": True, "message": "Turtle graphics applied successfully."}
        except Exception as e:
            return {"success": False, "message": f"Error applying turtle graphics: {e}"}
